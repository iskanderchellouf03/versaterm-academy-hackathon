# Tasks: Professional Branded Theme

**Input**: Design documents from `/specs/013-branded-theme/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Not requested in specification. Visual verification only.

**Organization**: Tasks grouped by user story (US1: branding header, US2: color palette, US3: typography).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create directory structure, configuration constants, and placeholder assets

- [x] T001 Create `src/theme/` package with `src/theme/__init__.py`
- [x] T002 [P] Create `src/assets/` directory and add placeholder `src/assets/logo.png`
- [x] T003 [P] Add BRAND_* configuration constants (BRAND_LOGO_PATH, BRAND_TITLE, BRAND_SUBTITLE, BRAND_PRIMARY_COLOR, BRAND_SIDEBAR_BG, BRAND_SIDEBAR_TEXT, BRAND_BG_COLOR, BRAND_SECONDARY_BG, BRAND_TEXT_COLOR) to `src/config.py`
- [x] T004 [P] Create `.streamlit/config.toml` with `[theme]` section (primaryColor=#1B4F72, backgroundColor=#FFFFFF, secondaryBackgroundColor=#F8F9FA, textColor=#2C3E50, font="sans serif")

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No foundational blockers — this feature has no data layer or auth requirements. Setup phase outputs are sufficient.

**⚠️ CRITICAL**: Ensure `src/config.py` exists (from feature 001 or earlier). If not, create it in T003.

**Checkpoint**: Configuration and directories ready — user story implementation can begin.

---

## Phase 3: User Story 1 - Branded Header with Logo, Title, and Subtitle (Priority: P1) 🎯 MVP

**Goal**: Display logo, application title, and subtitle on the login screen and in the sidebar on all authenticated pages. Graceful fallback if logo is missing.

**Independent Test**: Open the login screen — confirm logo, title, subtitle are visible. Log in and navigate modules — confirm logo and title appear consistently in sidebar. Delete logo file — confirm title/subtitle still render with no broken image.

### Implementation for User Story 1

- [x] T005 [US1] Implement `render_branding(show_subtitle=True)` function in `src/components/branding.py` — display logo via `st.image()` (with `os.path.exists()` check for graceful fallback), title via `st.markdown()`, and subtitle (conditionally). Logo constrained to max width (48px sidebar, 80px login). Read all values from `src/config.py` constants.
- [x] T006 [US1] Integrate `render_branding()` into `src/app.py` — call in sidebar (with `show_subtitle=False`) for authenticated pages, and on login screen (with `show_subtitle=True`) for unauthenticated state.

**Checkpoint**: Logo, title, and subtitle visible on login and all authenticated pages. Graceful degradation when logo missing.

---

## Phase 4: User Story 2 - Neutral Professional Color Palette (Priority: P2)

**Goal**: Apply a consistent navy/charcoal corporate color palette across all pages — sidebar dark background, light sidebar text, WCAG AA compliant contrast throughout.

**Independent Test**: Navigate login screen, sidebar, and modules. Confirm sidebar is dark charcoal (#2C3E50), sidebar text is light (#ECF0F1), buttons use navy accent (#1B4F72), content area is white. Verify text is readable on all backgrounds.

### Implementation for User Story 2

- [x] T007 [US2] Implement `inject_theme_css()` function in `src/theme/css.py` — generate a `<style>` block with CSS for sidebar background (`[data-testid="stSidebar"]` → #2C3E50), sidebar text color (`[data-testid="stSidebar"] *` → #ECF0F1), and link/button accent colors. Use BRAND_* constants from `src/config.py`. Call via `st.markdown(unsafe_allow_html=True)`.
- [x] T008 [US2] Integrate `inject_theme_css()` into `src/app.py` — call once at the top of the app (before any page content renders) so CSS applies to all pages including login.

**Checkpoint**: Color palette consistent across all pages. Sidebar dark, content light, buttons navy. WCAG AA contrast met.

---

## Phase 5: User Story 3 - Consistent Typography (Priority: P3)

**Goal**: Apply a single professional font family and consistent heading hierarchy (H1 2rem/700, H2 1.5rem/600, H3 1.25rem/600, body 1rem/400) across all pages.

**Independent Test**: Navigate across all modules. Confirm same font family everywhere, heading sizes are consistent, body text is readable. Compare H1/H2/H3 sizes between modules — they should match.

### Implementation for User Story 3

- [x] T009 [US3] Extend `inject_theme_css()` in `src/theme/css.py` — add CSS rules for `body` font-family (system font stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif), `h1` (2rem, 700, #1B4F72), `h2` (1.5rem, 600, #1B4F72), `h3` (1.25rem, 600, #1B4F72) using BRAND_PRIMARY_COLOR from config.

**Checkpoint**: All pages use same font family. Heading sizes consistent across modules.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and edge case handling

- [x] T010 Verify `.streamlit/config.toml` theme values match `src/config.py` BRAND_* constants — ensure no conflicts between config.toml colors and CSS injection
- [x] T011 Verify graceful degradation: delete `src/assets/logo.png`, run app, confirm no errors and title/subtitle still render. Restore logo file afterward.
- [x] T012 Run quickstart.md validation — confirm all code locations listed in quickstart.md match actual file paths

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: N/A — no foundational blockers
- **US1 (Phase 3)**: Depends on T001-T004 (setup). Can start after setup.
- **US2 (Phase 4)**: Depends on T001, T003 (theme package + config). Independent of US1.
- **US3 (Phase 5)**: Depends on T007 (extends the CSS injection function from US2). Must follow US2.
- **Polish (Phase 6)**: Depends on all user stories complete.

### User Story Dependencies

- **User Story 1 (P1)**: Independent — uses `src/components/branding.py` and `src/config.py`
- **User Story 2 (P2)**: Independent — uses `src/theme/css.py` and `src/config.py`
- **User Story 3 (P3)**: Depends on US2 — extends the `inject_theme_css()` function created in US2

### Within Each User Story

- Config constants before component code
- Component code before app.py integration
- US2 (color CSS) before US3 (typography CSS, same file)

### Parallel Opportunities

- T002, T003, T004 can all run in parallel (different files)
- T005 and T007 can run in parallel (different files: branding.py vs css.py)
- T006 and T008 both modify app.py — must be sequential

---

## Parallel Example: Setup Phase

```bash
# Launch all setup tasks together:
Task: "Create src/assets/ directory and add placeholder logo.png"
Task: "Add BRAND_* constants to src/config.py"
Task: "Create .streamlit/config.toml with theme section"
```

## Parallel Example: US1 + US2 Components

```bash
# Launch component implementations together (different files):
Task: "Implement render_branding() in src/components/branding.py"
Task: "Implement inject_theme_css() in src/theme/css.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 3: User Story 1 (T005-T006)
3. **STOP and VALIDATE**: Logo, title, subtitle visible on all pages
4. Deploy/demo if ready — app looks branded even without color/font polish

### Incremental Delivery

1. Setup → directories, config, config.toml ready
2. Add US1 → Logo + title + subtitle everywhere → Demo (MVP!)
3. Add US2 → Professional color palette → Demo (polished!)
4. Add US3 → Consistent typography → Demo (complete!)
5. Polish → Edge cases validated

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Zero new dependencies — uses only Streamlit built-ins
- All branding values read from `src/config.py` (single source of truth per FR-010)
- CSS injection uses `st.markdown(unsafe_allow_html=True)` — standard Streamlit pattern
- Commit after each task or logical group
