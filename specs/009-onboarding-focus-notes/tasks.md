# Tasks: Onboarding Focus Notes

**Input**: Design documents from `/specs/009-onboarding-focus-notes/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Not requested in specification. Skipped.

**Organization**: Tasks grouped by user story (US1: focus notes input, US2: multiple focus areas, US3: edit & regenerate).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: No setup needed — this feature modifies existing 008 files only.

*No tasks in this phase.*

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Feature 008-onboarding-plan-generator must be fully implemented.

**⚠️ CRITICAL**: 008 must be complete before this feature begins.

*No tasks in this phase — dependency on 008 is external.*

---

## Phase 3: User Story 1 - Add Focus Notes Before Plan Generation (Priority: P1) 🎯 MVP

**Goal**: Optional "Focus notes" text area (max 1,000 chars) on the onboarding planner. When provided, plan prioritizes focus-area activities earlier, includes focus-specific key terms, and adds focus-area checkpoints. When empty, baseline 008 behavior unchanged.

**Independent Test**: Enter role/product/level + focus notes "safety-critical dispatch workflows and data validation" → Generate → Learning Plan frontloads safety activities, Key Terms includes safety terminology, Checkpoints include safety verification. Then generate without focus notes → standard plan (no focus emphasis).

### Implementation for User Story 1

- [x] T001 [US1] Add focus notes text area to `src/pages/onboarding_planner.py` — add `st.text_area("Focus notes (optional)", max_chars=1000, key="onb_focus_notes", placeholder="e.g., safety-critical workflows, compliance reporting, mobile operations")` below the level selector and above the "Generate Plan" button.
- [x] T002 [US1] Extend prompt in `src/ai/prompts/onboarding_planner.py` — add logic to conditionally append a "Priority Focus Areas" section to the system prompt when `focus_notes.strip()` is non-empty: "The manager has specified the following priority focus areas. Emphasize these topics by: (1) frontloading related activities in Week 1, (2) including focus-specific key terms, (3) adding at least one checkpoint per focus area. Focus areas: {notes}". When empty, omit this section entirely. Pass `onb_focus_notes` from session state when calling the LLM.

**Checkpoint**: Focus notes → plan emphasizes specified topics. No focus notes → baseline behavior unchanged.

---

## Phase 4: User Story 2 - Multiple Focus Areas (Priority: P2)

**Goal**: System recognizes and addresses multiple distinct topics listed in focus notes. All topics appear in Learning Plan and at least two in Checkpoints.

**Independent Test**: Focus notes "1) compliance reporting 2) mobile field operations 3) data migration" → Generate → all 3 topics in Learning Plan, at least 2 in Checkpoints.

### Implementation for User Story 2

- [x] T003 [US2] Verify multi-topic handling in `src/ai/prompts/onboarding_planner.py` — no additional code needed if T002 is implemented correctly (the LLM handles multi-topic free text naturally). Test with 3 distinct focus areas and confirm all are addressed. If needed, add explicit prompt instruction: "Address each focus area mentioned, distributing attention across all of them."

**Checkpoint**: Multiple focus areas all represented in plan output.

---

## Phase 5: User Story 3 - Edit Focus Notes and Regenerate (Priority: P3)

**Goal**: Focus notes retained after generation. Modifying notes and regenerating produces updated plan with new emphasis.

**Independent Test**: Generate with "compliance" focus → change to "mobile operations" → regenerate → output shifts emphasis.

### Implementation for User Story 3

- [x] T004 [US3] Verify focus notes persistence in `src/pages/onboarding_planner.py` — confirm `st.text_area` with `key="onb_focus_notes"` retains value after clicking "Generate Plan". On re-generate, new focus notes are passed to prompt and output reflects updated emphasis.

**Checkpoint**: Focus notes retained. Changed notes → different plan emphasis on regenerate.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases

- [x] T005 Verify vague focus notes handling — enter "make it good" as focus notes, generate, confirm plan is similar to baseline (no error, no hallucinated emphasis).
- [x] T006 Verify conflicting focus notes — enter focus notes about "iOS development" for a Support Analyst role, confirm system processes best-effort without errors.
- [x] T007 Run quickstart.md validation — confirm focus notes flow works end-to-end.

---

## Dependencies & Execution Order

### Phase Dependencies

- **External**: 008 must be fully implemented
- **US1 (Phase 3)**: Can start immediately after 008
- **US2 (Phase 4)**: Depends on US1 (focus notes must work to test multi-topic)
- **US3 (Phase 5)**: Depends on US1 (must have working focus notes to test persistence)
- **Polish (Phase 6)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on 008 only
- **User Story 2 (P2)**: Depends on US1
- **User Story 3 (P3)**: Depends on US1. Independent of US2.

### Parallel Opportunities

- T001 and T002 can run in parallel (different files: page vs prompt)
- US2 and US3 can run in parallel after US1

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete US1 (T001-T002)
2. **STOP and VALIDATE**: Focus notes influence plan output
3. Demo-ready — customizable onboarding plans

### Incremental Delivery

1. US1 → Focus notes input + prompt injection → Demo (MVP!)
2. US2 → Multi-topic verified → Demo (robust!)
3. US3 → Persistence verified → Demo (complete!)
4. Polish → Edge cases

---

## Notes

- Zero new files — all modifications to existing 008 files
- Zero new dependencies
- Same extension pattern as 005 (extends 004) and 007 (extends 006)
- Optional field — empty = baseline behavior, non-empty = enhanced
- Commit after each task
