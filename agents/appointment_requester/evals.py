import asyncio
from dataclasses import dataclass
from typing import List
from unittest.mock import patch

from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import LLMJudge
from pydantic_evals.evaluators.llm_as_a_judge import set_default_judge_model

from agents.shared.models import Doctor, SPECIALITY
from agents.appointment_requester.main import select_doctor_from, create_appointment_request_email

set_default_judge_model("anthropic:claude-sonnet-4-6")


@dataclass
class AppointmentInput:
    query: str
    doctors: List[Doctor]
    selected_doctor_index: int


async def sut(input: AppointmentInput) -> str:
    selected_doctor = input.doctors[input.selected_doctor_index]

    with patch("agents.appointment_requester.main.select_doctor", return_value=selected_doctor):
        doctor = select_doctor_from(input.doctors)
        return await create_appointment_request_email(input.query, doctor)


dataset: Dataset[AppointmentInput, str, None] = Dataset(
    name="appointment_requester_evals",
    cases=[
        # Happy path: all required fields (doctor name, patient name, phone, query)
        # must appear in the generated email content.
        Case(
            name="happy_path_email_contains_doctor_and_patient_info",
            inputs=AppointmentInput(
                query="I have been experiencing persistent shortness of breath and chronic cough.",
                doctors=[
                    Doctor(
                        name="Dr. John Smith",
                        speciality=SPECIALITY.NEUMOLOGY,
                        email="john.smith@hospital.com",
                    )
                ],
                selected_doctor_index=0,
            ),
            evaluators=[
                LLMJudge(
                    rubric=(
                        "The email must include: the doctor's name 'Dr. John Smith' and a reference to the patient's "
                        "symptoms (shortness of breath and chronic cough). It must not be written on behalf of the "
                        "patient — it should provide email content for the patient to send, not an already-sent message."
                    ),
                    include_input=True,
                ),
            ],
        ),

        # Happy path: query-specific content must appear in the email without the
        # agent fabricating unrelated medical details not present in the input.
        Case(
            name="happy_path_email_reflects_patient_query_without_fabrication",
            inputs=AppointmentInput(
                query="I have been experiencing stomach pain and diarrhea for three days.",
                doctors=[
                    Doctor(
                        name="Dr. Robert Johnson",
                        speciality=SPECIALITY.DIGESTIVE,
                        email="robert.johnson@hospital.com",
                    )
                ],
                selected_doctor_index=0,
            ),
            evaluators=[
                LLMJudge(
                    rubric=(
                        "The email must include the doctor's name 'Dr. Robert Johnson' and accurately reflect "
                        "the patient's complaint about stomach pain and diarrhea. It must NOT introduce medical "
                        "diagnoses or symptoms not mentioned in the query. It must not be written on behalf of "
                        "the patient — it should provide email content for the patient to send, not an "
                        "already-sent message."
                    ),
                    include_input=True,
                ),
            ],
        ),

        # Happy path: when multiple doctors are available, the email must address the
        # doctor selected by the patient, not the first one in the list.
        Case(
            name="happy_path_correct_doctor_addressed_from_list",
            inputs=AppointmentInput(
                query="I need a consultation about a persistent eye irritation.",
                doctors=[
                    Doctor(
                        name="Dr. John Smith",
                        speciality=SPECIALITY.NEUMOLOGY,
                        email="john.smith@hospital.com",
                    ),
                    Doctor(
                        name="Dr. Jane Doe",
                        speciality=SPECIALITY.NEUMOLOGY,
                        email="jane.doe@hospital.com",
                    ),
                ],
                selected_doctor_index=1,
            ),
            evaluators=[
                LLMJudge(
                    rubric=(
                        "The email must be addressed to 'Dr. Jane Doe' (the second doctor), to 'Dr. John Smith'. "
                        "It must not be written on behalf of the patient — it should provide email content for "
                        "the patient to send, not an already-sent message."
                    ),
                    include_input=True,
                ),
            ],
        ),

        # Corner case: a vague query must produce an email that sticks to the
        # provided data only — the agent must not invent medical details.
        Case(
            name="corner_case_no_fabricated_medical_content",
            inputs=AppointmentInput(
                query="I would like to schedule a general consultation.",
                doctors=[
                    Doctor(
                        name="Dr. Jane Doe",
                        speciality=SPECIALITY.NEUMOLOGY,
                        email="jane.doe@hospital.com",
                    )
                ],
                selected_doctor_index=0,
            ),
            evaluators=[
                LLMJudge(
                    rubric=(
                        "The email must include the doctor's name 'Dr. Jane Doe'. It must NOT fabricate any "
                        "symptoms, diagnoses, or medical details beyond what was stated in the query (a general "
                        "consultation request). It must not be written on behalf of the patient — it should "
                        "provide email content for the patient to send, not an already-sent message."
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
