# Research: Structured Output Formatting

## R1 — Per-Module Section Configuration

**Decision**: Plain Python dictionary in a single `schema.py`
file. Each module ID maps to an ordered list of section
heading strings.

**Rationale**: A dict is the simplest data structure that
preserves insertion order (Python 3.7+). No YAML/JSON config
files needed — the section definitions are code, versioned
with the repo, and imported directly by each module.

**Alternatives considered**:
- YAML/JSON config file: Adds a file-parsing dependency and
  indirection. Rejected per Simplicity First — the config is
  small and unlikely to be edited by non-developers.
- Dataclass per module: Over-abstraction for a list of
  strings. Rejected — YAGNI.
- Database table: Grossly over-engineered. Rejected.

## R2 — Prompt Engineering for Tone and Structure

**Decision**: Build a system prompt fragment from the module's
section schema and shared formatting rules. Append this
fragment to each module's existing system prompt before
calling the LLM.

**Rationale**: LLMs respond well to explicit structural
instructions in the system prompt. Combining section headings
("You MUST output these sections in this order") with tone
rules ("No preamble, no sign-off, bullet-first") in the
system prompt is the simplest enforcement mechanism. No
post-processing needed for structure — only for minor
Markdown normalization.

**Alternatives considered**:
- Structured output / JSON mode: Forces JSON, which then
  needs to be converted to Markdown. Adds complexity.
  Rejected.
- Few-shot examples in prompt: Increases token count
  significantly. Rejected for MVP.
- Output validation + retry: Checks output and re-calls LLM
  if non-compliant. Adds latency and cost. Rejected for MVP.

## R3 — Markdown Normalization Strategy

**Decision**: Lightweight regex-based post-processor that
fixes common LLM Markdown inconsistencies:
1. Replace `*` list markers with `-`
2. Strip raw HTML tags (except inside code fences)
3. Remove code fences wrapping non-code content
4. Normalize bold from `__text__` to `**text**`
5. Ensure section headings use `##` / `###`

**Rationale**: LLMs produce 95%+ correct Markdown when
instructed. The normalizer handles the remaining edge cases
with simple regex passes. No AST parsing needed — the
corrections are syntactic, not semantic.

**Alternatives considered**:
- Markdown AST parser (e.g., `markdown-it-py`, `mistune`):
  Full parsing is overkill for fixing list markers and
  stripping HTML. Adds an external dependency. Rejected per
  Simplicity First.
- No post-processing: Relies entirely on prompt engineering.
  Works 95% of the time but spec requires 100% Markdown
  validity (SC-003). Rejected.
- Client-side (JavaScript) normalization: Violates Python-
  only tech stack constraint. Rejected.

## R4 — Empty Section Handling

**Decision**: After LLM response, check that all required
section headings are present. If a heading is missing, insert
it at the correct position with the text "None identified."

**Rationale**: LLMs sometimes skip sections when they have
nothing to say. A simple post-check ensures FR-002 and FR-003
compliance. Insertion is trivial — split on headings, check
for gaps, insert placeholders.

**Alternatives considered**:
- Rely solely on prompt instruction: LLMs occasionally skip
  sections despite being told not to. Rejected — FR-002
  requires 100% compliance.
- Return error and ask user to regenerate: Poor UX. Rejected.

## R5 — Integration Pattern with AI Modules

**Decision**: Each AI module (004, 006, 008) calls two
functions from `src/output/`:
1. `get_system_prompt(module_id)` — returns the formatting
   rules fragment to append to the module's system prompt.
2. `normalize_output(module_id, raw_text)` — post-processes
   the LLM response (Markdown fixes + missing section
   insertion).

**Rationale**: Two-function interface is minimal and
composable. Modules remain in control of their own LLM calls
and can add module-specific prompt content. The output package
only handles formatting concerns.

**Alternatives considered**:
- Decorator pattern wrapping LLM calls: Too magical, hides
  behavior. Rejected per Simplicity First.
- Middleware / pipeline: Over-abstraction for 3 modules.
  Rejected — YAGNI.
- Monolithic "generate" function that owns the LLM call:
  Couples formatting to LLM invocation. Rejected — each
  module should own its own LLM interaction.
