# Booking goes through one gateway with an adapter per hospital, and hospitals own agenda consistency

Doctors may have affiliations with several hospitals, and each hospital runs its own Appointment Booking Service with its own HTTP API, which knows doctors by its own local reference. Doctor Advisor talks to all of them through a single `BookingGateway` interface (list slots, book with an idempotency key, cancel), with one adapter per hospital that translates the insurer's doctor code into the hospital's local reference. We chose HTTP over MCP because booking is deterministic code that no LLM calls. Doctor Advisor deliberately does not reconcile agendas across hospitals: each booking service is the only authority on its slots, and avoiding overlapping schedules is the hospitals' responsibility.

## Consequences

- Slot listing queries all of a doctor's hospitals in parallel, each with a timeout, up to 2 retries and backoff. Hospitals that fail are silently left out, and doctors with no slots are hidden.
- A booking conflict (409) means slots are fetched again and the new ones offered.
- The simulated hospital APIs deliberately differ in shape, to prove the abstraction works.
