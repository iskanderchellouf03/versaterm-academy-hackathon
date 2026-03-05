# Research: KB Article Generator

## R1 — Prompt Design for KB Article Generation

**Decision**: Single system prompt instructing the LLM to
produce a KB article with four sections (Title, Summary,
Body, Tags). The prompt includes specific rules: title under
80 chars, summary 1-2 sentences, body with headings and
numbered steps for procedures, 3-7 tags. Formatting rules
appended via 014's `get_system_prompt("006")`.

**Rationale**: Same pattern as 004. One prompt, one LLM call.
The prompt explicitly describes what a "good" KB article
looks like: remove conversational filler, distill key
information, use numbered steps for procedures. The LLM
handles content transformation naturally.

**Alternatives considered**:
- Two-pass generation (first extract key points, then write
  article): Doubles latency and API cost. Rejected for MVP.
- Template-based fill-in (extract fields, fill template):
  Loses the LLM's ability to reorganize and enhance content.
  Rejected.
- Multiple specialized prompts per input type (notes vs
  transcripts vs docs): Over-engineering. A single well-
  crafted prompt handles all input types. Rejected.

## R2 — Editable Output Implementation

**Decision**: Render the generated article in a
`st.text_area()` widget (not `st.markdown()`). This makes
the output directly editable by the user (FR-013). The
`st.text_area` value is also what gets copied to clipboard.

**Rationale**: `st.text_area()` is the simplest way to show
editable text in Streamlit. The user sees the raw Markdown,
can edit it, and copies the edited version. `st.markdown()`
would require a separate edit mode toggle — more complexity.

**Alternatives considered**:
- `st.markdown()` with a separate "Edit" button toggling to
  `st.text_area()`: More UX steps, more state management.
  Rejected per Simplicity First.
- Rich text editor (WYSIWYG): Out of scope per spec. Would
  require JavaScript. Rejected.
- Split view (rendered + editable): Nice but over-engineering
  for MVP. Rejected.

## R3 — Sensitive Data Reminder

**Decision**: Display a `st.info()` banner at the top of the
module page: "Remember to remove sensitive information
(names, ticket numbers) before publishing externally." Always
visible, not dismissible.

**Rationale**: FR-015 requires a reminder. `st.info()` is
a non-intrusive Streamlit banner. Always-visible ensures the
user sees it before every generation. No automated redaction
(out of scope per spec).

**Alternatives considered**:
- Modal/popup on generate: Interrupts workflow, annoying on
  repeated use. Rejected.
- Checkbox acknowledgment: Adds friction. Rejected per
  Simplicity First.
- No reminder (rely on training): Violates FR-015. Rejected.

## R4 — Input Character Limit

**Decision**: 10,000 characters (per spec). Validate with
`len(text)`. If exceeded, truncate and show `st.warning()`.
Higher than 004's 5,000 limit because KB source material
is typically longer.

**Rationale**: Simple length check. No token counting (the
LLM handles truncation at the API level if needed). 10K chars
is approximately 2,500 words — sufficient for most support
transcripts and meeting notes.

**Alternatives considered**:
- Token-based limit: Requires a tokenizer dependency. Over-
  engineering. Rejected.
- No limit: Risks API errors on very long inputs. Rejected.

## R5 — Copy Functionality

**Decision**: Same approach as 004 — use `st.code()` or a
copy helper for the full article. Feature 010 (copy/download)
will standardize this cross-cutting concern later. For MVP,
the editable `st.text_area` content can be selected and
copied natively, plus a "Copy article" button using
Streamlit's clipboard mechanism.

**Rationale**: Consistent with 004 pattern. Avoids premature
investment in copy infrastructure that 010 will replace.

**Alternatives considered**:
- Per-section copy buttons: Spec says "Copy article" for
  the full article (FR-011). Individual section copy is not
  required (unlike 004). Simpler. Accepted.
