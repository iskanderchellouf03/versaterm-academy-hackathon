# Implementation Plan: AI Requirement Analyzer

**Branch**: `004-requirement-analyzer` | **Date**: 2026-03-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/004-requirement-analyzer/spec.md`

## Summary

Build the first AI-powered module: a Requirement Analyzer
that accepts pasted requirement text, sends it to an LLM
with a structured prompt, and displays the analysis in five
sections (Rewritten Requirements, Acceptance Criteria, Test
Cases, Edge Cases, Risks). Uses OpenAI-compatible API via
the `openai` Python package. Input validation, loading
indicator, 30-second timeout, and copy functionality included.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit (UI), `openai` Python package (LLM API client)
**Storage**: N/A (stateless — no analysis history)
**Testing**: pytest
**Target Platform**: Web (Streamlit app)
**Project Type**: Web application (Streamlit) — AI module
**Performance Goals**: 90% of analyses complete within 15 seconds
**Constraints**: All Python, 5,000 char input limit, 30s timeout
**Scale/Scope**: Single module within the app shell (003)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after
Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. User-Centric Design | PASS | Maps to PO/QA use case: "paste requirement, get structured analysis." Every FR ties to accelerating delivery. |
| II. Simplicity First | PASS | Single LLM call with structured prompt. No chain-of-thought, no multi-step pipeline, no RAG. One function call. |
| MVP-first | PASS | US1 (core analyze) is independently demoable. Copy (US2) and refinement (US3) are incremental. |
| Demo-ready | PASS | Module works with any OpenAI-compatible API (local or cloud). |
| No gold-plating | PASS | No analysis history, no export formats, no Jira integration. |
| Tech stack | PASS | Python + `openai` package (standard Python LLM client). |
| Single-repo | PASS | All code in repo. API key via env var. |
| Secrets in env | PASS | LLM API key loaded from `OPENAI_API_KEY` env var. |

**Post-design re-check**: PASS — no violations introduced
during Phase 1 design.

## Project Structure

### Documentation (this feature)

```text
specs/004-requirement-analyzer/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```text
src/
├── app.py               # (existing) — shell layout from 003
├── pages/
│   ├── __init__.py      # (existing) — register requirement_analyzer
│   ├── placeholder.py   # (existing)
│   └── requirement_analyzer.py  # Module UI: input, button, output display
├── ai/
│   ├── __init__.py
│   ├── client.py        # LLM API client wrapper (openai package)
│   └── prompts/
│       └── requirement_analyzer.py  # System prompt for 004
├── output/              # (from 014) — section schema, normalizer
└── config.py            # (existing) — add OPENAI_API_KEY, model name
```

**Structure Decision**: New `src/ai/` package for shared LLM
client. Module-specific prompt in `src/ai/prompts/`. Page
renderer in `src/pages/requirement_analyzer.py`. The AI client
is shared across all future AI modules (006, 008).

## Complexity Tracking

No violations to justify. All choices align with constitution
principles.
