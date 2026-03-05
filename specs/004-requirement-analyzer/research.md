# Research: AI Requirement Analyzer

## R1 — LLM API Client Choice

**Decision**: Use the `openai` Python package as the LLM
client. Configure via `OPENAI_API_KEY` and `OPENAI_BASE_URL`
environment variables to support any OpenAI-compatible API
(OpenAI, Azure OpenAI, local models via Ollama/LM Studio).

**Rationale**: The `openai` package is the de-facto standard
Python LLM client. It supports streaming, timeouts, and
retries out of the box. Using `OPENAI_BASE_URL` makes the
client provider-agnostic — works with OpenAI, Azure, or
local endpoints without code changes.

**Alternatives considered**:
- `anthropic` package: Only works with Anthropic models.
  Less flexible. Rejected for provider-agnosticism.
- `litellm`: Abstraction over multiple providers. Adds a
  dependency for functionality we don't need (we only need
  one provider at a time). Rejected per Simplicity First.
- `requests` (raw HTTP): Loses retry logic, streaming, and
  type safety. More code for the same result. Rejected.
- `langchain`: Massive dependency, extreme over-abstraction
  for a single LLM call. Rejected per Simplicity First.

## R2 — Prompt Engineering Strategy

**Decision**: Single system prompt with explicit section
headings and formatting rules. The user's requirement is
passed as the user message. No few-shot examples (to keep
token count low). The prompt explicitly lists the five
required sections and instructs the LLM to use Markdown
headings, bullet points, and Given/When/Then format.

**Rationale**: A well-structured system prompt produces
reliable output from modern LLMs (GPT-4, Claude, Llama 3).
The prompt leverages feature 014 (structured output format)
by importing formatting rules from `src/output/prompt.py`.
This keeps the module prompt focused on content (what to
analyze) while 014 handles structure (how to format).

**Alternatives considered**:
- Few-shot examples: Increases token count by ~2-3x. Not
  needed for this task — modern LLMs handle structured
  output instructions well. Rejected for MVP.
- Chain-of-thought with multiple calls: Adds latency and
  cost. A single call produces adequate results. Rejected.
- JSON mode / structured output: Forces JSON response, which
  then needs Markdown conversion. Adds complexity. Rejected.

## R3 — Timeout and Error Handling

**Decision**: Set a 30-second timeout on the `openai` client
call. If the timeout fires, display a user-friendly message:
"Analysis timed out. Please try again." Use Streamlit's
`st.spinner()` as the loading indicator during processing.

**Rationale**: The spec requires a 30-second timeout (FR-013)
and loading indicator (FR-008). `st.spinner()` is Streamlit's
built-in loading UI. The `openai` package supports a
`timeout` parameter directly.

**Alternatives considered**:
- Custom async timeout with `asyncio`: Over-engineering.
  The `openai` package handles this natively. Rejected.
- Streaming with progressive display: Adds UX complexity
  (partial sections appearing). Good for future enhancement
  but not MVP. Rejected for now.

## R4 — Copy Functionality

**Decision**: Use Streamlit's `st.code()` block with a built-
in copy button for each section, or use a custom clipboard
helper via `st.components.v1.html()` with a small JavaScript
snippet for copy-to-clipboard. The cross-cutting copy feature
(010) will standardize this — for MVP, use `st.code()` blocks
which have a native copy icon.

**Rationale**: `st.code()` renders a code block with a copy
button in the top-right corner. While not ideal for Markdown
content, it provides copy functionality with zero custom code.
Feature 010 will replace this with a proper copy/download
mechanism later.

**Alternatives considered**:
- `pyperclip`: Server-side clipboard — doesn't work in web
  browsers. Rejected.
- Custom JavaScript clipboard API: Works but adds JS to a
  Python-only stack. Acceptable as a small utility but
  deferred to 010. Rejected for now.
- Third-party Streamlit component: Adds external dependency.
  Rejected per Simplicity First.

## R5 — Input Validation

**Decision**: Check input length client-side via Python
(`len(text) > 5000`). If exceeded, truncate and show a
warning via `st.warning()`. If empty, show `st.error("Please
enter a requirement to analyze.")` and do not call the LLM.

**Rationale**: Simple Python string length check. No regex,
no NLP-based validation. The spec says "best-effort" for
non-requirement inputs, so no content validation is needed.

**Alternatives considered**:
- NLP-based input classification: Over-engineering. The LLM
  handles bad input gracefully (flags it in Risks). Rejected.
- Hard block on non-requirement text: Spec says best-effort.
  Rejected.

## R6 — LLM Client as Shared Service

**Decision**: Create `src/ai/client.py` with a `get_client()`
function that returns a configured `openai.OpenAI` instance.
All AI modules (004, 006, 008) import this shared client.
Model name configured via `OPENAI_MODEL` env var (default:
`gpt-4o`).

**Rationale**: Centralizes API key loading, base URL config,
and timeout settings. Adding a new AI module doesn't require
duplicating client setup.

**Alternatives considered**:
- Per-module client instantiation: Duplicates config loading.
  Rejected.
- Dependency injection: Over-abstraction for 3 modules.
  Rejected — YAGNI.
