# Implementation Plan: Session Sign-Out

**Branch**: `002-session-logout` | **Date**: 2026-03-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/002-session-logout/spec.md`

## Summary

Add a "Sign out" button to the authenticated app shell that
clears Streamlit session state and redirects to the login
screen. Depends on 001-employee-auth session model. No new
storage, no new dependencies — purely session state
manipulation and a UI button.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit (session state + UI)
**Storage**: N/A (session state is in-memory via Streamlit)
**Testing**: pytest
**Target Platform**: Web (Streamlit app)
**Project Type**: Web application (Streamlit)
**Performance Goals**: Sign-out completes in < 2 seconds
**Constraints**: All Python, no external services, single repo
**Scale/Scope**: Single Streamlit instance, ~50 employees

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after
Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. User-Centric Design | PASS | Directly maps to employee task: "end session so no one else can use assistant." Every FR ties to security and convenience. |
| II. Simplicity First | PASS | Single button, clears `st.session_state`, calls `st.rerun()`. No confirmation dialog, no multi-step flow. Zero new dependencies. |
| MVP-first | PASS | US1 (sign-out action) is the entire core. US2 (visibility) is layout placement. |
| Demo-ready | PASS | Feature is demoable immediately — click button, see login screen. |
| No gold-plating | PASS | No confirmation modal, no admin forced logout, no real-time tab sync. |
| Tech stack | PASS | Pure Python + Streamlit. |
| Single-repo | PASS | All code in repo. No external session store. |

**Post-design re-check**: PASS — no violations introduced
during Phase 1 design.

## Project Structure

### Documentation (this feature)

```text
specs/002-session-logout/
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
├── app.py               # Entry point — add sign-out button to sidebar (existing from 001)
├── auth/
│   ├── __init__.py
│   ├── service.py       # Add logout() function to clear session
│   ├── email.py         # (unchanged)
│   └── db.py            # (unchanged)
└── config.py            # (unchanged)
```

**Structure Decision**: No new files. Add a `logout()` function
to `src/auth/service.py` and a "Sign out" button in the
sidebar area of `src/app.py`. The function clears all
authentication keys from `st.session_state` and triggers
`st.rerun()` to redirect to the login screen.

## Complexity Tracking

No violations to justify. All choices align with constitution
principles.
