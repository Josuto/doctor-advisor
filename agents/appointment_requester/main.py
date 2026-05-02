from typing import List
from pydantic_ai import Agent

from agents.shared.models import Doctor

from .utils import list_doctors, select_doctor


system_prompt = f""""
    You are a helpful assistant that sends appointment requests to doctors.

    ### Role and behaviour:
    - You are a part of a multi-agent system that helps patients get the care they need.
    - Given the patient's data and original query as well as a doctor selected by the patient, 
    you will create an email appointment request to the doctor.
    - Do not write the email on behalf of the patient, just provide the content that should be 
    sent in the email.
    - Provide a clear, accurate answer content for the email.
    - Do not fabricate any data; only use the provided patient data and query.
    """

# Create an agent using Claude model
agent = Agent(
    model="anthropic:claude-sonnet-4-5",
    system_prompt=system_prompt,
    output_type=str
)

def print_email_template(template: str):
    print("\n📧 Generated email content:\n")
    print(80 * "-")
    print(template)
    print(80 * "-")


def select_doctor_from(doctors: List[Doctor]):
    """Display a list of doctors to the patient and enable them to pick one"""
    list_doctors(doctors)
    return select_doctor(doctors)


async def create_appointment_request_email(query: str, doctor: Doctor):
    """Create an email template that the patient can use to send an appointment request to the selected doctor"""
    from rich.console import Console

    prompt = f"""
        Create an email appointment request to {doctor.name} ({doctor.email}) with the following details:
        - Use a placeholder for the patient's name ([PATIENT_NAME]) as well as for the patient's phone number ([PATIENT_PHONE_NUMBER]).
        - Add a note asking the patient to replace the placeholders with their actual name and phone number before sending the email.
        - Patient query: {query}
    """

    console = Console()
    with console.status("[bold green]Producing medical appointment email template...", spinner="dots"):
        result = await agent.run(prompt)
    print_email_template(result.output)
    return result.output