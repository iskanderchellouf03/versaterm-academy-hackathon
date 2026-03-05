# Tasks: Structured Output Formatting

**Input**: Design documents from `/specs/014-structured-output-format/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Not requested in specification. Skipped.

**Organization**: Tasks grouped by user story (US1: strict section headings, US2: concise tone, US3: clean Markdown output).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create output package with section schema and formatting rules

- [x] T001 [P] Create `src/output/` package with `src/output/__init__.py`
- [x] T002 [P] Define per-module section schemas in `src/output/schema.py` — create `MODULE_SCHEMAS` dict mapping module IDs to their section definitions: `{"004": {"name": "Requirement Analyzer", "sections": ["Rewritten Requirements", "Acceptance Criteria", "Test Cases", "Edge Cases", "Risks"], "empty_note": "None identified."}, "006": {"name": "KB Article Generator", "sections": ["Title", "Summary", "Body", "Tags"], "empty_note": "None identified."}, "008": {"name": "Onboarding Plan Generator", "sections": ["What It Is", "Why It Matters", "Key Terms", "Learning Plan", "Checkpoints"], "empty_note": "None identified."}}`. Also define `FORMATTING_RULES` dict with shared rules: `{"heading_level": 2, "subheading_level": 3, "list_marker": "-", "bold_syntax": "**", "no_preamble": True, "no_signoff": True, "direct_voice": True, "bullet_first": True}`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: All AI modules (004, 006, 008) must be complete. Feature 003 (app shell) must exist.

**⚠️ CRITICAL**: `src/pages/requirement_analyzer.py`, `src/pages/kb_article_generator.py`, `src/pages/onboarding_planner.py` must exist with working LLM calls.

*No tasks in this phase — dependency on 004/006/008 is external.*

---

## Phase 3: User Story 1 - Strict Section Headings per Module (Priority: P1) 🎯 MVP

**Goal**: Every AI module output contains a fixed, predictable set of section headings in a fixed order. No section omitted — empty sections show "None identified." Section headings identical across runs.

**Independent Test**: Run Requirement Analyzer 3 times with different inputs → every output has exactly: Rewritten Requirements, Acceptance Criteria, Test Cases, Edge Cases, Risks in that order. Same for KB Article Generator (4 sections) and Onboarding Planner (5 sections).

### Implementation for User Story 1

- [x] T003 [US1] Create system prompt builder in `src/output/prompt.py` — implement `get_format_prompt(module_id: str) -> str` that: (1) looks up `MODULE_SCHEMAS[module_id]`, (2) builds a formatting instruction string: "You MUST structure your output with exactly these sections, in this order, using ## headings:\n{numbered list of sections}\n\nIMPORTANT: Never omit a section. If you have no relevant content for a section, include the heading with the note: '{empty_note}'". Return the string. If `module_id` not found, return empty string.
- [x] T004 [US1] Create section enforcement post-processor in `src/output/normalizer.py` — implement `ensure_sections(module_id: str, text: str) -> str` that: (1) looks up `MODULE_SCHEMAS[module_id]`, (2) checks that all required section headings (`## Section Name`) are present in `text`, (3) for any missing section, inserts `## {section_name}\n\n{empty_note}\n\n` at the correct position relative to existing sections, (4) returns the corrected text. Use simple string searching for `## ` headings.
- [x] T005 [US1] Integrate format prompt into `src/pages/requirement_analyzer.py` — import `get_format_prompt` from `src.output.prompt`, call `get_format_prompt("004")`, and append the returned string to the system prompt before calling the LLM. After receiving the LLM response, call `ensure_sections("004", result)` before storing in session state.
- [x] T006 [P] [US1] Integrate format prompt into `src/pages/kb_article_generator.py` — same pattern as T005: append `get_format_prompt("006")` to system prompt, call `ensure_sections("006", result)` on LLM response.
- [x] T007 [P] [US1] Integrate format prompt into `src/pages/onboarding_planner.py` — same pattern as T005: append `get_format_prompt("008")` to system prompt, call `ensure_sections("008", result)` on LLM response.

**Checkpoint**: All 3 modules produce outputs with fixed section headings. No sections missing. Empty sections show placeholder.

---

## Phase 4: User Story 2 - Concise, Scannable Tone (Priority: P2)

**Goal**: No filler preamble/sign-off. Bullet-first formatting. Direct active voice. No AI meta-commentary.

**Independent Test**: Generate output in any module → no "Here is your analysis..." intro, no "I hope this helps!" sign-off, lists use bullets, language is direct.

### Implementation for User Story 2

- [x] T008 [US2] Extend `get_format_prompt()` in `src/output/prompt.py` — add tone rules to the formatting instruction string based on `FORMATTING_RULES`: "Tone rules:\n- Do NOT include any introductory preamble (e.g., 'Here is your analysis...')\n- Do NOT include any closing sign-off (e.g., 'I hope this helps!')\n- Do NOT include meta-commentary about your process\n- Use direct, active voice with imperative verbs (e.g., 'System MUST validate' not 'It would be good if...')\n- Use bullet points (-) for enumerable content instead of long paragraphs\n- Each bullet or paragraph conveys ONE idea — no redundant restatements". These rules are appended to the section structure instructions already in the prompt.

