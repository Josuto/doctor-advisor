from pydantic import BaseModel, EmailStr as Email
from typing import List, Optional
from enum import Enum

class Diagnostic(BaseModel):
    id: str
    title: str
    definition: str
    symptoms: List[str]

class SPECIALITY(Enum):
  NEUMOLOGY = "neumology"
  DIGESTIVE = "digestive"
  OPHTHALMOLOGY = "ophthalmology"
  ALLERGIST = "allergist"
  CARDIOLOGIST = "cardiologist"
  NEUROLOGIST = "neurologist"
  GENERAL_PRACTITIONER ="general_practitioner"

class Doctor(BaseModel):
  name: str
  speciality: SPECIALITY
  email: Email
