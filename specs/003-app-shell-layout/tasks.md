# Tasks: App Shell Layout with Sidebar Navigation

**Input**: Design documents from `/specs/003-app-shell-layout/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Not requested in specification. Skipped.

**Organization**: Tasks grouped by user story (US1: sidebar switching, US2: responsive layout, US3: visual design).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create pages package and module registry

- [x] T001 Create `src/pages/` directory with `src/pages/__init__.py` — define `MODULES` as an ordered dict mapping display names to render functions: `{"Requirement Analyzer": render_placeholder, "KB Article Generator": render_placeholder, "Onboarding Planner": render_placeholder}`. Import `render_placeholder` from `src.pages.placeholder`.
- [x] T002 [P] Create `src/pages/placeholder.py` — implement `render_placeholder(module_name)` function that displays `st.header(module_name)` and `st.info(f"{module_name} — Coming soon.")`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Ensure 001-employee-auth and 002-session-logout are implemented. The auth gate and session model must exist in `src/app.py`.

**⚠️ CRITICAL**: Features 001 and 002 must be complete before shell layout integration.

*No tasks in this phase — dependency on 001/002 is external.*

---

## Phase 3: User Story 1 - Sidebar Module Switching (Priority: P1) 🎯 MVP

**Goal**: Authenticated user sees a left sidebar listing all modules. Clicking a module updates the main content area. Selected module is highlighted. Default module selected on load.

**Independent Test**: Log in → see sidebar with 3 modules → click each → main area updates → active module highlighted → sidebar stays visible.

### Implementation for User Story 1

- [x] T003 [US1] Implement shell layout in `src/app.py` — inside the authenticated branch (after auth gate): render sidebar with `st.sidebar.radio("Modules", list(MODULES.keys()), key="active_module")`, get the selected module name, dispatch to `MODULES[selected]()` to render the page content. Import `MODULES` from `src.pages`. Set default to first module in the dict.
- [x] T004 [US1] Update `src/pages/placeholder.py` — ensure `render_placeholder` is called with the module name from the dispatch: change registry in `src/pages/__init__.py` to use `lambda` or `functools.partial` so each entry passes its module name, e.g., `{"Requirement Analyzer": lambda: render_placeholder("Requirement Analyzer"), ...}`.

**Checkpoint**: App shows sidebar with 3 modules. Clicking each shows correct placeholder. Active module highlighted by radio button.

---

## Phase 4: User Story 2 - Responsive Layout (Priority: P2)

**Goal**: Sidebar collapses on screens < 768px. Main content uses full width when sidebar collapsed.

**Independent Test**: Resize browser from desktop to mobile width. Sidebar collapses to hamburger toggle. Content fills screen. Toggle sidebar — module switching still works.

### Implementation for User Story 2

- [x] T005 [US2] Verify Streamlit's built-in responsive sidebar collapse works correctly in `src/app.py` — no code changes expected (Streamlit handles this natively). Test by resizing browser and confirm sidebar collapses with hamburger toggle. If needed, set `st.set_page_config(layout="wide")` in `src/app.py` to ensure content area uses full width.

**Checkpoint**: Sidebar collapses on narrow screens. Hamburger toggle works. Content fills available width.

---

## Phase 5: User Story 3 - Clean Visual Design (Priority: P3)

**Goal**: Clear visual separation between sidebar and content. Consistent typography and spacing across modules.

**Independent Test**: Navigate all modules. Sidebar has distinct background. Font sizes consistent. No visual clutter.

### Implementation for User Story 3

- [x] T006 [US3] Add visual separation in `src/app.py` sidebar — add `st.sidebar.divider()` between the module radio selector and the sign-out button (from 002). Verify Streamlit's default sidebar styling provides distinct background against main content. No custom CSS needed (deferred to 013-branded-theme).

**Checkpoint**: Sidebar visually distinct from content. Divider separates navigation from sign-out. Consistent look across modules.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation

- [x] T007 Verify edge case: single module in registry — temporarily reduce `MODULES` dict to one entry in `src/pages/__init__.py`, confirm sidebar still renders with single highlighted item. Restore full list.
- [x] T008 Run quickstart.md validation — confirm adding a new module by adding one import + one dict entry in `src/pages/__init__.py` works as documented.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately (T001-T002)
- **Foundational (Phase 2)**: External — 001 + 002 must be complete
- **US1 (Phase 3)**: Depends on T001, T002 (registry + placeholder) and 001/002 (auth gate in app.py)
- **US2 (Phase 4)**: Depends on US1 (shell must exist to test responsiveness)
- **US3 (Phase 5)**: Depends on US1 and 002 (divider between nav and sign-out)
- **Polish (Phase 6)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Setup + external 001/002
- **User Story 2 (P2)**: Depends on US1 (layout must exist)
- **User Story 3 (P3)**: Depends on US1 + 002 (sign-out button placement)

### Within Each User Story

- Registry + placeholder before app.py integration

### Parallel Opportunities

- T001 and T002 can run in parallel (different files)
- US2 and US3 can run in parallel after US1 (different concerns — responsive vs visual)

---

## Parallel Example: Setup Phase

```bash
# Launch setup tasks together:
Task: "Create src/pages/__init__.py with MODULES registry"
Task: "Create src/pages/placeholder.py with render_placeholder()"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 3: User Story 1 (T003-T004)
3. **STOP and VALIDATE**: Sidebar switching works with placeholders
4. Demo-ready — shell layout functional

### Incremental Delivery

1. Setup → Registry + placeholder ready
2. US1 → Sidebar module switching → Demo (MVP!)
3. US2 → Responsive verified → Demo (mobile-ready!)
4. US3 → Visual separation → Demo (polished!)
5. Polish → Edge cases validated

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Zero new dependencies — uses only Streamlit built-ins
- `MODULES` dict in `src/pages/__init__.py` is the single registration point for all modules
- Future modules (004, 006, 008) replace placeholder entries with real render functions
- Responsive sidebar is free from Streamlit — no custom CSS
- Commit after each task
