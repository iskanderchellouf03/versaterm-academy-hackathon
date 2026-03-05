# Tasks: AI Requirement Analyzer

**Input**: Design documents from `/specs/004-requirement-analyzer/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Not requested in specification. Skipped.

**Organization**: Tasks grouped by user story (US1: paste & analyze, US2: copy output, US3: iterative refinement).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create AI package, shared client, and module prompt

- [x] T001 Create `src/ai/` package with `src/ai/__init__.py` and `src/ai/prompts/` directory with `src/ai/prompts/__init__.py`
- [x] T002 [P] Add `openai` to `requirements.txt`
- [x] T003 [P] Add LLM configuration to `src/config.py` — add `OPENAI_API_KEY` (from env, required), `OPENAI_BASE_URL` (from env, default None), `OPENAI_MODEL` (from env, default "gpt-4o"), `OPENAI_TIMEOUT` (hardcoded 30), `REQ_INPUT_MAX_CHARS` (5000)
- [x] T004 [P] Implement `get_client()` in `src/ai/client.py` — return configured `openai.OpenAI` instance using `OPENAI_API_KEY`, `OPENAI_BASE_URL`, and `OPENAI_TIMEOUT` from `src/config.py`. Raise clear error if API key is not set.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Ensure 001 (auth), 003 (shell layout) are implemented. Module registry must exist.

**⚠️ CRITICAL**: Features 001, 002, 003 must be complete. The `MODULES` registry in `src/pages/__init__.py` must exist.

*No tasks in this phase — dependency on 001/002/003 is external.*

---

## Phase 3: User Story 1 - Paste and Analyze a Requirement (Priority: P1) 🎯 MVP

**Goal**: User pastes requirement text, clicks "Analyze", sees structured output with 5 sections (Rewritten Requirements, Acceptance Criteria, Test Cases, Edge Cases, Risks). Loading indicator during processing. 30s timeout with error message.

**Independent Test**: Navigate to Requirement Analyzer → paste "Users should be able to reset their password" → click Analyze → see all 5 sections populated → verify loading spinner shown during processing.

### Implementation for User Story 1

- [x] T005 [P] [US1] Create system prompt in `src/ai/prompts/requirement_analyzer.py` — define `SYSTEM_PROMPT` string instructing the LLM to analyze a requirement and produce 5 Markdown sections (## Rewritten Requirements, ## Acceptance Criteria with Given/When/Then, ## Test Cases, ## Edge Cases, ## Risks). Include formatting rules: use bullet points, be specific, flag ambiguity in Risks.
- [x] T006 [P] [US1] Create `src/pages/requirement_analyzer.py` with `render()` function — display `st.header("Requirement Analyzer")`, `st.text_area("Paste your requirement", max_chars=5000, key="req_input_text")`, `st.button("Analyze")`. On button click: validate input is not empty (show `st.error` if empty), set `req_analysis_loading=True`, call LLM via `get_client()` with system prompt + user input inside `st.spinner("Analyzing...")`, handle 30s timeout with `st.error("Analysis timed out. Please try again.")`, store result in `st.session_state["req_analysis_result"]`. Display result via `st.markdown(result)` below input area.
- [x] T007 [US1] Register module in `src/pages/__init__.py` — replace placeholder entry for "Requirement Analyzer" with import of `render` from `src.pages.requirement_analyzer` and map to it in the `MODULES` dict.
- [x] T008 [US1] Add `.env.example` entries for `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL` with descriptive comments (append to existing `.env.example` from 001)

**Checkpoint**: Full analyze flow works — paste requirement, click Analyze, see 5 sections. Spinner during processing. Timeout handled. Empty input rejected.

---

## Phase 4: User Story 2 - Copy Output Sections (Priority: P2)

**Goal**: Each output section has a copy action. "Copy all" copies the entire analysis.

**Independent Test**: Run an analysis → click copy on any section → paste into editor → content matches. Click "Copy all" → paste → all 5 sections present.

### Implementation for User Story 2

- [x] T009 [US2] Add per-section copy in `src/pages/requirement_analyzer.py` — after analysis completes, split `req_analysis_result` on `\n## ` to extract individual sections. Display each section with `st.markdown()` and a `st.button("Copy", key=f"copy_{section_name}")` that uses `st.code(section_text)` or a clipboard helper. Add a "Copy all" button at the top that copies the full `req_analysis_result`. Use `st.code()` blocks with built-in copy icon for MVP (to be replaced by 010-copy-download-export later).

