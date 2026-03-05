# Research: Employee Email & Access Code Authentication

**Feature**: 001-employee-auth
**Date**: 2026-03-04

## R1: UI Framework for Authentication Flow

**Decision**: Streamlit
**Rationale**: Constitution mandates full-stack Python. Streamlit
provides built-in session state (`st.session_state`) which maps
directly to the session persistence requirement. Login/code-entry
forms are trivial with `st.text_input` and `st.button`. No
frontend build tooling needed.
**Alternatives considered**:
- Gradio: Better for ML demos, less natural for multi-page
  app navigation and session gating.
- Flask/FastAPI + Jinja: More control but violates simplicity
  principle — requires HTML templates, CSRF handling, and
  session middleware.

## R2: Access Code Storage

**Decision**: SQLite via Python `sqlite3` (stdlib)
**Rationale**: Codes need persistence across Streamlit reruns
(each interaction re-executes the script). In-memory dicts are
lost on rerun. SQLite is zero-config, stdlib, file-based, and
handles concurrent reads for a single-user hackathon app. No
external database dependency.
**Alternatives considered**:
- In-memory dict: Lost on Streamlit rerun; unsuitable.
- JSON file: No atomic writes, race conditions possible.
- Redis: External dependency; violates single-repo constraint.

## R3: Email Delivery

**Decision**: Python `smtplib` (stdlib) with SMTP credentials
from environment variables.
**Rationale**: Stdlib, zero dependencies. Works with any SMTP
provider (Gmail app password, SendGrid SMTP, Mailgun SMTP).
For local development/demo, codes can be logged to console as
a fallback when SMTP is not configured.
**Alternatives considered**:
- SendGrid SDK: External dependency for a single SMTP call.
- `email` + `smtplib` combo: `email` is stdlib too; use it
  for MIME formatting.

## R4: Code Generation

**Decision**: Python `secrets.randbelow(1000000)` zero-padded
to 6 digits.
**Rationale**: `secrets` module is stdlib and
cryptographically secure. 6-digit numeric codes are standard
for OTP flows and user-friendly on mobile keyboards.
**Alternatives considered**:
- `random.randint`: Not cryptographically secure.
- UUID-based tokens: Less user-friendly to type manually.

## R5: Session Management

**Decision**: Streamlit `st.session_state` with server-side
validation.
**Rationale**: Streamlit session state persists across reruns
within a browser tab session. For session timeout, store
`last_activity` timestamp in session state and check on each
page load. Logout clears session state. This is the simplest
approach with zero dependencies.
**Alternatives considered**:
- Cookie-based sessions: Streamlit doesn't expose cookie
  control easily; requires workarounds.
- JWT tokens: Over-engineered for a Streamlit app where the
  server already manages state.

## R6: Rate Limiting

**Decision**: SQLite-backed counter per email, checked on code
request.
**Rationale**: Rate limit state must persist across Streamlit
reruns. SQLite already chosen for code storage, so reuse it.
Query: count codes issued to email in last 15 minutes. Simple,
no new dependencies.
**Alternatives considered**:
- In-memory counter: Lost on rerun.
- Redis: External dependency.
