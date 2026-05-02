import asyncio
from agents.symptoms_triage import generate_patient_diagnostics
from agents.doctor_fetcher import fetch_doctors_from
from agents.appointment_requester import select_doctor_from, create_appointment_request_email
from observability import init_telemetry

init_telemetry(project_name="doctor-advisor")

async def main():
  query, diagnostics = await generate_patient_diagnostics()
  if diagnostics and len(diagnostics) > 0:
    doctors = await fetch_doctors_from(diagnostics)
    if doctors and len(doctors) > 0:
      doctor = select_doctor_from(doctors)
      await create_appointment_request_email(query, doctor)
  else:
    print("Sorry, I couldn't generate any diagnostics based on your query. " \
          "Please try asking a different question or provide more information.")


if __name__ == "__main__":
  asyncio.run(main())
