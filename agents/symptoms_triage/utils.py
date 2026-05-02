from typing import List, Dict, Sequence
from chromadb import Collection, ClientAPI
from pathlib import Path

from .memory import QueryMemory
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# Begin: disable all Hugging Face's verbosity
import os
os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'

from huggingface_hub import utils as hf_utils
hf_utils.disable_progress_bars()

import transformers
transformers.utils.logging.set_verbosity_error()
transformers.utils.logging.disable_progress_bar()

import logging
logging.getLogger('huggingface_hub').setLevel(logging.ERROR)
# End: disable all Hugging Face's verbosity

CURRENT_DIR = Path(__file__).parent
MEMORY_FILE = CURRENT_DIR / "patient_memories.json"
memory = QueryMemory(MEMORY_FILE)

_analyzer = AnalyzerEngine()
_anonymizer = AnonymizerEngine()
_PII_ENTITIES = ["EMAIL_ADDRESS", "PHONE_NUMBER"]


def _load_diagnostics(file_path: str) -> list:
    """
    Reads a diagnostics markdown file and returns a list of tuples:
    (id, title, definition, symptoms)
    """
    import re

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception:
        raise RuntimeError(f"Error: Could not read the contents of '{file_path}'.")

    # Split the file by diagnostic (## headers)
    # We ignore the first element because it contains the main # title
    diagnostic_sections = re.split(r'\n##\s+', content)[1:]
    
    diagnostics_list = []

    for section in diagnostic_sections:
        # Extract specific fields using non-greedy matches between ### headers
        definition = re.search(r'### Definition\n+(.*?)(?=\n+###|\n+---|\Z)', section, re.DOTALL)
        symptoms = re.search(r'### Symptoms\n+(.*?)(?=\n+###|\n+---|\Z)', section, re.DOTALL)

        # Clean and format the extracted data
        diagnostic_title = section.split('\n')[0].strip()
        diagnostic_id = re.sub(r'\s+', '_', diagnostic_title.lower())
        diagnostic_definition = " ".join(definition.group(1).split()) if definition else ""
        # Clean symptom list: remove dashes and join into single string
        if symptoms:
            symptoms_text = symptoms.group(1).strip()
            symptom_lines = [re.sub(r'^-\s*', '', line).strip() for line in symptoms_text.split('\n') if line.strip()]
            diagnostic_symptoms = " ".join(symptom_lines)
        else:
            diagnostic_symptoms = ""

        diagnostics_list.append((diagnostic_id, diagnostic_title, diagnostic_definition, diagnostic_symptoms))

    return diagnostics_list


def _chunk(diagnostics: list) -> list:
    """
    Chunk diagnostics for better retrieval.
    """
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    # Configure text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=25,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    # Chunk all documents
    all_chunks = []
    for diagnostic_id, diagnostic_title, diagnostic_definition, diagnostic_symptoms in diagnostics:
        chunks = text_splitter.split_text(diagnostic_symptoms)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "diagnostic_id": f"{diagnostic_id}_chunk_{i}",
                "diagnostic_title": diagnostic_title,
                "diagnostic_definition": diagnostic_definition,
                "content": chunk
            })

    return all_chunks


def _init_client():
    import chromadb
    from pathlib import Path

    db_path = Path(__file__).parent / "chroma_db"
    return chromadb.PersistentClient(path=str(db_path))


def _get_or_create_collection(client: ClientAPI) -> Collection:
    return client.get_or_create_collection(
        name="diagnostics",
        metadata={"hnsw:space": "cosine"}
    )


def _store(collection: Collection, chunks: List[Dict]) -> None:
    ids = [chunk["diagnostic_id"] for chunk in chunks]
    documents = [chunk["content"] for chunk in chunks]
    metadatas = [{
        "diagnostic_title": chunk["diagnostic_title"],
        "diagnostic_definition": chunk["diagnostic_definition"]} for chunk in chunks]

    collection.add(ids=ids, documents=documents, metadatas=metadatas)


