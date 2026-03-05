# Research: One-Click Copy & Markdown Download

## R1 — Clipboard Copy in Streamlit

**Decision**: Use `st.components.v1.html()` to inject a small
JavaScript snippet that calls `navigator.clipboard.writeText()`
when the user clicks a styled button. The Python function
`render_copy_button(text, label="Copy")` generates the HTML/JS
component. On success, the button text changes to "Copied!"
for 2 seconds.

**Rationale**: Streamlit has no built-in clipboard API.
`navigator.clipboard.writeText()` is the standard browser
Clipboard API, supported in all modern browsers over HTTPS.
The JS is minimal (< 10 lines) and self-contained — no
external libraries.

**Alternatives considered**:
- `st.code()` built-in copy: Only works for code blocks, not
  arbitrary markdown. Rejected.
- `pyperclip`: Server-side clipboard — doesn't work in web
  browsers. Rejected.
- `streamlit-clipboard` third-party component: External
  dependency. Rejected per Simplicity First.
- Manual select-all: Poor UX, doesn't satisfy "one-click"
  requirement. Rejected.

## R2 — Download as .md File

**Decision**: Use `st.download_button()` (built-in Streamlit
widget). Pass the markdown text as data, MIME type as
`text/markdown`, and filename following the pattern
`{module-slug}-{YYYY-MM-DD}.md`.

**Rationale**: `st.download_button()` is a first-class
Streamlit widget that handles file downloads natively. No
server-side file generation needed — the content is passed
as a string. The filename is generated with
`datetime.date.today().isoformat()`.

**Alternatives considered**:
- Write to temp file + serve: Over-engineering. Streamlit
  handles in-memory download natively. Rejected.
- `st.components.v1.html()` with JS download: Unnecessary
  when `st.download_button` exists. Rejected.

## R3 — Per-Section Copy

**Decision**: Parse the output markdown into sections by
splitting on `## ` headings. For each section, render a small
copy icon (using the same `render_copy_button` with a compact
icon style) that copies only that section's content (heading
+ body until next heading).

**Rationale**: Reuses the same clipboard mechanism from R1.
Section splitting is simple string parsing (split on `\n## `).
Each section gets its own copy button rendered inline.

**Alternatives considered**:
- No per-section copy (full-output only): Violates FR-009.
  Rejected.
- Server-side section extraction API: Over-engineering.
  String splitting is sufficient. Rejected.

## R4 — Button State Management

**Decision**: Both Copy and Download buttons are rendered
conditionally:
- Hidden/disabled when no output exists (check session state)
- Disabled while generation is in progress (check loading
  state)
- Active when output is available and not loading

**Rationale**: Simple conditional rendering using session
state flags that already exist in each module
(`*_loading`, `*_result`).

**Alternatives considered**:
- Always show buttons, show error on click: Poor UX. Rejected.

## R5 — Shared Component Architecture

**Decision**: Create `src/components/copy_button.py` with
`render_copy_button(text, label)` and
`src/components/download_button.py` with
`render_download_button(text, module_slug)`. Each module page
imports and calls these after rendering output.

**Rationale**: DRY — all modules use identical copy/download
logic. Adding a new module = importing the same helpers.
Replaces the per-module copy implementations from 004/006/008.

**Alternatives considered**:
- Per-module inline copy code: Duplicates 3x. Rejected.
- Abstract base page class: Over-abstraction for shared
  buttons. Rejected — YAGNI.

## R6 — Clipboard Fallback

**Decision**: If `navigator.clipboard` is unavailable (non-
HTTPS, old browser), the JS snippet catches the error and
displays an inline message: "Unable to copy. Please select
the text and copy manually (Ctrl+C)." The button changes
to an error state.

**Rationale**: Graceful degradation per FR-011. The fallback
is a simple try/catch in the JS snippet.

**Alternatives considered**:
- `document.execCommand('copy')`: Deprecated API. May work
  in some browsers but is being removed. Rejected as primary
  mechanism, but could be a secondary fallback. Noted.
