from pydantic_ai import Agent
from typing import List
from chromadb import Collection
from pathlib import Path

from agents.shared.models import Diagnostic

from .utils import (
    store_diagnostics_in_vector_database,
    augment_prompt_with_diagnostics,
    augment_prompt_with_patient_recent_queries,
    extract_diagnostics_from_query,
    store_patient_query,
)

system_prompt = f""""
    You are a helpful assistant that answers medical questions based on the provided diagnostic data.

    ### Role and behaviour:
    - Provide a clear, accurate answer based on the diagnostics above.
    - Consider all diagnostics collectively, as symptoms frequently overlap across different conditions.
    - Answer using only the provided diagnostics; do not fabricate data.
    - In case of insufficient information, do not provide any answer.
    """

# Create an agent using Claude model
agent = Agent(
    model="anthropic:claude-sonnet-4-5",
    system_prompt=system_prompt,
    output_type=List[Diagnostic]
)


async def answer_query(query: str, collection: Collection) -> List[Diagnostic]:
    """
    Generate an answer to the user query based on the existing diagnostics and recent query history.
    """
    diagnostics = await extract_diagnostics_from_query(collection, query)
    prompt = augment_prompt_with_diagnostics(query, diagnostics)
    prompt = augment_prompt_with_patient_recent_queries(prompt)

    result = await agent.run(prompt)
    return result.output


def print_diagnostics(diagnostics: List[Diagnostic]):
    print(f"\n📚 Generated diagnostics:")
    [print(f"  - {d.title}: {d.definition}") for d in diagnostics]


CURRENT_DIR = Path(__file__).parent 
DIAGNOSTICS_PATH = CURRENT_DIR / "diagnostics.md"

async def generate_patient_diagnostics() -> tuple[str, List[Diagnostic]]:
    from rich.console import Console

    console = Console()
    with console.status("[bold green]Warming up the system...", spinner="dots"):
        collection = store_diagnostics_in_vector_database(str(DIAGNOSTICS_PATH))

    while True:
        query = input("😷 Please explain your symptoms: ")
        if query:
            with console.status("[bold green]Generating diagnostics...", spinner="dots"):
                diagnostics = await answer_query(query, collection)
            store_patient_query(query)
            print_diagnostics(diagnostics)
            return (query, diagnostics)
        else:
            print("Invalid input. Please enter some valid symptoms.")