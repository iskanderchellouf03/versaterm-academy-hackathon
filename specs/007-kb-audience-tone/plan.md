# Implementation Plan: KB Audience & Tone Selection

**Branch**: `007-kb-audience-tone` | **Date**: 2026-03-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/007-kb-audience-tone/spec.md`

## Summary

Extend the KB Article Generator (006) UI with an audience
dropdown (Internal/External/Support) and a tone dropdown
(Formal/Conversational/Concise). Both selections are injected
into the LLM prompt so the generated article matches the
target reader and writing style. No new files — modifications
to the existing 006 page and prompt.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit (UI controls), `openai` (from 004)
**Storage**: N/A (selections in session state only)
**Testing**: pytest
**Target Platform**: Web (Streamlit app)
**Project Type**: Web application (Streamlit) — enhancement to AI module
**Performance Goals**: Same 30s timeout as 006
**Constraints**: All Python, fixed option lists, single LLM call
**Scale/Scope**: Extends 006 module UI, no new pages

## Constitution Check

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. User-Centric Design | PASS | KMS use case: "audience + tone makes KB articles match reader expectations." Directly improves output usability. |
| II. Simplicity First | PASS | Two dropdowns. Context injected as text into existing prompt. No style guides, no templates. |
| MVP-first | PASS | US1 (audience) adds value alone. Tone (US2) and combined (US3) are incremental. |
| Demo-ready | PASS | Select External + Conversational, paste notes, see customer-friendly FAQ. Impressive demo. |
| No gold-plating | PASS | Fixed option lists, no custom audiences/tones, no audience detection. |
| Tech stack | PASS | Pure Python + Streamlit. |
| Single-repo | PASS | All code in repo. |

**Post-design re-check**: PASS — no violations.

## Project Structure

### Documentation (this feature)

```text
specs/007-kb-audience-tone/
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
├── pages/
│   └── kb_article_generator.py      # (modify) — add audience + tone selectors
├── ai/
│   └── prompts/
│       └── kb_article_generator.py  # (modify) — inject audience/tone context
└── config.py                        # (modify) — add AUDIENCES, TONES constants
```

**Structure Decision**: No new files. Same pattern as 005
extending 004. Modify existing KB page and prompt to accept
audience and tone context.

## Complexity Tracking

No violations to justify.
