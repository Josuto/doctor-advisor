from typing import List

from agents.shared.models import Doctor

def list_doctors(doctors: List[Doctor]):
  print("\n🚑 Available doctors:")
  for i, doctor in enumerate(doctors, start=1):
    print(f"{i}. {doctor.name} ({doctor.speciality.value})")


def select_doctor(doctors: List[Doctor]) -> Doctor:
  while True:
    try:
      choice = int(input('\nSelect a doctor: '))
      if 1 <= choice <= len(doctors):
        return doctors[choice - 1]
      else:
        print("Invalid choice. Please enter a valid number.")
    except ValueError:
      print("Invalid input. Please enter a number.")
