import asyncio
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List
from unittest.mock import patch

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import Evaluator, EvaluatorContext, EqualsExpected

from agents.shared.models import Diagnostic, Doctor, SPECIALITY
from .main import fetch_doctors_from, system_prompt

_ROOT_DIR = str(Path(__file__).parents[2])
_mock_server_script = str(Path(__file__).parent / "mock_insurance_server.py")

_mock_server = MCPServerStdio(
    "uv",
    args=["run", "python", _mock_server_script],
    env={**os.environ, "PYTHONPATH": _ROOT_DIR},
)

_mock_agent = Agent(
    model="anthropic:claude-sonnet-4-5",
    system_prompt=system_prompt,
    toolsets=[_mock_server],
    output_type=List[Doctor],
)


async def sut(diagnostics: List[Diagnostic]) -> List[Doctor]:
    with patch("builtins.input", return_value="y"), \
         patch("agents.doctor_fetcher.main.agent", _mock_agent):
        return await fetch_doctors_from(diagnostics)


@dataclass
class DoctorFieldsMatch(Evaluator[List[Diagnostic], List[Doctor]]):
    """Assert that every expected Doctor appears in the output by matching name,
    speciality, and email. Returns True only when every expected doctor is found.
    """
    expected: List[Doctor]

    def evaluate(self, ctx: EvaluatorContext[List[Diagnostic], List[Doctor]]) -> bool:
        for expected_doctor in self.expected:
            match_found = any(
                actual.name == expected_doctor.name
                and actual.speciality == expected_doctor.speciality
                and actual.email == expected_doctor.email
                for actual in ctx.output
            )
            if not match_found:
                return False
        return True


dataset: Dataset[List[Diagnostic], List[Doctor], None] = Dataset(
    name="doctor_fetcher_evals",
    cases=[
        # Happy path: A respiratory diagnostic should surface both neumology doctors.
        # Both Dr. John Smith and Dr. Jane Doe specialise in NEUMOLOGY.
        Case(
            name="happy_path_neumology_diagnostic",
            inputs=[
                Diagnostic(
                    id="influenza_chunk_0",
                    title="Influenza",
                    definition=(
                        "A viral infection that attacks your respiratory system — "
                        "your nose, throat, and lungs."
                    ),
                    symptoms=["Fever", "Cough", "Shortness of breath"],
                )
            ],
            evaluators=[
                DoctorFieldsMatch(expected=[
                    Doctor(
                        name="Dr. John Smith",
                        speciality=SPECIALITY.NEUMOLOGY,
                        email="john.smith@city-hospital.com",
                    ),
                    Doctor(
                        name="Dr. Jane Doe",
                        speciality=SPECIALITY.NEUMOLOGY,
                        email="jane.doe@metro-clinic.com",
                    ),
                ]),
            ],
        ),

        # Happy path: A digestive diagnostic should return only the digestive specialist.
        Case(
            name="happy_path_digestive_diagnostic",
            inputs=[
                Diagnostic(
                    id="gastroenteritis_chunk_0",
                    title="Gastroenteritis",
                    definition=(
                        "Inflammation of the stomach and intestines, typically "
                        "caused by a viral or bacterial infection."
                    ),
                    symptoms=["Diarrhea", "Vomiting", "Abdominal cramps"],
                )
            ],
            evaluators=[
                DoctorFieldsMatch(expected=[
                    Doctor(
                        name="Dr. Robert Johnson",
                        speciality=SPECIALITY.DIGESTIVE,
                        email="robert.johnson@central-hospital.com",
                    ),
                ]),
            ],
        ),

        # Happy path: Diagnostics spanning two specialities should return doctors from both.
        # Respiratory + digestive diagnostics → neumology + digestive doctors.
        Case(
            name="happy_path_multiple_specialities_both_matched",
            inputs=[
                Diagnostic(
                    id="influenza_chunk_0",
                    title="Influenza",
                    definition=(
                        "A viral infection that attacks your respiratory system — "
                        "your nose, throat, and lungs."
                    ),
                    symptoms=["Fever", "Cough"],
                ),
                Diagnostic(
                    id="gastroenteritis_chunk_0",
                    title="Gastroenteritis",
                    definition=(
                        "Inflammation of the stomach and intestines caused by infection."
                    ),
                    symptoms=["Diarrhea", "Vomiting"],
                ),
            ],
            evaluators=[
                DoctorFieldsMatch(expected=[
                    Doctor(
                        name="Dr. John Smith",
                        speciality=SPECIALITY.NEUMOLOGY,
                        email="john.smith@city-hospital.com",
                    ),
                    Doctor(
                        name="Dr. Robert Johnson",
                        speciality=SPECIALITY.DIGESTIVE,
                        email="robert.johnson@central-hospital.com",
                    ),
                ]),
            ],
        ),

        # Corner case: A diagnostic for a speciality not covered by any doctor (e.g. cardiology)
        # must return a list including at least one general practitioner.
        Case(
            name="corner_case_no_matching_speciality",
            inputs=[
                Diagnostic(
                    id="arrhythmia_chunk_0",
                    title="Arrhythmia",
                    definition=(
                        "An irregular heartbeat where the heart beats too fast, "
                        "too slow, or with an irregular rhythm."
                    ),
                    symptoms=["Palpitations", "Chest pain", "Fainting"],
                )
            ],
            evaluators=[
                DoctorFieldsMatch(expected=[
                    Doctor(
                        name="Dr. Fatima Panisello",
                        speciality=SPECIALITY.GENERAL_PRACTITIONER,
                        email="fatima.panisello@new-hospital.com",
                    ),
                ]),
            ],
        ),

        # Corner case: Insufficient diagnostic information must also produce an empty list.
        Case(
            name="corner_case_insufficient_diagnostic_information",
            inputs=[
                Diagnostic(
                    id="unknown_chunk_0",
                    title="Unknown condition",
                    definition="",
                    symptoms=[],
                )
            ],
            expected_output=[],
            evaluators=[EqualsExpected()],
        ),
    ],
)


async def main():
    report = await dataset.evaluate(
        sut, 
        max_concurrency=1 # Set max_concurrency to 1 to avoid issues with the mock server handling multiple requests simultaneously
    ) 
    report.print(include_input=True, include_output=True)


if __name__ == "__main__":
    asyncio.run(main())
