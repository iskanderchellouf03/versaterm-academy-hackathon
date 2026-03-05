# Implementation Plan: Employee Email & Access Code Authentication

**Branch**: `001-employee-auth` | **Date**: 2026-03-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-employee-auth/spec.md`

## Summary

Implement a lightweight email + one-time code authentication
gate for the Versaterm Academy web app. Employees enter their
company email, receive a 6-digit code, and verify it to gain
access. Built entirely in Python with Streamlit, using SQLite
for code storage and Streamlit session state for sessions.
Zero external auth dependencies.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit (UI + session state)
**Storage**: SQLite via `sqlite3` (stdlib) for access codes
**Testing**: pytest
**Target Platform**: Web (localhost / deployed Streamlit app)
**Project Type**: Web application (Streamlit)
**Performance Goals**: Sub-second page loads, code generation
under 100ms
**Constraints**: All Python ecosystem, no external services
that cannot be mocked locally, single repo
**Scale/Scope**: Single-user to small team (~50 employees),
single Streamlit instance

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after
Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. User-Centric Design | PASS | Feature maps directly to employee use case: "only authorized staff can access the web app". Every FR ties to an employee workflow. |
| II. Simplicity First | PASS | Uses stdlib (`sqlite3`, `secrets`, `smtplib`), Streamlit session state. No ORM, no JWT, no external auth service. Minimal files. |
| MVP-first | PASS | US1 (core login) is independently demostrable. US2/US3 are incremental. |
| Demo-ready | PASS | App is runnable after Phase 2 with console-printed codes (no SMTP required). |
| No gold-plating | PASS | Rate limiting (US3) deferred to P3. No admin panel, no user management. |
| Tech stack | PASS | Full Python: Streamlit + stdlib. |
| Single-repo | PASS | All code in this repository. SQLite is a local file. |
| Secrets in env | PASS | SMTP credentials loaded from environment variables / `.env`. |

**Post-design re-check**: PASS — no violations introduced
during Phase 1 design.

## Project Structure

### Documentation (this feature)

```text
specs/001-employee-auth/
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
├── app.py               # Streamlit entry point, page routing
├── auth/
│   ├── __init__.py
│   ├── service.py       # Code generation, verification, rate limiting
│   ├── email.py         # SMTP email delivery (with console fallback)
│   └── db.py            # SQLite schema init and queries
└── config.py            # Environment variable loading, constants

.env.example             # Template for SMTP and domain config
```

**Structure Decision**: Single project layout. Streamlit app
with a small `auth` package. No separate backend/frontend —
Streamlit is both. No tests directory in initial structure per
constitution (tests not requested in spec; add only if needed).

## Complexity Tracking

No violations to justify. All choices align with constitution
principles.
