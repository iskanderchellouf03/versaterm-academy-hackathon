# Research: KB Audience & Tone Selection

## R1 — Audience Context Injection

**Decision**: Append an audience description to the system
prompt. Each audience option maps to a brief instruction
block:
- Internal: "Write for internal employees. Use company
  jargon, reference internal tools, assume product knowledge."
- External: "Write for external customers. Use plain
  language, avoid internal jargon, provide full context."
- Support: "Write for support agents. Use troubleshooting
  structure, step-by-step resolution, reference ticket
  workflows and escalation."

**Rationale**: Same pattern as 005 (platform context for 004).
Explicit audience descriptions produce consistently
differentiated output. Brief descriptions keep token count
low.

**Alternatives considered**:
- Audience-specific prompt templates: Duplicates the full
  prompt per audience. Rejected — context injection is
  simpler and DRY.
- Few-shot examples per audience: Increases token count 3x.
  Rejected for MVP.
- RAG with audience style guides: Over-engineering. Rejected.

## R2 — Tone Context Injection

**Decision**: Append tone instructions alongside audience:
- Formal: "Use professional third-person voice. Passive
  voice is acceptable. No contractions, no colloquialisms."
- Conversational: "Use friendly second-person voice ('you').
  Contractions OK. Approachable and warm."
- Concise: "Minimize prose. Use bullet lists, imperative
  voice, short sentences. Quick-reference style."

**Rationale**: Tone instructions are orthogonal to audience.
Both are appended to the same prompt section, so the LLM
processes both simultaneously. All 9 combinations (3×3)
produce meaningfully different outputs.

**Alternatives considered**:
- Tone as a system message parameter: The `openai` API
  doesn't have a tone parameter. Prompt injection is the
  only option. Accepted.
- Post-processing tone transformation: Rewriting after
  generation doubles LLM calls. Rejected.

## R3 — UI Controls

**Decision**: Use `st.selectbox()` for both audience and tone.
Audience defaults to "Internal", tone defaults to "Formal".
Placed alongside the text input, above the "Generate" button.

**Rationale**: Same UI pattern as 005 (selectbox for single-
selection from fixed list). Consistent UX across modules.
Both widgets persist in session state automatically.

**Alternatives considered**:
- `st.radio()`: Takes more vertical space for 3 options.
  Selectbox is more compact. Rejected.
- Combined single dropdown (e.g., "Internal-Formal"):
  9 options is too many for a flat list. Two separate
  selectors is clearer. Rejected.

## R4 — Override Input Tone

**Decision**: The prompt explicitly instructs the LLM to use
the selected tone regardless of input style: "Regardless of
the input text's tone or style, the output MUST use the
selected tone." This satisfies FR-010.

**Rationale**: Simple prompt instruction. The LLM respects
explicit override instructions reliably.

**Alternatives considered**:
- Pre-processing to strip input tone: Impossible without
  NLP analysis. Over-engineering. Rejected.
