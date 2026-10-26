# Doctor Advisor

Helps an insured patient go from a description of their symptoms to a suitable in-network doctor and an appointment with them.

## Language

### People

**Patient**:
A person with medical insurance who describes their symptoms and is recommended doctors.
_Avoid_: User, client, customer

**Doctor**:
A medical professional with a single speciality who belongs to the insurer's network.
_Avoid_: Physician, provider

### Insurance

**Insurer**:
The single insurance company that owns Doctor Advisor. Every patient holds a policy with it.
_Avoid_: Insurance provider, carrier

**Network**:
The set of doctors covered by the insurer.
_Avoid_: Insurance directory, provider list

**Hospital**:
A healthcare institution the insurer has a business relationship with, where network doctors work. Each hospital runs its own Appointment Booking Service.
_Avoid_: Clinic, centre, facility

**Affiliation**:
A doctor's working arrangement with one hospital. A doctor may have several, and each hospital knows the doctor by its own local reference.
_Avoid_: Practice, posting, location

**Speciality**:
The medical field a doctor practises. Every condition is referred to exactly one speciality.
_Avoid_: Specialty, department

### Triage

**Symptom Description**:
The patient's opening free-text account of how they feel, which starts an intake.
_Avoid_: Query, question, prompt

**Intake**:
One exchange in which a patient gives a symptom description and answers a limited number of clarifying questions. It ends in candidate conditions, an emergency stop, or closure for being out of scope.
_Avoid_: Conversation, chat, session, consultation

**Clarifying Question**:
A closed question asked during an intake, either to tell candidate conditions apart or to confirm or rule out a red flag.
_Avoid_: Follow-up, prompt

**Condition**:
An entry in the medical knowledge base, with a definition, its common and occasional findings, an urgency, and the one speciality it is referred to.
_Avoid_: Diagnostic, diagnosis, illness, disease

**Candidate Condition**:
A condition proposed as possibly matching a patient's symptom description. It is never a diagnosis.
_Avoid_: Diagnostic, diagnosis, result

**Finding**:
A single sign or symptom the patient reports, recognisable through its lay phrasings. It is defined once and shared by the conditions and red flags that involve it.
_Avoid_: Sign, indicator, keyword

**Red Flag**:
One or more alternative combinations of findings, any of which may indicate the same medical emergency, so the patient is urged to seek emergency care. It is defined once and may be referenced by any number of conditions. One referenced by none is a general red flag.
_Avoid_: Alert, warning, emergency symptom

**Near Miss**:
A red flag with one of its combinations missing exactly one finding in an intake, which must be resolved by a clarifying question.
_Avoid_: Partial match, suspected red flag

**Lockout**:
A temporary ban on starting intakes, applied to a patient whose intakes have been repeatedly closed as unrelated to health.
_Avoid_: Ban, block, suspension

**Red Flag Check**:
The step that decides, alongside triage, whether a symptom description shows any red flag.
_Avoid_: Emergency screening, safety check

### Booking

**Appointment Booking Service**:
A hospital's external system that owns the agendas of the doctors working there. It is the only authority on which slots are free or booked.
_Avoid_: Calendar, scheduler

**Slot**:
A time interval in a doctor's agenda that a patient can book.
_Avoid_: Time slot, availability

**Appointment**:
A slot booked by a patient with a doctor.
_Avoid_: Booking, reservation, visit

**Visit Reason**:
A short summary of the patient's symptom description and candidate conditions, attached to an appointment for the doctor to read.
_Avoid_: Appointment request, email, notes
