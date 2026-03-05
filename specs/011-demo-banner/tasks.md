# Tasks: Demo Scope Banner

**Input**: Design documents from `/specs/011-demo-banner/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Not requested in specification. Skipped.

**Organization**: Tasks grouped by user story (US1: persistent banner on all pages, US2: banner dismissibility).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add banner text constant to config

- [x] T001 Add `DEMO_BANNER_TEXT` constant to `src/config.py` — value: `"Demo — This is a prototype. No data is persisted. All information is local to your current session."`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Feature 003-app-shell-layout must be complete (provides `app.py` and page structure). Feature 010 must be complete (provides `src/components/__init__.py`).

**⚠️ CRITICAL**: `src/app.py` and `src/components/__init__.py` must exist.

*No tasks in this phase — dependency on 003/010 is external.*

---

## Phase 3: User Story 1 - Persistent Demo Banner on All Pages (Priority: P1) 🎯 MVP

**Goal**: Amber/yellow banner fixed at top of every page (including login). Contains demo/prototype text and no-persistence message. Does not overlap functional UI. Visible on scroll. No dismiss control yet.

**Independent Test**: Open the app → banner visible at top with demo text. Navigate between modules → banner stays. Scroll down → banner stays fixed. No buttons/inputs obscured.

### Implementation for User Story 1

- [x] T002 [US1] Create `src/components/demo_banner.py` with `render_demo_banner()` function — import `DEMO_BANNER_TEXT` from `src.config` and `st.session_state`. Use `st.markdown(html, unsafe_allow_html=True)` to render a `<div>` styled with inline CSS: `position: fixed; top: 0; left: 0; width: 100%; background-color: #F39C12; color: #1A1A1A; text-align: center; padding: 8px 16px; z-index: 999; font-size: 14px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);`. Text content is `DEMO_BANNER_TEXT`. Also inject a `<style>` block adding `padding-top: 45px` to `.stApp` to prevent content overlap (FR-004). Max height constraint via CSS to keep under 15% viewport (FR-009).
- [x] T003 [US1] Integrate banner into `src/app.py` — import `render_demo_banner` from `src.components.demo_banner` and call it at the very top of the `main()` function, before the auth gate, so it appears on the login screen too (FR-001, R5).

**Checkpoint**: Banner visible on all pages including login. Fixed on scroll. Amber background. Content not obscured. Readable on narrow screens.

---

## Phase 4: User Story 2 - Banner Dismissibility (Priority: P2)

**Goal**: Small "✕" dismiss control on the banner hides it for the current session. Banner reappears on new session (new tab or re-auth). Dismiss state stored in `st.session_state["banner_dismissed"]`.

**Independent Test**: Click dismiss → banner hidden → navigate modules → stays hidden. Close tab → reopen → banner reappears.

### Implementation for User Story 2

- [x] T004 [US2] Add dismiss logic to `render_demo_banner()` in `src/components/demo_banner.py` — at the start of `render_demo_banner()`, check `st.session_state.get("banner_dismissed", False)`: if True, return immediately (skip rendering). Add a `st.button("✕", key="dismiss_banner")` rendered via Streamlit columns: use `st.columns([0.95, 0.05])` where col1 renders the banner HTML and col2 renders the dismiss button. On button click, set `st.session_state["banner_dismissed"] = True` and call `st.rerun()`. Alternatively, embed the dismiss as part of the HTML/CSS banner with a small clickable "✕" at the right side, and use a separate `st.button` hidden approach. The key requirement is: session state flag controls visibility, button triggers the flag.

**Checkpoint**: Dismiss hides banner for session. Navigation keeps it hidden. New session shows banner again.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases and validation

- [x] T005 Verify banner does not overlap UI — test all 3 AI modules (requirement analyzer, KB article generator, onboarding planner) and confirm no buttons, inputs, or output areas are obscured by the banner. Adjust `padding-top` value if needed.
- [x] T006 Verify banner on narrow screens — resize browser to mobile width, confirm banner text wraps but remains readable and does not exceed 15% viewport height.
- [x] T007 Run quickstart.md validation — confirm banner visible on login, all modules, dismiss works, reappears on new session.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately (T001)
- **Foundational (Phase 2)**: External — 003/010 must be complete
- **US1 (Phase 3)**: Depends on T001 (config constant) and 003/010
- **US2 (Phase 4)**: Depends on US1 (banner must exist to add dismiss)
- **Polish (Phase 5)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Setup + external 003/010
- **User Story 2 (P2)**: Depends on US1

### Parallel Opportunities

- T001 can run alongside external prerequisite work
- T002 and T003 are sequential (component must exist before integration)
- US2 depends on US1 — no parallelism between stories

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 3: User Story 1 (T002-T003)
3. **STOP and VALIDATE**: Banner visible on all pages, fixed on scroll, no overlap
4. Demo-ready — stakeholders see "this is a demo" immediately

### Incremental Delivery

1. Setup → Config constant ready
2. US1 → Fixed banner on all pages → Demo (MVP!)
3. US2 → Dismissible banner → Demo (complete!)
4. Polish → Edge cases, overlap checks

---

## Notes

- Zero new dependencies — pure `st.markdown` with inline CSS
- Small CSS injection (~10 lines) justified per constitution for fixed positioning
- Called before auth gate in `app.py` — visible on login screen
- Session state dismiss — no database, resets on new tab
- Compatible with 013-branded-theme (banner renders above themed content)
- Commit after each task
