# Tasks: Employee Email & Access Code Authentication

**Input**: Design documents from `/specs/001-employee-auth/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Not explicitly requested in specification. Skipped.

**Organization**: Tasks grouped by user story (US1: login flow, US2: session persistence, US3: code expiry & rate limiting).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project structure, dependencies, configuration

- [x] T001 Create project directory structure: `src/`, `src/auth/`, and `src/auth/__init__.py`
- [x] T002 [P] Create `requirements.txt` with `streamlit` dependency
- [x] T003 [P] Create `.env.example` with SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM, ALLOWED_DOMAIN variables and descriptive comments
- [x] T004 [P] Create `src/config.py` with environment variable loading (`os.getenv`) for SMTP settings, ALLOWED_DOMAIN (default "versaterm.com"), CODE_EXPIRY_MINUTES (default 10), SESSION_TIMEOUT_HOURS (default 8), RATE_LIMIT_MAX (default 5), RATE_LIMIT_WINDOW_MINUTES (default 15), and DB_PATH (default "auth.db")

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Database schema and shared auth infrastructure that all user stories depend on

**⚠️ CRITICAL**: No user story work can begin until the database is initialized.

- [x] T005 Implement `init_db()` and `get_connection()` in `src/auth/db.py` — create SQLite database at DB_PATH with `access_codes` table (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL, code TEXT NOT NULL, created_at DATETIME NOT NULL, expires_at DATETIME NOT NULL, used BOOLEAN DEFAULT 0). Use `CREATE TABLE IF NOT EXISTS`. Import DB_PATH from `src/config.py`.
- [x] T006 Create `src/app.py` as Streamlit entry point — set page config (`st.set_page_config`), call `init_db()` on startup, implement auth gate: if `st.session_state.get("authenticated")` is True show main app placeholder, else show login screen placeholder. Import from `src/auth/` and `src/config.py`.

**Checkpoint**: App runs with `streamlit run src/app.py`, shows login placeholder, database file is created.

---

## Phase 3: User Story 1 - Employee Login with Access Code (Priority: P1) 🎯 MVP

**Goal**: Employee enters company email, receives 6-digit code, enters code, gains access to app.

**Independent Test**: Run app → enter `user@versaterm.com` → check terminal for code → enter code → see authenticated state.

### Implementation for User Story 1

- [x] T007 [P] [US1] Implement `generate_code(email)` in `src/auth/service.py` — use `secrets.randbelow(1000000)` zero-padded to 6 digits, invalidate all prior unused codes for that email (UPDATE access_codes SET used=1 WHERE email=? AND used=0), insert new code row with created_at=now and expires_at=now+10min, return the code string. Import from `src/auth/db.py`.
- [x] T008 [P] [US1] Implement `verify_code(email, code)` in `src/auth/service.py` — query for matching email+code where used=0 and expires_at > now, if found mark as used (used=1) and return True, else return False.
- [x] T009 [P] [US1] Implement `validate_email(email)` in `src/auth/service.py` — check email is non-empty, contains `@`, and domain matches ALLOWED_DOMAIN from config. Return (valid: bool, error_message: str).
- [x] T010 [P] [US1] Implement `send_code_email(email, code)` in `src/auth/email.py` — if SMTP_HOST is configured, send email via `smtplib.SMTP` with TLS using SMTP_* config values; if SMTP is not configured, print code to console with `print(f"[DEV] Access code for {email}: {code}")`. Use `email.mime.text.MIMEText` for message formatting.
- [x] T011 [US1] Implement login UI in `src/app.py` — replace login placeholder with two-step form: Step 1: `st.text_input("Email")` + `st.button("Send Code")` that calls `validate_email()`, then `generate_code()`, then `send_code_email()`, stores email in `st.session_state["login_email"]`, shows success message. Step 2: `st.text_input("Access Code")` + `st.button("Verify")` that calls `verify_code()`, on success sets `st.session_state["authenticated"]=True` and `st.session_state["user_email"]` and calls `st.rerun()`, on failure shows error. Include "Resend code" button.

**Checkpoint**: Full login flow works — enter email, get code from console, enter code, see authenticated page.

---

## Phase 4: User Story 2 - Session Persistence (Priority: P2)

**Goal**: Authenticated session persists across page navigation. Session expires after 8 hours of inactivity. Logout terminates session.

**Independent Test**: Log in → navigate pages → remain authenticated. Wait beyond timeout → get redirected to login. Click logout → return to login screen.

### Implementation for User Story 2

- [x] T012 [US2] Implement session timeout check in `src/auth/service.py` — add `check_session_timeout()` function that reads `st.session_state["last_activity"]`, compares with `datetime.utcnow()`, returns True if expired (delta > SESSION_TIMEOUT_HOURS). Add `update_activity()` function that sets `st.session_state["last_activity"] = datetime.utcnow()`.
- [x] T013 [US2] Implement `logout()` in `src/auth/service.py` — clear `st.session_state["authenticated"]`, `st.session_state["user_email"]`, `st.session_state["login_time"]`, `st.session_state["last_activity"]`, then call `st.rerun()`.
- [x] T014 [US2] Integrate session management into `src/app.py` — on every page load for authenticated users: call `update_activity()`, call `check_session_timeout()` and if expired clear session and `st.rerun()` to login. Set `st.session_state["login_time"]` and `st.session_state["last_activity"]` on successful login in T011. Add logout button in sidebar: `st.sidebar.button("Log out", on_click=logout)`.

**Checkpoint**: Session persists across reruns. Logout works. Timeout logic correct (test by temporarily setting timeout to seconds).

---

## Phase 5: User Story 3 - Code Expiry and Rate Limiting (Priority: P3)

**Goal**: Expired codes are rejected. Rate limiting blocks excessive code requests (max 5 per email per 15 minutes).

**Independent Test**: Request a code, wait >10min (or set short expiry for test), enter code → rejected. Request 6 codes rapidly → 6th blocked with "try again later" message.

### Implementation for User Story 3

- [x] T015 [US3] Implement `check_rate_limit(email)` in `src/auth/service.py` — query COUNT of access_codes where email=? AND created_at > (now - RATE_LIMIT_WINDOW_MINUTES). Return (allowed: bool, remaining: int). If count >= RATE_LIMIT_MAX, return (False, 0).
- [x] T016 [US3] Integrate rate limiting into login flow in `src/app.py` — before calling `generate_code()` in Step 1, call `check_rate_limit(email)`. If blocked, show `st.error("Too many code requests. Please try again in X minutes.")` and disable the send button. Also update `verify_code()` error message to distinguish between "incorrect code" and "code expired — please request a new one" by checking if the code exists but is expired vs not found.

**Checkpoint**: Expired codes rejected with specific message. Rate limit kicks in after 5 requests. Clear messaging for both cases.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and hardening

- [x] T017 Add `.gitignore` entries for `auth.db`, `.env`, `__pycache__/`, `*.pyc`, `.venv/`
- [x] T018 Verify all error messages are user-friendly: domain rejection, invalid code, expired code, rate limit exceeded, SMTP failure fallback
- [x] T019 Run quickstart.md validation — confirm demo flow works end-to-end per quickstart steps

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on T001, T004 (directory + config)
- **US1 (Phase 3)**: Depends on T005, T006 (db + app entry point)
- **US2 (Phase 4)**: Depends on US1 completion (need working login to test sessions)
- **US3 (Phase 5)**: Depends on US1 completion (need working login to test rate limits)
- **Polish (Phase 6)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (Phase 2) only
- **User Story 2 (P2)**: Depends on US1 (session requires successful login)
- **User Story 3 (P3)**: Depends on US1 (rate limiting applies to login flow). Independent of US2.

### Within Each User Story

- Service functions before UI integration
- `src/auth/service.py` before `src/app.py` modifications

### Parallel Opportunities

- T002, T003, T004 can all run in parallel (different files)
- T007, T008, T009, T010 can all run in parallel (different functions/files, no interdependencies)
- US2 and US3 can run in parallel after US1 is complete (US2 touches session logic, US3 touches rate limit logic — different concerns)

---

## Parallel Example: Setup Phase

```bash
# Launch all setup tasks together:
Task: "Create requirements.txt"
Task: "Create .env.example"
Task: "Create src/config.py"
```

## Parallel Example: US1 Service Layer

```bash
# Launch all service functions together:
Task: "Implement generate_code() in src/auth/service.py"
Task: "Implement verify_code() in src/auth/service.py"
Task: "Implement validate_email() in src/auth/service.py"
Task: "Implement send_code_email() in src/auth/email.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T006)
3. Complete Phase 3: User Story 1 (T007-T011)
4. **STOP and VALIDATE**: Full login flow works with console code output
5. Deploy/demo if ready — app has working auth gate

### Incremental Delivery

1. Setup + Foundational → App runs, shows login placeholder
2. Add US1 → Email + code login works → Demo (MVP!)
3. Add US2 → Session persistence + logout → Demo (usable!)
4. Add US3 → Code expiry + rate limiting → Demo (hardened!)
5. Polish → Error messages, gitignore, validation

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Console code fallback makes demo work without SMTP setup
- SQLite file (`auth.db`) created automatically on first run
- All config via environment variables with sensible defaults
- Commit after each task or logical group