**Checkpoint**: No preamble/sign-off in outputs. Lists use bullets. Direct voice throughout.

---

## Phase 5: User Story 3 - Clean Markdown Output (Priority: P3)

**Goal**: Valid Markdown: `##` for sections, `-` for unordered lists, `**` for bold, no raw HTML, no code fences around non-code. Acceptance criteria use bold Given/When/Then.

**Independent Test**: Generate output → copy → paste into GitHub comment or Confluence → renders correctly with no artifacts.

### Implementation for User Story 3

- [x] T009 [US3] Implement Markdown normalizer in `src/output/normalizer.py` — add `normalize_markdown(text: str) -> str` function that applies regex-based fixes: (1) replace `* ` list markers with `- ` (but not inside code fences), (2) strip raw HTML tags outside code fences using `re.sub(r'<[^>]+>', '', text)` (with code-fence-aware splitting), (3) normalize `__text__` bold to `**text**`, (4) ensure section headings use `## ` not `# ` or `#### `, (5) remove code fences that wrap non-code content (i.e., fences without a language identifier that contain only prose). Return cleaned text.
- [x] T010 [US3] Extend `get_format_prompt()` in `src/output/prompt.py` — add Markdown style rules: "Markdown rules:\n- Use ## for top-level sections and ### for subsections\n- Use - for unordered lists and 1. for ordered lists\n- Use **text** for bold emphasis — never ALL CAPS or underscores\n- Never output raw HTML\n- Never wrap non-code content in code fences\n- Format acceptance criteria with bold keywords: **Given** / **When** / **Then**".
- [x] T011 [US3] Wire normalizer into all 3 module pages — in each of `src/pages/requirement_analyzer.py`, `src/pages/kb_article_generator.py`, `src/pages/onboarding_planner.py`, after calling `ensure_sections()`, also call `normalize_markdown(result)` before storing in session state. This can be combined with the existing `ensure_sections` call as: `result = normalize_markdown(ensure_sections(module_id, raw_result))`.

**Checkpoint**: Copied output renders correctly in Markdown tools. No HTML, no wrong list markers, no code fences around prose.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Consistency verification and edge cases

- [x] T012 Verify section consistency across runs — generate output 3 times in each module with different inputs, confirm sections are identical in name and order every time.
- [x] T013 Verify empty section handling — provide minimal input to Requirement Analyzer that likely won't produce edge cases or risks, confirm those sections appear with "None identified." note.
- [x] T014 Verify normalizer does not corrupt code content — if any module can produce code snippets in output, confirm code fences are preserved for actual code.
- [x] T015 Run quickstart.md validation — confirm all 3 modules produce structured, clean Markdown output end-to-end.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately (T001-T002)
- **Foundational (Phase 2)**: External — 004/006/008 must be complete
- **US1 (Phase 3)**: Depends on T001-T002 (schema + package) and 004/006/008
- **US2 (Phase 4)**: Depends on US1 (extends the format prompt from T003)
- **US3 (Phase 5)**: Depends on US1 (extends normalizer from T004). Independent of US2 at code level.
- **Polish (Phase 6)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Setup + external 004/006/008
- **User Story 2 (P2)**: Depends on US1 (extends `get_format_prompt`)
- **User Story 3 (P3)**: Depends on US1 (extends normalizer). Independent of US2.

### Parallel Opportunities

- T001 and T002 can run in parallel (different files)
- T006 and T007 can run in parallel (different module pages)
- US2 and US3 can develop in parallel after US1 (different concerns: tone vs Markdown)

---

## Parallel Example: Module Integration

```bash
# Integrate formatting into all modules simultaneously:
Task: "Integrate format prompt into kb_article_generator.py"
Task: "Integrate format prompt into onboarding_planner.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 3: User Story 1 (T003-T007)
3. **STOP and VALIDATE**: All 3 modules produce outputs with fixed section headings
4. Demo-ready — predictable, structured AI output

### Incremental Delivery

1. Setup → Schema + package ready
2. US1 → Section heading enforcement → Demo (MVP!)
3. US2 → Concise tone rules → Demo (professional!)
4. US3 → Clean Markdown normalization → Demo (copy-paste ready!)
5. Polish → Consistency verification, edge cases

---

## Notes

- Zero new dependencies — uses stdlib `re` for Markdown normalization
- Cross-cutting: modifies all 3 AI module pages (004, 006, 008)
- Two-function integration per module: `get_format_prompt()` + `normalize_markdown(ensure_sections())`
- Section schemas are plain Python dicts — easy to extend for future modules
- Prompt engineering handles 95%+ of formatting; normalizer handles the remaining edge cases
- Compatible with 010-copy-download-export (clean Markdown = better copy/download)
- Commit after each task
