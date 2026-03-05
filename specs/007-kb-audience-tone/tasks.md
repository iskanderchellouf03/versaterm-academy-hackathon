# Tasks: KB Audience & Tone Selection

**Input**: Design documents from `/specs/007-kb-audience-tone/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Not requested in specification. Skipped.

**Organization**: Tasks grouped by user story (US1: audience selector, US2: tone selector, US3: combined context).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add constants for audience and tone options

- [x] T001 Add `AUDIENCES` and `TONES` constants to `src/config.py` — `AUDIENCES` is a dict mapping name to prompt description (e.g., `{"Internal": "Write for internal employees. Use company jargon, reference internal tools, assume product knowledge.", "External": "Write for external customers. Use plain language, avoid internal jargon, provide full context.", "Support": "Write for support agents. Use troubleshooting structure, step-by-step resolution, reference ticket workflows and escalation."}`). `TONES` is a dict (e.g., `{"Formal": "Use professional third-person voice. Passive voice acceptable. No contractions or colloquialisms.", "Conversational": "Use friendly second-person voice ('you'). Contractions OK. Approachable and warm.", "Concise": "Minimize prose. Use bullet lists, imperative voice, short sentences. Quick-reference style."}`).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Feature 006-kb-article-generator must be fully implemented.

**⚠️ CRITICAL**: 006 must be complete before this feature begins.

*No tasks in this phase — dependency on 006 is external.*

---

## Phase 3: User Story 1 - Select Target Audience (Priority: P1) 🎯 MVP

**Goal**: User selects audience (Internal/External/Support) via dropdown. Generated article reflects audience-specific language, assumptions, and detail level. Default: Internal.

**Independent Test**: Paste same notes → generate with "Internal" → uses jargon. Generate with "External" → uses plain language. Outputs differ meaningfully.

### Implementation for User Story 1

- [x] T002 [US1] Add audience dropdown to `src/pages/kb_article_generator.py` — add `st.selectbox("Target Audience", list(AUDIENCES.keys()), key="kb_audience")` above the "Generate" button. Import `AUDIENCES` from `src.config`.
- [x] T003 [US1] Extend prompt in `src/ai/prompts/kb_article_generator.py` — add a `build_kb_context(audience, tone)` function that appends an "Audience & Style" section to the system prompt: "Target audience: {audience}. {description}." Pass `kb_audience` from session state when calling the LLM in the page renderer.

**Checkpoint**: Select "External" → generate → article uses plain customer-friendly language. Select "Internal" → uses jargon. Default is "Internal".

---

## Phase 4: User Story 2 - Select Tone (Priority: P2)

**Goal**: User selects tone (Formal/Conversational/Concise) via dropdown. Article writing style matches selected tone. Default: Formal.

**Independent Test**: Same input + "External" audience → generate with "Formal" → third-person professional. Generate with "Conversational" → friendly "you" style. Outputs differ in style.

### Implementation for User Story 2

- [x] T004 [US2] Add tone dropdown to `src/pages/kb_article_generator.py` — add `st.selectbox("Tone", list(TONES.keys()), key="kb_tone")` below the audience selector and above "Generate". Import `TONES` from `src.config`.
- [x] T005 [US2] Extend `build_kb_context()` in `src/ai/prompts/kb_article_generator.py` — when `tone` is provided, append tone instruction: "Writing tone: {tone}. {description}." Add explicit override instruction: "Regardless of the input text's tone or style, the output MUST use the selected tone." Pass `kb_tone` from session state when calling the LLM.

**Checkpoint**: Select "Concise" → article uses bullet lists, imperative voice. Select "Formal" → third-person, professional. Default is "Formal".

---

## Phase 5: User Story 3 - Combined Audience + Tone Context (Priority: P3)

**Goal**: Audience and tone work together to produce intersection-specific output (e.g., "Support" + "Concise" = compact troubleshooting quick-reference).

**Independent Test**: "Support" + "Concise" → compact troubleshooting bullets. "External" + "Conversational" → friendly customer FAQ. Both differ from either dimension alone.

### Implementation for User Story 3

- [x] T006 [US3] Verify combined context in `src/ai/prompts/kb_article_generator.py` — ensure `build_kb_context()` includes both audience and tone in a single prompt section so the LLM processes both simultaneously. No additional code needed if T003 and T005 are implemented correctly — just verify all 9 combinations produce differentiated output by testing at least 2 contrasting combinations.

**Checkpoint**: All 9 combinations valid. "External" + "Conversational" ≠ "Internal" + "Formal" for same input.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases and validation

- [x] T007 Verify selections persist across re-generations in `src/pages/kb_article_generator.py` — confirm `st.selectbox` with `key` params retain audience and tone values after clicking "Generate".
- [x] T008 Verify edge case: informal input + "Formal" tone — paste very casual notes, select "Formal", generate, confirm output is formal regardless of input style.
- [x] T009 Run quickstart.md validation — confirm audience + tone flow works end-to-end.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately (T001)
- **Foundational (Phase 2)**: External — 006 must be complete
- **US1 (Phase 3)**: Depends on T001 (constants) and 006
- **US2 (Phase 4)**: Depends on T001 (constants) and 006. Can develop in parallel with US1 at code level.
- **US3 (Phase 5)**: Depends on US1 + US2 (both selectors must exist)
- **Polish (Phase 6)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Setup + external 006
- **User Story 2 (P2)**: Depends on Setup + external 006. Independent of US1 at code level.
- **User Story 3 (P3)**: Depends on US1 + US2

### Parallel Opportunities

- T002 and T004 are both UI additions to the same file — safer sequential but logically independent
- T003 and T005 modify the same prompt function — must be sequential

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 3: User Story 1 (T002-T003)
3. **STOP and VALIDATE**: Audience dropdown influences output
4. Demo-ready — audience-aware KB articles

### Incremental Delivery

1. Setup → Constants ready
2. US1 → Audience selector → Demo (MVP!)
3. US2 → Tone selector → Demo (style-aware!)
4. US3 → Combined verified → Demo (complete!)
5. Polish → Persistence, edge cases

---

## Notes

- Zero new files — all modifications to existing 006 files + config.py
- Zero new dependencies
- Same pattern as 005 extending 004 (dropdowns + prompt context injection)
- `build_kb_context()` is the single integration point
- All 9 audience × tone combinations are valid, no restrictions
- Commit after each task
