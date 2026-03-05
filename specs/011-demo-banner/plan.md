# Implementation Plan: Demo Scope Banner

**Branch**: `011-demo-banner` | **Date**: 2026-03-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/011-demo-banner/spec.md`

## Summary

Add a fixed demo banner at the top of every page (including
login) that communicates "demo/prototype" status and "no data
persistence." Uses `st.markdown()` with inline CSS for
styling and fixed positioning. Dismiss state tracked in
`st.session_state`. Banner text configurable from `config.py`.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit (`st.markdown` with `unsafe_allow_html=True`)
**Storage**: N/A (dismiss state in session state only)
**Testing**: pytest
**Target Platform**: Web (Streamlit app)
**Project Type**: Web application (Streamlit) — UI component
**Performance Goals**: Instant render (no async, no API calls)
**Constraints**: All Python, minimal CSS, no JavaScript
**Scale/Scope**: Single banner component, all pages

## Constitution Check

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. User-Centric Design | PASS | Sets stakeholder expectations: "this is a demo, no data saved." Prevents incorrect assumptions. |
| II. Simplicity First | PASS | One `st.markdown()` call with inline CSS. One session state flag for dismiss. No JS, no component library. |
| MVP-first | PASS | US1 (always-visible banner) is trivial. Dismiss (US2) is incremental. |
| Demo-ready | PASS | The banner literally exists to support demos. |
| No gold-plating | PASS | No animation, no theme integration, no admin toggle. |
| Tech stack | PASS | Pure Python + inline CSS (necessary for fixed positioning in Streamlit). |
| Single-repo | PASS | All code in repo. |

**Post-design re-check**: PASS — no violations.

## Project Structure

### Documentation (this feature)

```text
specs/011-demo-banner/
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
├── components/
│   ├── __init__.py          # (existing from 010)
│   └── demo_banner.py       # Banner rendering + dismiss logic
├── app.py                   # (modify) — call render_demo_banner() at top
└── config.py                # (modify) — add DEMO_BANNER_TEXT constant
```

**Structure Decision**: New file `src/components/demo_banner.py`
in the existing components package. Called from `app.py` at
the very top of the page (before auth gate) so it appears on
login screen too.

## Complexity Tracking

No violations to justify.
