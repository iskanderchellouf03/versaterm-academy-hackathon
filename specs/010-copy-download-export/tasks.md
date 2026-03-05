# Tasks: One-Click Copy & Markdown Download

**Input**: Design documents from `/specs/010-copy-download-export/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Not requested in specification. Skipped.

**Organization**: Tasks grouped by user story (US1: copy to clipboard, US2: download .md, US3: per-section copy).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create components package

- [x] T001 Create `src/components/` package with `src/components/__init__.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: At least one AI module (004, 006, or 008) must be implemented to test copy/download.

**⚠️ CRITICAL**: 004-requirement-analyzer must be complete (first AI module with output to copy).

*No tasks in this phase — dependency on 004 is external.*

---

## Phase 3: User Story 1 - One-Click Copy to Clipboard (Priority: P1) 🎯 MVP

**Goal**: "Copy" button next to AI output copies full markdown to clipboard. Visual "Copied!" confirmation for 2 seconds. Button disabled when no output. Fallback message if clipboard API unavailable.

**Independent Test**: Generate output in Requirement Analyzer → click "Copy" → see "Copied!" → paste into editor → full markdown with headings/lists preserved.

### Implementation for User Story 1

- [x] T002 [US1] Implement `render_copy_button(text, label="Copy")` in `src/components/copy_button.py` — generate HTML/JS via `st.components.v1.html()` that renders a styled button. On click: call `navigator.clipboard.writeText(text)`, change button text to "Copied!" for 2 seconds, then revert. Include try/catch: if clipboard unavailable, show "Unable to copy. Please select the text and copy manually (Ctrl+C)." Pass text as escaped string into the JS template. Set component height to ~40px.
- [x] T003 [US1] Integrate copy button into `src/pages/requirement_analyzer.py` — after rendering analysis output, call `render_copy_button(st.session_state.get("req_analysis_result", ""))`. Only render when `req_analysis_result` exists and `req_analysis_loading` is False. Remove any existing `st.code()` copy from 004 US2.
- [x] T004 [P] [US1] Integrate copy button into `src/pages/kb_article_generator.py` — call `render_copy_button(st.session_state.get("kb_article_edited", ""))`. Only render when output exists and not loading. Remove any existing copy mechanism from 006 US2.
- [x] T005 [P] [US1] Integrate copy button into `src/pages/onboarding_planner.py` — call `render_copy_button(st.session_state.get("onb_plan_result", ""))`. Only render when output exists and not loading. Remove any existing copy mechanism from 008 US2.

**Checkpoint**: Copy works in all 3 modules. "Copied!" confirmation shown. Button hidden when no output. Fallback on non-HTTPS.

---

## Phase 4: User Story 2 - Download as Markdown File (Priority: P2)

**Goal**: "Download" button downloads AI output as `.md` file. Filename pattern: `{module-slug}-{YYYY-MM-DD}.md`. Button disabled when no output.

**Independent Test**: Generate output → click "Download" → `.md` file saved → open in editor → matches on-screen output.

### Implementation for User Story 2

- [x] T006 [US2] Implement `render_download_button(text, module_slug)` in `src/components/download_button.py` — wrapper around `st.download_button(label="Download", data=text, file_name=f"{module_slug}-{date.today().isoformat()}.md", mime="text/markdown")`. Import `datetime.date`.
- [x] T007 [US2] Integrate download button into all 3 module pages — in `src/pages/requirement_analyzer.py` call `render_download_button(result, "requirement-analysis")`, in `src/pages/kb_article_generator.py` call `render_download_button(edited, "kb-article")`, in `src/pages/onboarding_planner.py` call `render_download_button(result, "onboarding-plan")`. Render alongside copy button, only when output exists and not loading.

**Checkpoint**: Download works in all 3 modules. Filename correct. File content matches output.

---

## Phase 5: User Story 3 - Per-Section Copy (Priority: P3)

**Goal**: Each output section (split on `\n## `) has its own copy icon. Clicking copies only that section's heading + body.

**Independent Test**: Generate multi-section output in Requirement Analyzer → click copy icon on "Test Cases" → paste → only Test Cases content.

### Implementation for User Story 3

- [x] T008 [US3] Implement `render_sections_with_copy(markdown_text)` in `src/components/copy_button.py` — split `markdown_text` on `\n## ` to extract sections (preserving `## ` prefix). For each section, render `st.markdown(section)` followed by a compact `render_copy_button(section, label="Copy section")` with smaller styling. Return the list of section names for reference.
- [x] T009 [US3] Integrate per-section copy into `src/pages/requirement_analyzer.py` — replace direct `st.markdown(result)` with `render_sections_with_copy(result)` when output exists. Keep full copy + download buttons at the top.

**Checkpoint**: Per-section copy works in Requirement Analyzer. Pasted content matches individual section only.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Consistency and edge cases

- [x] T010 Verify button disabled state across all modules — confirm Copy and Download buttons are hidden/disabled when no output exists and during generation (check `*_loading` flags).
- [x] T011 Verify KB Article Generator copies edited content — in 006, confirm `render_copy_button` uses `kb_article_edited` (user-edited text) not `kb_article_result` (original LLM output).
- [x] T012 Run quickstart.md validation — confirm copy/download works in all 3 modules end-to-end.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately (T001)
- **Foundational (Phase 2)**: External — at least 004 must be complete
- **US1 (Phase 3)**: Depends on T001 + at least one AI module
- **US2 (Phase 4)**: Depends on T001. Independent of US1 at component level.
- **US3 (Phase 5)**: Depends on US1 (reuses `render_copy_button`)
- **Polish (Phase 6)**: Depends on all user stories

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Setup + external AI modules
- **User Story 2 (P2)**: Independent of US1 (different component). Can develop in parallel.
- **User Story 3 (P3)**: Depends on US1 (extends copy_button.py)

### Parallel Opportunities

- T003, T004, T005 can run in parallel (different module pages)
- T002 and T006 can run in parallel (different component files)
- US1 and US2 component development can run in parallel

---

## Parallel Example: Module Integration

```bash
# Integrate copy button into all modules simultaneously:
Task: "Integrate copy into requirement_analyzer.py"
Task: "Integrate copy into kb_article_generator.py"
Task: "Integrate copy into onboarding_planner.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 3: US1 (T002-T005)
3. **STOP and VALIDATE**: Copy works in all 3 modules
4. Demo-ready — one-click copy to clipboard

### Incremental Delivery

1. Setup → Components package ready
2. US1 → Copy to clipboard → Demo (MVP!)
3. US2 → Download .md file → Demo (shareable!)
4. US3 → Per-section copy → Demo (complete!)
5. Polish → State management, edge cases

---

## Notes

- One small JS snippet (~10 lines) for clipboard — only JS in entire app, justified per constitution
- `st.download_button` is native Streamlit — zero JS needed for download
- Replaces per-module copy implementations from 004/006/008 US2 stories
- Section splitting uses `\n## ` — compatible with 014 structured output format
- Commit after each task
