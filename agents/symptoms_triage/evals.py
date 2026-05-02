import asyncio
import os
from typing import List
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import EqualsExpected, LLMJudge
from pydantic_evals.evaluators.llm_as_a_judge import set_default_judge_model

from agents.shared.models import Diagnostic
from .main import answer_query
from .utils import store_diagnostics_in_vector_database


set_default_judge_model("anthropic:claude-sonnet-4-6")


DIAGNOSTICS_FILE = os.path.join(os.path.dirname(__file__), "diagnostics.md")
collection = store_diagnostics_in_vector_database(DIAGNOSTICS_FILE)


async def sut(query: str) -> List[Diagnostic]:
    return await answer_query(query, collection)


dataset: Dataset[str, List[Diagnostic], None] = Dataset(
    name="symptoms_triage_evals",
    cases=[
        # Happy path: Known symptom.
        # Fatigue is listed under Influenza in diagnostics.md.
        Case(
            name="happy_path_known_symptom_fever",
            inputs="Which illness causes fatigue?",
            evaluators=[
                LLMJudge(
                    rubric="The output should contain Influenza as a diagnostic that causes fatigue, " \
                    "with a definition describing it as a viral infection of the respiratory system.",
                    include_input=True
                ),
            ],
        ),

        # Happy path: Shared symptom across multiple diagnostics.
        # Dizziness appears in both Dehydration and Motion Sickness.
        Case(
            name="happy_path_shared_symptom_dizziness",
            inputs="Which illness causes dizziness?",
            evaluators=[
                LLMJudge(
                    rubric="The output should contain both Dehydration and Motion Sickness as diagnostics " \
                    "that cause dizziness, with correct definitions mentioning fluid loss and inner ear disturbance respectively.",
                    include_input=True
                ),
            ],
        ),

        # Happy path: Two symptoms that together narrow the result to a single diagnostic.
        # Throbbing pain AND sensitivity to light both belong exclusively to Migraine
        # in the knowledge base, so the combined query should converge on one result.
        Case(
            name="happy_path_multiple_symptoms_single_diagnostic",
            inputs="Which illness causes throbbing pain and sensitivity to light?",
            evaluators=[
                LLMJudge(
                    rubric="The output should contain Migraine as the diagnostic that causes both throbbing " \
                    "pain and sensitivity to light, with a definition describing it as a neurological condition with headaches.",
                    include_input=True
                ),
            ],
        ),

        # Happy path: Case-insensitive / noisy query.
        # The pipeline lowercases queries before embedding so an all-caps question should
        # surface the expected result.
        Case(
            name="happy_path_case_insensitive_query",
            inputs="WHICH ILLNESS CAUSES FEVER?",
            evaluators=[
                LLMJudge(
                    rubric="The output should contain Influenza as a diagnostic that causes fever and muscle aches, " \
                    "with a definition describing it as a viral respiratory infection, demonstrating case-insensitive query handling.",
                    include_input=True
                ),
            ],
        ),

        # Corner case: Nonexistent symptom.
        # "Purple skin discoloration" does not appear in diagnostics.md, so the agent
        # must return an empty list. 
        Case(
            name="corner_case_nonexistent_symptom",
            inputs="Which illness causes purple skin discoloration?",
            expected_output=[],
            evaluators=[
                EqualsExpected(),
            ],
        ),
    ],
)


async def main():
    report = await dataset.evaluate(sut)
    report.print(include_input=True, include_output=True)


if __name__ == "__main__":
    asyncio.run(main())
