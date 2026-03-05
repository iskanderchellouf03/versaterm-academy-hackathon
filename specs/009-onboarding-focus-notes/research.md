# Research: Onboarding Focus Notes

## R1 — Focus Notes Prompt Injection

**Decision**: Append focus notes as a "Priority Focus Areas"
section in the system prompt: "The manager has specified the
following priority focus areas. Emphasize these topics by:
(1) frontloading related activities in Week 1, (2) including
focus-specific key terms, (3) adding at least one checkpoint
per focus area. Focus areas: {notes}"

**Rationale**: Same pattern as 005 (platform context) and
007 (audience/tone). Explicit instructions on HOW to use
the focus notes produce consistent emphasis. The LLM handles
multi-topic notes naturally.

**Alternatives considered**:
- Parse focus notes into structured topics (NLP extraction):
  Over-engineering. The LLM interprets free text well.
  Rejected per Simplicity First.
- Separate prompt per focus area: Multiplies API calls.
  Rejected.
- Predefined focus area checkboxes: Limits flexibility.
  Free text is more powerful. Rejected per spec.

## R2 — Empty Focus Notes Handling

**Decision**: If focus notes are empty, omit the "Priority
Focus Areas" section from the prompt entirely. This ensures
baseline 008 behavior is unchanged (FR-008).

**Rationale**: The cleanest approach. No conditional logic
in the LLM's output — the focus section simply isn't there.
The prompt builder checks `if focus_notes.strip():` before
appending.

**Alternatives considered**:
- Always include the section with "No specific focus areas":
  Adds unnecessary tokens. May confuse the LLM. Rejected.

## R3 — UI Control

**Decision**: `st.text_area()` with label "Focus notes
(optional)", max 1,000 characters, placeholder text: "e.g.,
safety-critical workflows, compliance reporting, mobile
operations". Placed below the level selector, above the
"Generate Plan" button.

**Rationale**: `st.text_area()` allows multi-line input,
which is natural for listing multiple focus areas. The
placeholder provides examples without requiring documentation.
"(optional)" in the label makes it clear the field can be
skipped.

**Alternatives considered**:
- `st.text_input()`: Single line limits multi-topic input.
  Rejected.
- Checkboxes from a predefined list: Limits flexibility.
  Rejected per spec.
- Tags/chips input: Requires a custom component. Rejected
  per Simplicity First.

## R4 — Character Limit Enforcement

**Decision**: Use `max_chars=1000` parameter on
`st.text_area()`. Streamlit enforces this client-side. Also
validate server-side with `len()` as defense-in-depth.

**Rationale**: `st.text_area(max_chars=N)` is the simplest
enforcement — built into Streamlit, no additional code.
Server-side check is a safety net.

**Alternatives considered**:
- No limit: Risk of very long focus notes inflating prompt
  tokens. Rejected.
- Word count instead of character count: Less intuitive for
  users. Rejected.
