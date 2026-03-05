# Implementation Plan: App Shell Layout with Sidebar Navigation

**Branch**: `003-app-shell-layout` | **Date**: 2026-03-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/003-app-shell-layout/spec.md`

## Summary

Build the authenticated app shell: a persistent left sidebar
listing available modules with a main content area that
updates on module selection. Uses Streamlit's native
`st.sidebar` for the navigation panel and `st.session_state`
to track the active module. Module content is rendered via a
simple dispatch dictionary mapping module names to page
functions. No new dependencies beyond Streamlit.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit (sidebar, session state, page rendering)
**Storage**: N/A (active module tracked in session state)
**Testing**: pytest
**Target Platform**: Web (Streamlit app)
**Project Type**: Web application (Streamlit)
**Performance Goals**: Module switch in < 1 second
**Constraints**: All Python, no external services, single repo
**Scale/Scope**: 3 AI modules initially (004, 006, 008), expandable

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after
Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. User-Centric Design | PASS | Directly maps to employee task: "switch modules to stay focused." Sidebar is the primary navigation for all module access. |
| II. Simplicity First | PASS | Uses `st.sidebar` (built-in), dict-based page dispatch. No router library, no component framework. |
| MVP-first | PASS | US1 (sidebar switching) is independently demoable. Responsive (US2) and visual polish (US3) are incremental. |
| Demo-ready | PASS | Shell is demoable with placeholder module content. |
| No gold-plating | PASS | No nested navigation, no user-configurable modules, no state persistence across refreshes. |
| Tech stack | PASS | Pure Python + Streamlit. |
| Single-repo | PASS | All code in repo. |

**Post-design re-check**: PASS — no violations introduced
during Phase 1 design.

## Project Structure

### Documentation (this feature)

```text
specs/003-app-shell-layout/
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
├── app.py               # Entry point — auth gate, shell layout, page dispatch
├── auth/                # (existing from 001, 002)
├── pages/
│   ├── __init__.py      # Module registry (dict of name → render function)
│   └── placeholder.py   # Default placeholder page for unimplemented modules
└── config.py            # (existing) — add MODULE_LIST constant
```

**Structure Decision**: Single `src/pages/` package for module
page functions. `app.py` owns the shell layout: sidebar with
module list, active module tracking via `st.session_state`,
and dispatch to the selected page function. Each future module
(004, 006, 008) adds its own file to `src/pages/`.

## Complexity Tracking

No violations to justify. All choices align with constitution
principles.
