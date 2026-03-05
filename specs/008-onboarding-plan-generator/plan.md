# Implementation Plan: Onboarding Plan Generator

**Branch**: `008-onboarding-plan-generator` | **Date**: 2026-03-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/008-onboarding-plan-generator/spec.md`

## Summary

Build the third AI module: an Onboarding Plan Generator that
accepts role, product, and level inputs and produces a
structured 2-week learning plan with five sections (What It
Is, Why It Matters, Key Terms, Learning Plan, Checkpoints).
Follows the same architecture as 004 and 006: shared LLM
client, structured output formatting (014), registered in the
app shell (003).

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit (UI), `openai` (shared from 004)
**Storage**: N/A (stateless — no plan history)
**Testing**: pytest
**Target Platform**: Web (Streamlit app)
**Project Type**: Web application (Streamlit) — AI module
**Performance Goals**: 90% of generations within 20 seconds
**Constraints**: All Python, 30s timeout, free-text role/product inputs
**Scale/Scope**: Single module within the app shell (003)

## Constitution Check

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. User-Centric Design | PASS | HR/new-hire use case: "enter role/product/level, get 2-week ramp plan." Directly accelerates employee onboarding. |
| II. Simplicity First | PASS | Single LLM call, reuses shared client (004) and output formatting (014). Two text inputs + one selectbox. |
| MVP-first | PASS | US1 (generate plan) is independently demoable. Copy (US2) and refinement (US3) incremental. |
| Demo-ready | PASS | Enter role + product + level, get a complete onboarding plan. Impressive demo. |
| No gold-plating | PASS | No plan history, no PDF export, no custom durations, no resource linking. |
| Tech stack | PASS | Pure Python + Streamlit + openai. |
| Single-repo | PASS | All code in repo. |

**Post-design re-check**: PASS — no violations.

## Project Structure

### Documentation (this feature)

```text
specs/008-onboarding-plan-generator/
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
│   ├── __init__.py                  # (modify) — register onboarding_planner
│   └── onboarding_planner.py        # Module UI: inputs, generate, output
├── ai/
│   ├── client.py                    # (existing from 004)
│   └── prompts/
│       └── onboarding_planner.py    # System prompt for 008
├── output/                          # (existing from 014)
└── config.py                        # (existing) — add EXPERIENCE_LEVELS constant
```

**Structure Decision**: Same pattern as 004 and 006. New page
file + new prompt file. Reuses shared AI client and output
formatting.

## Complexity Tracking

No violations to justify.
