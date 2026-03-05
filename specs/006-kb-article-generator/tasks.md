# Tasks: KB Article Generator

**Input**: Design documents from `/specs/006-kb-article-generator/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Not requested in specification. Skipped.

**Organization**: Tasks grouped by user story (US1: generate article, US2: copy article, US3: edit & regenerate).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create prompt file and add config constant

- [x] T001 [P] Create system prompt in `src/ai/prompts/kb_article_generator.py` — define `SYSTEM_PROMPT` string instructing the LLM to transform raw text into a structured KB article with 4 Markdown sections (## Title — concise under 80 chars, ## Summary — 1-2 sentences, ## Body — headings, numbered steps for procedures, clear paragraphs, remove conversational filler, ## Tags — 3-7 keywords). Include instruction to distill key information and remove irrelevant content.
- [x] T002 [P] Add `KB_INPUT_MAX_CHARS = 10000` constant to `src/config.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Features 001 (auth), 003 (shell), 004 (shared AI client) must be complete.

**⚠️ CRITICAL**: `src/ai/client.py` and `src/pages/__init__.py` must exist from 004/003.

*No tasks in this phase — dependency on 001/003/004 is external.*

---

## Phase 3: User Story 1 - Generate Structured KB Article (Priority: P1) 🎯 MVP

**Goal**: User pastes messy notes, clicks "Generate", sees structured KB article with Title, Summary, Body, Tags. Loading indicator during processing. 30s timeout. Sensitive data reminder displayed.

**Independent Test**: Paste "customer called about password reset, told them to go to settings then security then click reset link, takes 24hrs to process" → click Generate → see structured article with title, summary, step-by-step body, and tags.

### Implementation for User Story 1

- [x] T003 [US1] Create `src/pages/kb_article_generator.py` with `render()` function — display `st.header("KB Article Generator")`, `st.info("Remember to remove sensitive information (names, ticket numbers) before publishing externally.")`, `st.text_area("Paste your notes or raw text", max_chars=10000, key="kb_input_text")`, `st.button("Generate")`. On button click: validate input not empty (`st.error` if empty), call LLM via `get_client()` with system prompt + user input inside `st.spinner("Generating article...")`, handle 30s timeout with `st.error("Generation timed out. Please try again.")`, store result in `st.session_state["kb_article_result"]`. Display result via `st.markdown(result)` below input area.
- [x] T004 [US1] Register module in `src/pages/__init__.py` — replace placeholder entry for "KB Article Generator" with import of `render` from `src.pages.kb_article_generator` and map to it in the `MODULES` dict.

**Checkpoint**: Paste notes → Generate → see 4-section article. Spinner during processing. Empty input rejected. Sensitive data reminder visible.

---

## Phase 4: User Story 2 - Copy Generated Article (Priority: P2)

**Goal**: "Copy article" button copies the entire article (markdown) to clipboard in one click.

**Independent Test**: Generate an article → click "Copy article" → paste into editor → all 4 sections present with proper formatting.

### Implementation for User Story 2

- [x] T005 [US2] Add "Copy article" button to `src/pages/kb_article_generator.py` — below the generated output, add a copy mechanism. For MVP, use `st.code(result, language="markdown")` which has a built-in copy icon, or add a `st.button("Copy article")` that uses a clipboard helper. Copy the full `kb_article_result` (or `kb_article_edited` if editing is implemented).

**Checkpoint**: Copy button works. Pasted content matches displayed article with markdown formatting.

---

## Phase 5: User Story 3 - Edit and Regenerate (Priority: P3)

**Goal**: Output is editable via text_area. Input retains text for re-generation. Regenerating replaces previous output (and discards edits).

**Independent Test**: Generate article → edit output text → copy → edits preserved. Edit input → Generate again → new output replaces old (including discarding prior edits).

### Implementation for User Story 3

- [x] T006 [US3] Replace `st.markdown()` output with `st.text_area()` in `src/pages/kb_article_generator.py` — when `kb_article_result` exists, display it in `st.text_area("Generated Article (editable)", value=st.session_state.get("kb_article_result", ""), key="kb_article_edited", height=400)`. Copy button should reference `kb_article_edited` instead of `kb_article_result` so user edits are included. On re-generate, overwrite both `kb_article_result` and reset `kb_article_edited`.
- [x] T007 [US3] Verify input persistence in `src/pages/kb_article_generator.py` — confirm `st.text_area` for input uses `key="kb_input_text"` so text is retained after generation. On re-generate, overwrite previous output completely.

**Checkpoint**: Output is editable. Edits preserved when copying. Input retained. Re-generate replaces everything.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases and validation

- [x] T008 Verify character limit enforcement in `src/pages/kb_article_generator.py` — test with >10000 chars, confirm `max_chars=10000` truncates input.
- [x] T009 Run quickstart.md validation — confirm full flow works: paste notes → generate → edit → copy → re-generate.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately (T001-T002)
- **Foundational (Phase 2)**: External — 001/003/004 must be complete
- **US1 (Phase 3)**: Depends on T001-T002 (prompt + config) and 001/003/004
- **US2 (Phase 4)**: Depends on US1 (output must exist to copy)
- **US3 (Phase 5)**: Depends on US1 (must have working generate to test editing)
- **Polish (Phase 6)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Setup + external 001/003/004
- **User Story 2 (P2)**: Depends on US1
- **User Story 3 (P3)**: Depends on US1. Independent of US2.

### Parallel Opportunities

- T001 and T002 can run in parallel (different files)
- US2 and US3 can run in parallel after US1 (different concerns — copy vs edit)

---

## Parallel Example: Setup Phase

```bash
# Launch setup tasks together:
Task: "Create system prompt in src/ai/prompts/kb_article_generator.py"
Task: "Add KB_INPUT_MAX_CHARS to src/config.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 3: User Story 1 (T003-T004)
3. **STOP and VALIDATE**: Paste notes → Generate → See structured article
4. Demo-ready — second AI module functional

### Incremental Delivery

1. Setup → Prompt + config ready
2. US1 → Core generate flow → Demo (MVP!)
3. US2 → Copy article → Demo (workflow-ready!)
4. US3 → Editable output + re-generate → Demo (complete!)
5. Polish → Char limit, validation

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Zero new dependencies — reuses `openai` and shared `ai/client.py` from 004
- Same pattern as 004: page file + prompt file + module registration
- `st.text_area` for editable output is the key differentiator from 004's `st.markdown`
- Sensitive data reminder is always visible (st.info), not dismissible
- Commit after each task
