# Implementation Plan: Onboarding Focus Notes

**Branch**: `009-onboarding-focus-notes` | **Date**: 2026-03-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/009-onboarding-focus-notes/spec.md`

## Summary

Extend the Onboarding Plan Generator (008) with an optional
"Focus notes" text area. Focus notes are injected into the
LLM prompt to emphasize specific topics in the generated plan.
No new files — modifications to the existing 008 page and
prompt. Same pattern as 005 extending 004 and 007 extending
006.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit (UI), `openai` (from 004)
**Storage**: N/A (session state only)
**Testing**: pytest
**Target Platform**: Web (Streamlit app)
**Project Type**: Web application (Streamlit) — enhancement to AI module
**Performance Goals**: Same 30s timeout as 008
**Constraints**: All Python, 1,000 char focus notes limit, optional field
**Scale/Scope**: Extends 008 module UI, no new pages

## Constitution Check

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. User-Centric Design | PASS | HR/Manager use case: "customize onboarding plan to team's real priorities." Directly improves plan relevance. |
| II. Simplicity First | PASS | One text area. Injected as text into existing prompt. No NLP parsing, no focus-area taxonomy. |
| MVP-first | PASS | US1 (focus notes input) adds value alone. Multiple areas (US2) and refinement (US3) are incremental. |
| Demo-ready | PASS | Add "safety-critical workflows" as focus, see plan prioritize safety. Impressive demo. |
| No gold-plating | PASS | No predefined focus list, no focus weighting, no focus-area auto-detection. |
| Tech stack | PASS | Pure Python + Streamlit. |
| Single-repo | PASS | All code in repo. |

**Post-design re-check**: PASS — no violations.

## Project Structure

### Documentation (this feature)

```text
specs/009-onboarding-focus-notes/
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
│   └── onboarding_planner.py        # (modify) — add focus notes text area
├── ai/
│   └── prompts/
│       └── onboarding_planner.py    # (modify) — inject focus notes context
└── config.py                        # (unchanged)
```

**Structure Decision**: No new files. Modify existing
onboarding planner page and prompt. Same pattern as 005/007.

## Complexity Tracking

No violations to justify.
