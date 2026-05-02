import asyncio
from dataclasses import dataclass
from typing import List
from unittest.mock import patch, AsyncMock

from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import LLMJudge, Evaluator, EvaluatorContext
from pydantic_evals.evaluators.llm_as_a_judge import set_default_judge_model

from agents.shared.models import Diagnostic, Doctor, SPECIALITY

set_default_judge_model("anthropic:claude-sonnet-4-6")


@dataclass
class HappyPathInput:
    """Integration test input: symptom query, expected diagnostics, available doctors, selected doctor index"""
    symptom_query: str
    mock_diagnostics: List[Diagnostic]
    available_doctors: List[Doctor]
    selected_doctor_index: int


@dataclass
class HappyPathOutput:
    """Integration test output: diagnostics, selected doctor, and appointment email"""
    diagnostics: List[Diagnostic]
    selected_doctor: Doctor
    appointment_email: str


async def sut(input: HappyPathInput) -> HappyPathOutput:
    """System under test: orchestrates the happy path workflow"""
    from agents.symptoms_triage.main import answer_query
    from agents.doctor_selector.main import fetch_doctors_from
    from agents.appointment_requester.main import select_doctor_from, create_appointment_request_email
    from agents.symptoms_triage.utils import store_diagnostics_in_vector_database

    with patch("builtins.input") as mock_input, \
         patch("agents.symptoms_triage.main.answer_query", new_callable=AsyncMock) as mock_answer, \
         patch("agents.doctor_selector.main.fetch_doctors_from", new_callable=AsyncMock) as mock_fetch, \
         patch("agents.appointment_requester.main.select_doctor", return_value=input.available_doctors[input.selected_doctor_index]):

        mock_input.return_value = input.symptom_query
        mock_answer.return_value = input.mock_diagnostics
        mock_fetch.return_value = input.available_doctors

        from agents.symptoms_triage.main import generate_patient_diagnostics

        query, diagnostics = await generate_patient_diagnostics()
        doctors = await fetch_doctors_from(diagnostics)
        selected_doctor = select_doctor_from(doctors)
        appointment_email = await create_appointment_request_email(query, selected_doctor)

        return HappyPathOutput(
            diagnostics=diagnostics,
            selected_doctor=selected_doctor,
            appointment_email=appointment_email,
        )


class DiagnosticsNotEmpty(Evaluator[HappyPathInput, HappyPathOutput]):
    """Verify that diagnostics were generated"""
    def evaluate(self, ctx: EvaluatorContext[HappyPathInput, HappyPathOutput]) -> bool:
        return len(ctx.output.diagnostics) > 0


class SelectedDoctorMatchesInput(Evaluator[HappyPathInput, HappyPathOutput]):
    """Verify that the correct doctor was selected"""
    def evaluate(self, ctx: EvaluatorContext[HappyPathInput, HappyPathOutput]) -> bool:
        expected_doctor = ctx.inputs.available_doctors[ctx.inputs.selected_doctor_index]
        return ctx.output.selected_doctor == expected_doctor


dataset: Dataset[HappyPathInput, HappyPathOutput, None] = Dataset(
    name="main_happy_path_integration",
    cases=[
        # Happy path: Single symptom → diagnostics → doctor selection → appointment email
        Case(
            name="happy_path_headache_workflow",
            inputs=HappyPathInput(
                symptom_query="I have a persistent headache with sensitivity to light.",
                mock_diagnostics=[
                    Diagnostic(
                        id="migraine_1",
                        title="Migraine",
                        definition="A neurological condition characterized by intense throbbing headaches.",
                        symptoms=["Throbbing pain", "Sensitivity to light", "Nausea"],
                    )
                ],
                available_doctors=[
                    Doctor(
                        name="Dr. Emily Chen",
                        speciality=SPECIALITY.NEUROLOGIST,
                        email="emily.chen@wellness-clinic.com",
                    )
                ],
                selected_doctor_index=0,
            ),
            evaluators=[
                DiagnosticsNotEmpty(),
                SelectedDoctorMatchesInput(),
                LLMJudge(
                    rubric=(
                        "The appointment email must address Dr. Emily Chen, reference the patient's headache "
                        "and light sensitivity complaint, include placeholders for patient name and phone number, "
                        "and not be written on behalf of the patient."
                    ),
                    include_input=True,
                ),
            ],
        ),

        # Happy path: Multiple diagnostics → doctor from matching speciality selected
        Case(
            name="happy_path_multiple_diagnostics_single_doctor_selection",
            inputs=HappyPathInput(
                symptom_query="I have eye irritation and redness.",
                mock_diagnostics=[
                    Diagnostic(
                        id="conjunctivitis_1",
                        title="Conjunctivitis",
                        definition="Inflammation of the conjunctiva causing redness and irritation.",
                        symptoms=["Eye irritation", "Redness", "Watery eyes"],
                    ),
                    Diagnostic(
                        id="allergic_reaction_1",
                        title="Allergic Reaction",
                        definition="An immune response to an allergen causing ocular symptoms.",
                        symptoms=["Eye irritation", "Itching", "Redness"],
                    ),
                ],
                available_doctors=[
                    Doctor(
                        name="Dr. Sarah Williams",
                        speciality=SPECIALITY.OPHTHALMOLOGY,
                        email="sarah.williams@eye-clinic.com",
                    ),
                    Doctor(
                        name="Dr. Michelle Brown",
                        speciality=SPECIALITY.ALLERGIST,
                        email="michelle.brown@allergy-center.com",
                    ),
                ],
                selected_doctor_index=0,
            ),
            evaluators=[
                DiagnosticsNotEmpty(),
                SelectedDoctorMatchesInput(),
                LLMJudge(
                    rubric=(
                        "The appointment email must address Dr. Sarah Williams, reference the patient's "
                        "eye irritation and redness symptoms, include placeholders for patient name and phone, "
                        "and provide professional email content for the patient to send to the doctor."
                    ),
                    include_input=True,
                ),
            ],
        ),

        # Happy path: Vague symptom produces email with focused request (no fabrication)
        Case(
            name="happy_path_vague_symptom_focused_email",
            inputs=HappyPathInput(
                symptom_query="I don't feel well.",
                mock_diagnostics=[
                    Diagnostic(
                        id="general_malaise_1",
                        title="General Malaise",
                        definition="A general feeling of unwellness or discomfort without specific localized symptoms.",
                        symptoms=["Fatigue", "General discomfort"],
                    )
                ],
                available_doctors=[
                    Doctor(
                        name="Dr. Fatima Panisello",
                        speciality=SPECIALITY.GENERAL_PRACTITIONER,
                        email="fatima.panisello@new-hospital.com",
                    )
                ],
                selected_doctor_index=0,
            ),
            evaluators=[
                DiagnosticsNotEmpty(),
                SelectedDoctorMatchesInput(),
                LLMJudge(
                    rubric=(
                        "The appointment email must address Dr. Fatima Panisello, reflect the patient's "
                        "vague complaint without fabricating specific diagnoses or symptoms beyond 'not feeling well', "
                        "include placeholders for patient name and phone, and be formatted as content for "
                        "the patient to send."
                    ),
                    include_input=True,
                ),
            ],
        ),
    ],
)


async def main():
    report = await dataset.evaluate(sut)
    report.print(include_input=True, include_output=True)


if __name__ == "__main__":
    asyncio.run(main())
