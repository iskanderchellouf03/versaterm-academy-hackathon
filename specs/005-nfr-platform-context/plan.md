# Implementation Plan: NFR & Platform Context for Requirement Analysis

**Branch**: `005-nfr-platform-context` | **Date**: 2026-03-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/005-nfr-platform-context/spec.md`

## Summary

Extend the Requirement Analyzer (004) UI with a system type
dropdown (Web/Mobile/API/Desktop) and NFR checkboxes
(Performance, Security, Accessibility, Scalability,
Reliability, Usability). Both selections are injected into the
LLM prompt to produce platform- and quality-aware analysis
output. No new files — modifications to the existing 004
page and prompt.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit (UI controls), `openai` (from 004)
**Storage**: N/A (selections in session state only)
**Testing**: pytest
**Target Platform**: Web (Streamlit app)
**Project Type**: Web application (Streamlit) — enhancement to AI module
**Performance Goals**: Same 30s timeout as 004
**Constraints**: All Python, fixed option lists, single LLM call
**Scale/Scope**: Extends 004 module UI, no new pages

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after
Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. User-Centric Design | PASS | PO/QA use case: "platform context makes analysis more relevant." Directly improves output quality for employee workflows. |
| II. Simplicity First | PASS | One dropdown + checkboxes. Injected as text into the existing prompt. No new services, no knowledge base. |
| MVP-first | PASS | US1 (system type) adds value alone. NFRs (US2) and combined (US3) are incremental. |
| Demo-ready | PASS | Immediately demoable — pick Mobile, paste requirement, see mobile-specific output. |
| No gold-plating | PASS | Fixed option lists, no custom types, no NFR weighting or priority. |
| Tech stack | PASS | Pure Python + Streamlit. |
| Single-repo | PASS | All code in repo. |

**Post-design re-check**: PASS — no violations.

## Project Structure

### Documentation (this feature)

```text
specs/005-nfr-platform-context/
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
│   └── requirement_analyzer.py  # (modify) — add selectbox + checkboxes
├── ai/
│   └── prompts/
│       └── requirement_analyzer.py  # (modify) — inject platform/NFR context
└── config.py                    # (modify) — add SYSTEM_TYPES, NFR_OPTIONS constants
```

**Structure Decision**: No new files. Modify the existing
requirement analyzer page to add UI controls and extend the
prompt builder to include platform and NFR context. Constants
for system types and NFR options live in `config.py`.

## Complexity Tracking

No violations to justify. All choices align with constitution
principles.
