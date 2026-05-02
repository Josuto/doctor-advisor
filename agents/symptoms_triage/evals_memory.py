import asyncio
import os
from dataclasses import dataclass
from typing import List
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import Evaluator, EvaluatorContext

from agents.shared.models import Diagnostic
from .main import answer_query
from .utils import store_diagnostics_in_vector_database, memory, store_patient_query

DIAGNOSTICS_FILE = os.path.join(os.path.dirname(__file__), "diagnostics.md")
collection = store_diagnostics_in_vector_database(DIAGNOSTICS_FILE)


@dataclass
class DiagnosticFieldsMatch(Evaluator[str, List[Diagnostic]]):
    """Assert that every expected Diagnostic appears in the output by matching id, definition, 
    and symptoms. Returns True only when every expected diagnostic is accounted for.
    """
    expected: List[Diagnostic]

    def evaluate(self, ctx: EvaluatorContext[str, List[Diagnostic]]) -> bool:
        for expected_diag in self.expected:
            match_found = any(
                actual.id == expected_diag.id
                and actual.title == expected_diag.title
                and actual.definition == expected_diag.definition
                and actual.symptoms == expected_diag.symptoms
                for actual in ctx.output
            )
            if not match_found:
                return False
        return True


async def sut_with_memory_migraine(query: str) -> List[Diagnostic]:
    memory.queries = []
    store_patient_query("I have a headache and sensitivity to light")
    return await answer_query(query, collection)


async def sut_with_memory_unrelated(query: str) -> List[Diagnostic]:
    memory.queries = []
    store_patient_query("I have fever and muscle aches")
    return await answer_query(query, collection)


memory_dataset_migraine: Dataset[str, List[Diagnostic], None] = Dataset(
    name="symptoms_triage_memory_evals_migraine",
    cases=[
        # Happy path: Agent works correctly with memory context (migraine follow-up).
        # Seed with a past query about headache and light sensitivity (migraine symptoms),
        # then query about throbbing pain (also a migraine symptom). The agent should
        # correctly identify migraine even with the enriched memory context in the prompt.
        Case(
            name="happy_path_with_memory_context_migraine",
            inputs="Which illness causes throbbing pain?",
            evaluators=[
                DiagnosticFieldsMatch(expected=[
                    Diagnostic(
                        id="migraine_chunk_0",
                        title="Migraine",
                        definition=(
                            "A neurological condition that can cause multiple symptoms, most notably "
                            "a moderate to severe throbbing headache that is often localized to one side."
                        ),
                        symptoms=[
                            "Throbbing pain: Intense pulsing sensations, usually on one side of the head.",
                            "Sensitivity to light: Discomfort or pain caused by bright lights or screens.",
                        ],
                    )
                ]),
            ],
        ),
    ],
)


memory_dataset_unrelated: Dataset[str, List[Diagnostic], None] = Dataset(
    name="symptoms_triage_memory_evals_unrelated",
    cases=[
        # Happy path: Agent handles memory context with unrelated follow-up query.
        # Seed with influenza symptoms (fever and muscle aches), then query about dizziness.
        # Dizziness is not a symptom of influenza, so the agent should correctly identify
        # the dizziness-related conditions (Dehydration and Motion Sickness), demonstrating
        # that memory context doesn't override the new query semantics.
        Case(
            name="happy_path_with_memory_context_unrelated_query",
            inputs="Which illness causes dizziness?",
            evaluators=[
                DiagnosticFieldsMatch(expected=[
                    Diagnostic(
                        id="dehydration_chunk_0",
                        title="Dehydration",
                        definition=(
                            "Occurs when you use or lose more fluid than you take in, and your body "
                            "doesn't have enough water and other fluids to carry out its normal functions."
                        ),
                        symptoms=[
                            "Extreme thirst: A strong, persistent urge to drink fluids.",
                            "Dark-colored urine: A sign that the body is attempting to conserve water.",
                            "Dizziness: A feeling of lightheadedness or being off-balance.",
                        ],
                    ),
                    Diagnostic(
                        id="motion_sickness_chunk_0",
                        title="Motion Sickness",
                        definition=(
                            "A common disturbance of the inner ear that is caused by repeated motion, "
                            "such as from the swell of the sea, the movement of a car, or the motion of a plane."
                        ),
                        symptoms=[
                            "Dizziness: A sense of spinning or unsteadiness while moving.",
                            "Nausea: Feeling sick to the stomach, often leading to vomiting.",
                        ],
                    ),
                ]),
            ],
        ),
    ],
)


async def main():
    print("=" * 80)
    print("Running memory-specific evaluations for symptoms_triage agent")
    print("=" * 80)

    migraine_report = await memory_dataset_migraine.evaluate(sut_with_memory_migraine)
    migraine_report.print(include_input=True, include_output=True)

    print("\n" + "=" * 80 + "\n")

    unrelated_report = await memory_dataset_unrelated.evaluate(sut_with_memory_unrelated)
    unrelated_report.print(include_input=True, include_output=True)


if __name__ == "__main__":
    asyncio.run(main())
