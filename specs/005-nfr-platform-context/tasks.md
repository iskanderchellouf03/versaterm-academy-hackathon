# Tasks: NFR & Platform Context for Requirement Analysis

**Input**: Design documents from `/specs/005-nfr-platform-context/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Not requested in specification. Skipped.

**Organization**: Tasks grouped by user story (US1: system type, US2: NFR checkboxes, US3: combined context).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add constants for system types and NFR options

- [x] T001 Add `SYSTEM_TYPES` and `NFR_OPTIONS` constants to `src/config.py` — `SYSTEM_TYPES` is a dict mapping display name to prompt description (e.g., `{"Web": "Browser compatibility, responsive layout, accessibility, SEO, CORS", "Mobile": "Offline handling, battery, touch interactions, device permissions, network variability", "API": "Request/response validation, authentication, rate limiting, versioning, error codes", "Desktop": "OS compatibility, installation, file system access, keyboard shortcuts, memory management"}`). `NFR_OPTIONS` is a dict mapping NFR name to description (e.g., `{"Performance": "Response times, throughput, resource usage, load handling", "Security": "Authentication, authorization, data protection, input validation", ...}` for all 6 NFRs).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Feature 004-requirement-analyzer must be fully implemented (core analyze flow, prompt, page renderer).

**⚠️ CRITICAL**: 004 must be complete before this feature begins.

*No tasks in this phase — dependency on 004 is external.*

---

## Phase 3: User Story 1 - Select System Type Before Analysis (Priority: P1) 🎯 MVP

**Goal**: User selects system type (Web/Mobile/API/Desktop) via dropdown. Analysis output includes platform-specific considerations. Default: Web.

**Independent Test**: Select "Mobile" → paste "Users can upload a profile photo" → Analyze → output includes mobile-specific concerns (camera permissions, image compression, offline queuing).

### Implementation for User Story 1

- [x] T002 [US1] Add system type dropdown to `src/pages/requirement_analyzer.py` — add `st.selectbox("System Type", list(SYSTEM_TYPES.keys()), key="system_type")` above the "Analyze" button. Import `SYSTEM_TYPES` from `src/config`.
- [x] T003 [US1] Extend prompt builder in `src/ai/prompts/requirement_analyzer.py` — add a `build_context_section(system_type, selected_nfrs)` function that appends a "Context" section to the system prompt: "The target system is a {system_type} application. Consider: {description}." Pass `system_type` from session state when calling the LLM in `requirement_analyzer.py`.

**Checkpoint**: Select "API" → analyze a requirement → output includes API-specific concerns (rate limiting, error codes, authentication).

---

## Phase 4: User Story 2 - Add Non-Functional Requirements (Priority: P2)

**Goal**: User selects NFRs (Performance, Security, Accessibility, Scalability, Reliability, Usability) via multiselect. Analysis output includes NFR-specific test cases and risks. No NFRs selected = baseline behavior.

**Independent Test**: Select "Security" + "Performance" → paste login requirement → Analyze → output includes security test cases (brute force, credential storage) and performance criteria (response time under load).

### Implementation for User Story 2

- [x] T004 [US2] Add NFR multiselect to `src/pages/requirement_analyzer.py` — add `st.multiselect("Non-Functional Requirements", list(NFR_OPTIONS.keys()), key="selected_nfrs")` below the system type dropdown and above "Analyze". Import `NFR_OPTIONS` from `src/config`.
- [x] T005 [US2] Extend `build_context_section()` in `src/ai/prompts/requirement_analyzer.py` — when `selected_nfrs` is non-empty, append to the context section: "The following non-functional requirements apply:\n" followed by a bulleted list of each selected NFR with its description from `NFR_OPTIONS`. When `selected_nfrs` is empty, omit the NFR section entirely (baseline behavior per FR-007).

**Checkpoint**: Select "Security" + "Accessibility" → analyze → output includes security and accessibility items. No NFRs selected → output matches baseline.

---

## Phase 5: User Story 3 - Combined Platform + NFR Context (Priority: P3)

**Goal**: System type and NFR selections combine to produce platform-specific NFR output (e.g., "Mobile" + "Performance" → mobile performance like battery drain, network latency).

**Independent Test**: Select "Mobile" + "Security" + "Performance" → analyze → output includes mobile-security (biometric auth, certificate pinning) and mobile-performance (cold start, memory) rather than generic versions.

### Implementation for User Story 3

- [x] T006 [US3] Update `build_context_section()` in `src/ai/prompts/requirement_analyzer.py` — add an instruction line when both system type and NFRs are provided: "When addressing non-functional requirements, focus on concerns specific to {system_type} applications rather than generic considerations." This ensures the LLM combines the two contexts.

**Checkpoint**: "Desktop" + "Accessibility" → output includes desktop-accessibility (keyboard shortcuts, high-contrast, screen magnification) not generic web accessibility.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases and validation

- [x] T007 Verify selections persist across re-analyses in `src/pages/requirement_analyzer.py` — confirm `st.selectbox` and `st.multiselect` with `key` params retain values after clicking "Analyze" (Streamlit handles natively, just verify).
- [x] T008 Verify edge case: all 6 NFRs selected — analyze a requirement and confirm output is well-structured (all 5 sections present, not excessively long). Timeout still within 30 seconds.
- [x] T009 Run quickstart.md validation — confirm platform + NFR context flow works end-to-end.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately (T001)
- **Foundational (Phase 2)**: External — 004 must be complete
- **US1 (Phase 3)**: Depends on T001 (constants) and 004 (base analyzer)
- **US2 (Phase 4)**: Depends on T001 (constants) and 004. Independent of US1 at code level but sequential for UX coherence.
- **US3 (Phase 5)**: Depends on US1 + US2 (both context types must exist to combine)
- **Polish (Phase 6)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Setup + external 004
- **User Story 2 (P2)**: Depends on Setup + external 004. Can be developed in parallel with US1 (different UI control + different prompt section).
- **User Story 3 (P3)**: Depends on US1 + US2 (combines both)

### Parallel Opportunities

- T002 and T004 can run in parallel (different UI controls in same file, but adjacent — safer to do sequentially)
- T003 and T005 modify the same function — must be sequential
- US1 and US2 UI tasks (T002, T004) are independent additions to the page

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 3: User Story 1 (T002-T003)
3. **STOP and VALIDATE**: System type dropdown influences output
4. Demo-ready — platform-aware analysis

### Incremental Delivery

1. Setup → Constants ready
2. US1 → System type dropdown → Demo (MVP!)
3. US2 → NFR multiselect → Demo (quality-aware!)
4. US3 → Combined context → Demo (complete!)
5. Polish → Persistence, edge cases verified

---

## Notes

- Zero new files — all modifications to existing 004 files + config.py
- Zero new dependencies
- `build_context_section()` is the single integration point between UI selections and LLM prompt
- Constants in config.py make system types and NFR options easy to update
- Session state persistence is automatic via Streamlit widget `key` params
- Commit after each task
