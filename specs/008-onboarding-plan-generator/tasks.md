# Tasks: Onboarding Plan Generator

**Input**: Design documents from `/specs/008-onboarding-plan-generator/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Not requested in specification. Skipped.

**Organization**: Tasks grouped by user story (US1: generate plan, US2: copy plan, US3: adjust & regenerate).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create prompt file and add config constant

- [x] T001 [P] Create system prompt in `src/ai/prompts/onboarding_planner.py` — define `SYSTEM_PROMPT` string instructing the LLM to generate a 2-week onboarding plan with 5 Markdown sections (## What It Is — product overview, ## Why It Matters — value framed for the role, ## Key Terms — minimum 5 term-definition pairs, ## Learning Plan — Day 1-10 schedule with specific activities per day organized as Week 1 and Week 2, ## Checkpoints — minimum 2 assessment items at end of each week). Include level-adjustment instructions: Beginner = start with fundamentals no assumed knowledge, Intermediate = assume basics focus on workflows, Advanced = skip basics focus on expert workflows. Include instruction for unknown roles: "If the role or product is not recognized, generate based on best understanding and note this in the output." Add note about generic resource references.
- [x] T002 [P] Add `EXPERIENCE_LEVELS` constant to `src/config.py` — list: `["Beginner", "Intermediate", "Advanced"]`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Features 001 (auth), 003 (shell), 004 (shared AI client) must be complete.

**⚠️ CRITICAL**: `src/ai/client.py` and `src/pages/__init__.py` must exist.

*No tasks in this phase — dependency on 001/003/004 is external.*

---

## Phase 3: User Story 1 - Generate 2-Week Learning Plan (Priority: P1) 🎯 MVP

**Goal**: User enters role (free text), product (free text), level (selectbox), clicks "Generate Plan", sees structured 5-section onboarding plan. Validation: all fields required. Loading spinner. 30s timeout.

**Independent Test**: Enter "QA Engineer" / "Computer Aided Dispatch" / "Beginner" → Generate Plan → see 5 sections with beginner-level day-by-day schedule.

### Implementation for User Story 1

- [x] T003 [US1] Create `src/pages/onboarding_planner.py` with `render()` function — display `st.header("Onboarding Plan Generator")`, `st.text_input("Role", key="onb_role", placeholder="e.g., Support Analyst, QA Engineer")`, `st.text_input("Product", key="onb_product", placeholder="e.g., Records Management System, Computer Aided Dispatch")`, `st.selectbox("Experience Level", EXPERIENCE_LEVELS, key="onb_level")`, `st.button("Generate Plan")`. On click: validate all 3 fields non-empty (`st.error` listing missing fields if any empty), call LLM via `get_client()` with system prompt (injecting role, product, level as user message) inside `st.spinner("Generating onboarding plan...")`, handle 30s timeout with `st.error`, store result in `st.session_state["onb_plan_result"]`. Display result via `st.markdown(result)`.
- [x] T004 [US1] Register module in `src/pages/__init__.py` — replace placeholder entry for "Onboarding Planner" with import of `render` from `src.pages.onboarding_planner` and map in `MODULES` dict.

**Checkpoint**: Enter role/product/level → Generate → see 5-section plan. Empty fields rejected. Spinner shown. Timeout handled.

---

## Phase 4: User Story 2 - Copy Generated Plan (Priority: P2)

**Goal**: "Copy plan" button copies entire plan (markdown) to clipboard in one click.

**Independent Test**: Generate a plan → click "Copy plan" → paste → all 5 sections present with formatting.

### Implementation for User Story 2

- [x] T005 [US2] Add "Copy plan" button to `src/pages/onboarding_planner.py` — below the generated output, add copy mechanism using `st.code(result, language="markdown")` with built-in copy icon, or `st.button("Copy plan")` with clipboard helper. Copy the full `onb_plan_result`. (To be replaced by 010-copy-download-export later.)

**Checkpoint**: Copy works. Pasted content matches displayed plan.

---

## Phase 5: User Story 3 - Adjust Inputs and Regenerate (Priority: P3)

**Goal**: Input fields retain values after generation. User can change inputs and regenerate. New plan replaces previous.

**Independent Test**: Generate plan → change level from "Beginner" to "Intermediate" → Generate again → output updates with more advanced content. Previous plan gone.

### Implementation for User Story 3

- [x] T006 [US3] Verify input persistence in `src/pages/onboarding_planner.py` — confirm `st.text_input` and `st.selectbox` with `key` params retain values after clicking "Generate Plan". On re-generate, overwrite `st.session_state["onb_plan_result"]` with new result. Verify previous output cleared before showing spinner.

**Checkpoint**: Inputs retained. Level change → different plan content. Re-generate replaces output.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases and validation

- [x] T007 Verify unknown role/product handling — enter a made-up role like "Widget Coordinator" and product "Fantasy System", generate plan, confirm LLM produces best-effort output without errors.
- [x] T008 Verify level differentiation — generate plans for same role/product at all 3 levels, confirm "Beginner" starts with fundamentals and "Advanced" skips to expert content.
- [x] T009 Run quickstart.md validation — confirm full flow works end-to-end.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately (T001-T002)
- **Foundational (Phase 2)**: External — 001/003/004 must be complete
- **US1 (Phase 3)**: Depends on T001-T002 (prompt + config) and 001/003/004
- **US2 (Phase 4)**: Depends on US1 (output must exist to copy)
- **US3 (Phase 5)**: Depends on US1 (must have working generate to test re-generate)
- **Polish (Phase 6)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Setup + external 001/003/004
- **User Story 2 (P2)**: Depends on US1
- **User Story 3 (P3)**: Depends on US1. Independent of US2.

### Parallel Opportunities

- T001 and T002 can run in parallel (different files)
- US2 and US3 can run in parallel after US1

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 3: User Story 1 (T003-T004)
3. **STOP and VALIDATE**: Role/product/level → Generate → 5-section plan
4. Demo-ready — third AI module functional

### Incremental Delivery

1. Setup → Prompt + config ready
2. US1 → Core generate flow → Demo (MVP!)
3. US2 → Copy plan → Demo (shareable!)
4. US3 → Re-generate → Demo (complete!)
5. Polish → Edge cases verified

---

## Notes

- Zero new dependencies — reuses `openai` and shared `ai/client.py` from 004
- Same pattern as 004 and 006: page file + prompt file + module registration
- Role and Product are free-text (not dropdowns) per spec — broad range of titles/products
- Output is non-editable (unlike 006) — displayed via `st.markdown()`
- Commit after each task