**Checkpoint**: Copy per section works. Copy all works. Pasted content matches displayed output.

---

## Phase 5: User Story 3 - Iterative Refinement (Priority: P3)

**Goal**: Input field retains text after analysis. User can edit and re-analyze. New results replace previous.

**Independent Test**: Analyze a requirement → edit the text → click Analyze again → output updates to reflect changes. Previous output gone.

### Implementation for User Story 3

- [x] T010 [US3] Ensure input persistence in `src/pages/requirement_analyzer.py` — verify `st.text_area` uses `key="req_input_text"` so Streamlit session state retains the text after analysis. On re-analyze, overwrite `st.session_state["req_analysis_result"]` with new result (no history accumulation). Verify that re-running analysis clears previous output before showing spinner.

**Checkpoint**: Input retained after analysis. Re-analyze produces fresh output. No stale results shown.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Error handling, validation edge cases

- [x] T011 Handle API key missing gracefully in `src/pages/requirement_analyzer.py` — if `OPENAI_API_KEY` is not configured, show `st.warning("AI features require an API key. Set OPENAI_API_KEY in your environment.")` instead of the input form.
- [x] T012 Verify character limit enforcement in `src/pages/requirement_analyzer.py` — test with >5000 chars, confirm `st.text_area(max_chars=5000)` truncates input and optionally show `st.info` about the character limit.
- [x] T013 Run quickstart.md validation — confirm full flow works per quickstart steps with a real or mock LLM endpoint.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately (T001-T004)
- **Foundational (Phase 2)**: External — 001/002/003 must be complete
- **US1 (Phase 3)**: Depends on T001-T004 (AI package + client) and 001/002/003 (auth + shell)
- **US2 (Phase 4)**: Depends on US1 (output must exist to copy)
- **US3 (Phase 5)**: Depends on US1 (must have working analyze to test refinement)
- **Polish (Phase 6)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Setup + external 001/002/003
- **User Story 2 (P2)**: Depends on US1 (needs analysis output)
- **User Story 3 (P3)**: Depends on US1 (needs working analyze). Independent of US2.

### Within Each User Story

- Prompt before page renderer
- Page renderer before module registration

### Parallel Opportunities

- T002, T003, T004 can all run in parallel (different files)
- T005 and T006 can run in parallel (different files: prompt vs page)
- US2 and US3 can run in parallel after US1 (different concerns)

---

## Parallel Example: Setup Phase

```bash
# Launch setup tasks together:
Task: "Add openai to requirements.txt"
Task: "Add LLM config to src/config.py"
Task: "Implement get_client() in src/ai/client.py"
```

## Parallel Example: US1 Implementation

```bash
# Launch US1 component tasks together:
Task: "Create system prompt in src/ai/prompts/requirement_analyzer.py"
Task: "Create page renderer in src/pages/requirement_analyzer.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 3: User Story 1 (T005-T008)
3. **STOP and VALIDATE**: Paste → Analyze → See 5 sections
4. Demo-ready — first AI module functional

### Incremental Delivery

1. Setup → AI package + client ready
2. US1 → Core analyze flow → Demo (MVP!)
3. US2 → Copy sections → Demo (workflow-ready!)
4. US3 → Iterative refinement → Demo (complete!)
5. Polish → API key handling, char limit, validation

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- One new dependency: `openai` package (justified — no stdlib LLM client)
- `src/ai/client.py` is shared by all future AI modules (006, 008)
- System prompt in separate file for easy iteration
- `st.code()` for copy is MVP — replaced by 010-copy-download-export later
- Commit after each task
