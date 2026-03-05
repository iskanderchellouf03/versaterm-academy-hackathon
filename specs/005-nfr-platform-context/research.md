# Research: NFR & Platform Context for Requirement Analysis

## R1 — Prompt Injection Strategy for Platform Context

**Decision**: Append a "Context" section to the system prompt
that states the selected system type and its key concerns.
Example: "The target system is a Mobile application. Consider:
offline handling, battery consumption, touch interactions,
device permissions, network variability."

**Rationale**: Simple string concatenation in the prompt
builder. The LLM naturally incorporates stated context into
its analysis. No separate knowledge base or RAG needed —
modern LLMs have strong built-in knowledge of platform-
specific concerns.

**Alternatives considered**:
- Platform-specific prompt templates (one per system type):
  4 separate templates with heavy duplication. Rejected —
  a single template with injected context is simpler.
- Few-shot examples per platform: Increases token count
  significantly (4x the examples). Rejected for MVP.
- RAG with platform knowledge documents: Over-engineering.
  The LLM already knows platform concerns. Rejected.

## R2 — NFR Integration into Prompt

**Decision**: Append selected NFRs as a bulleted list in the
system prompt: "The following non-functional requirements
apply: - Performance: response times, throughput, resource
usage - Security: authentication, authorization, data
protection". Each NFR includes a brief description to guide
the LLM.

**Rationale**: Explicit NFR descriptions in the prompt
produce more targeted output than just listing NFR names.
The descriptions are short (one line each) and hardcoded
in the prompt builder.

**Alternatives considered**:
- NFR names only (no descriptions): LLM may interpret
  "Performance" too broadly. Adding brief descriptions
  costs minimal tokens and improves specificity. Rejected.
- Separate LLM call per NFR: Multiplies API calls and
  latency. Rejected per Simplicity First.
- User-defined NFR descriptions: Out of scope (fixed list).
  Rejected.

## R3 — UI Controls for System Type and NFRs

**Decision**: Use `st.selectbox()` for system type (single
selection, defaults to "Web") and `st.multiselect()` for
NFRs (zero or more selections, defaults to empty).

**Rationale**: `st.selectbox()` enforces single selection
from a fixed list — matches FR-001. `st.multiselect()`
allows zero-to-many selections — matches FR-005. Both
persist in session state automatically. Placed above the
"Analyze" button alongside the text input.

**Alternatives considered**:
- `st.radio()` for system type: Takes more vertical space
  for 4 options. Selectbox is more compact. Rejected.
- Individual `st.checkbox()` per NFR: Works but
  `st.multiselect()` is cleaner and takes less space.
  Either is acceptable; multiselect chosen for compactness.
- Sidebar placement: Spec says controls MUST be "alongside
  the requirement text input" (FR-009). Sidebar would
  separate them. Rejected.

## R4 — Session State Persistence

**Decision**: Store `system_type` and `selected_nfrs` in
`st.session_state`. Both persist across re-analyses within
the same session (FR-010). Reset on new session or logout.

**Rationale**: Streamlit session state automatically persists
widget values across reruns. No additional code needed —
`st.selectbox` and `st.multiselect` with `key` parameters
handle this natively.

**Alternatives considered**:
- URL query parameters: Streamlit has limited URL state
  support. More complex than session state. Rejected.
- Database persistence: Over-engineering. Out of scope
  (session-only). Rejected.
