# The doctor-matching agent calls the insurer's MCP server, which returns doctor codes only

The insurer exposes its network through an MCP server shared by several insurer services (read tools `list_doctors_by_speciality`, `list_doctors_by_hospital`, `get_doctor`; write tools to add, update and remove doctors). In Doctor Advisor, an agent run that follows triage calls `list_doctors_by_speciality` for each speciality of the candidate conditions. The tool returns only `{doctor_code, hospital_codes}`, so no doctor PII ever reaches the model. Plain code then resolves the codes with `get_doctor` (names, affiliations, local doctor references) for display and booking. We chose this over having plain code call MCP directly, because an LLM actually discovering and calling tools is the realistic use of MCP. Opaque codes keep privacy intact, and validators limit the model's freedom.

## Consequences

- The agent's MCP connection is filtered to read-only tools, and `get_doctor` is never exposed to the model.
- Output validators reject specialities that differ from the conditions file and doctor codes that didn't come from a tool result in the same run. Evals assert the set of tool calls made.