async def _create_embedded(query: str) -> Sequence[float]:
    """
    Process user query and convert to embedding for vector search.
    """
    from pydantic_ai import Embedder

    # Model is downloaded from Hugging Face on first use
    embedder = Embedder('sentence-transformers:all-MiniLM-L6-v2')

    cleaned_query = " ".join(query.lower().split())
    embedded_query = await embedder.embed_query(cleaned_query)
    return embedded_query[0]


def _retrieve_relevant_chunks(collection: Collection, embedded_query: Sequence[float], top_k=3) -> list:
    """
    Retrieve relevant chunks from the vector database using the embedded query.
    """
    # Perform similarity search
    results = collection.query(
        query_embeddings=embedded_query,
        n_results=top_k
    )

    # Process and display results
    search_results = []
    for i, (doc_id, distance, content, metadata) in enumerate(zip(
        results['ids'][0],
        results['distances'][0],
        results['documents'][0],
        results['metadatas'][0]
    )):
        similarity = 1 - distance  # Convert distance to similarity
        if similarity >= 0.3: # Only add those chunks with a similarity above 0.3
            search_results.append({
                'id': doc_id,
                'content': content,
                'metadata': metadata,
                'similarity': similarity
            })

    return search_results


def _filter_duplicate_diagnostics(diagnostics: list) -> list:
    """
    Filter out duplicate diagnostics, keeping only the highest similarity result for each unique diagnostic.
    """
    seen = {}

    for diagnostic in diagnostics:
        diagnostic_title = diagnostic['metadata']['diagnostic_title']
        # Keep the diagnostic with the highest similarity score
        if diagnostic_title not in seen or diagnostic['similarity'] > seen[diagnostic_title]['similarity']:
            seen[diagnostic_title] = diagnostic

    return list(seen.values())


def store_diagnostics_in_vector_database(file_path: str) -> Collection:
    """
    Store document chunks in a vector database.
    """
    client = _init_client()
    collection = _get_or_create_collection(client)

    if collection.count() == 0:
        diagnostics = _load_diagnostics(file_path)
        chunks = _chunk(diagnostics)
        _store(collection, chunks)
    return collection


async def extract_diagnostics_from_query(collection: Collection, query: str) -> list:
    """
    Extract the diagnostics from a user query.
    """
    embedded_query = await _create_embedded(query)
    diagnostics = _retrieve_relevant_chunks(collection, embedded_query)
    return _filter_duplicate_diagnostics(diagnostics)


def augment_prompt_with_diagnostics(query: str, diagnostics: list) -> str:
    """
    Augment the original query with retrieved diagnostics (i.e., custom context) to create a richer prompt for the LLM.
    """
    str_diagnostics = ""
    for diagnostic in diagnostics:
        str_diagnostics += f"{diagnostic['metadata']['diagnostic_title']}\n"
        str_diagnostics += f"ID: {diagnostic['id']}\n"
        str_diagnostics += f"Title: {diagnostic['metadata']['diagnostic_title']}\n"
        str_diagnostics += f"Definition: {diagnostic['metadata']['diagnostic_definition']}\n"
        str_diagnostics += f"Symptoms: \n {diagnostic['content']}\n"
        str_diagnostics += "\n"

    return f"""
        Answer the user's question based on the provided diagnostic data:

        Diagnostics:
        {str_diagnostics}

        Question:
        {query}
    """


def augment_prompt_with_patient_recent_queries(prompt: str) -> str:
    """
    Augment the prompt with patient's recent queries from the last 7 days.
    """
    recent_queries = memory.get_recent_queries()
    if not recent_queries:
        return prompt

    queries_context = "\n".join(recent_queries)
    augmented_prompt = f"""
    {prompt}

    ### Patient Query History (last 7 days):
    {queries_context}
    """

    return augmented_prompt


def _redact_pii(text: str) -> str:
    """Detect and redact PII (email addresses and phone numbers) from text."""
    results = _analyzer.analyze(text=text, entities=_PII_ENTITIES, language="en")
    return _anonymizer.anonymize(text=text, analyzer_results=results).text


def store_patient_query(query: str) -> None:
    """Store the patient query in memory for future context, with PII redacted."""
    sanitized = _redact_pii(query)
    memory.add_query(sanitized)
