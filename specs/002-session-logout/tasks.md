# Tasks: Session Sign-Out

**Input**: Design documents from `/specs/002-session-logout/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Not requested in specification. Skipped.

**Organization**: Tasks grouped by user story (US1: sign-out action, US2: visibility & accessibility).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: No setup needed — this feature modifies existing files from 001-employee-auth.

*No tasks in this phase.*

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Ensure 001-employee-auth session model exists.

**⚠️ CRITICAL**: Feature 001-employee-auth must be implemented first. The session state keys (`authenticated`, `user_email`) and the auth gate in `src/app.py` must exist.

*No tasks in this phase — dependency on 001 is external.*

---

## Phase 3: User Story 1 - Explicit Sign-Out (Priority: P1) 🎯 MVP

**Goal**: Clicking "Sign out" terminates session, clears all auth keys, redirects to login screen. Post-logout access to protected pages is blocked.

**Independent Test**: Log in → click "Sign out" → see login screen. Try browser back button → still on login screen. Try navigating to a protected URL → redirected to login.

### Implementation for User Story 1

- [x] T001 [US1] Implement `logout()` function in `src/auth/service.py` — define a list of auth-related session keys (`authenticated`, `user_email`, `login_time`, `last_activity`, `login_email`), iterate and delete each from `st.session_state` if present, then call `st.rerun()`.
- [x] T002 [US1] Add sign-out button to `src/app.py` — inside the authenticated branch (after auth gate check), add `st.sidebar.button("Sign out", on_click=logout)` at the bottom of the sidebar. Import `logout` from `src.auth.service`.

**Checkpoint**: Click "Sign out" → session cleared → login screen shown. Back button → still login screen.

---

## Phase 4: User Story 2 - Sign-Out Visibility and Accessibility (Priority: P2)

**Goal**: "Sign out" button is persistently visible on every authenticated page without scrolling. Positioned in sidebar, clearly labeled.

**Independent Test**: Navigate through all modules while authenticated. Confirm "Sign out" is visible on every page. Resize browser — confirm button is still accessible.

### Implementation for User Story 2

- [x] T003 [US2] Ensure sign-out button placement in `src/app.py` is at the bottom of the sidebar after all navigation elements — use `st.sidebar.divider()` before the button to visually separate it from module navigation. Verify the button text is "Sign out" (not icon-only, per FR-006).

**Checkpoint**: "Sign out" visible on all authenticated pages, separated from navigation, labeled clearly.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Edge case handling

- [x] T004 Verify sign-out during expired session in `src/app.py` — if session is already expired when "Sign out" is clicked, ensure no error occurs (logout function handles missing keys gracefully via `if key in st.session_state` checks before deletion).

---

## Dependencies & Execution Order

### Phase Dependencies

- **External**: 001-employee-auth must be fully implemented
- **US1 (Phase 3)**: Can start immediately after 001 is complete
- **US2 (Phase 4)**: Depends on T002 (button must exist to refine placement)
- **Polish (Phase 5)**: Depends on US1 complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on 001-employee-auth only
- **User Story 2 (P2)**: Depends on US1 (button must exist to verify placement)

### Within Each User Story

- Service function (T001) before UI integration (T002)

### Parallel Opportunities

- Limited — only 4 tasks total, mostly sequential
- T001 can be developed independently from T002 (different files)

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Implement `logout()` in `src/auth/service.py` (T001)
2. Add button to sidebar in `src/app.py` (T002)
3. **STOP and VALIDATE**: Sign-out works end-to-end
4. Demo-ready

### Incremental Delivery

1. US1 → Working sign-out → Demo (MVP!)
2. US2 → Polished placement → Demo (complete!)
3. Polish → Edge cases verified

---

## Notes

- Zero new files — all modifications to existing 001 files
- Zero new dependencies
- `logout()` uses key-by-key deletion (not `st.session_state.clear()`) to preserve non-auth state from other features
- Streamlit's rerun model inherently handles back-button protection
- Commit after each task
