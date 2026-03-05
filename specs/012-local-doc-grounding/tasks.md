# Tasks: Local Document Grounding

**Input**: Design documents from `/specs/012-local-doc-grounding/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Not requested in specification. Skipped.

**Organization**: Tasks grouped by user story (US1: upload documents, US2: grounded AI output with citations, US3: manage uploaded documents).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create docs package, add config constants, add dependencies

- [x] T001 [P] Create `src/docs/` package with `src/docs/__init__.py`
- [x] T002 [P] Add grounding config constants to `src/config.py` — `MAX_FILE_SIZE_MB = 10`, `MAX_FILES = 5`, `CHUNK_SIZE = 500`, `TOP_K = 3`, `ACCEPTED_TYPES = ["pdf", "docx", "txt", "csv"]`, `ACCEPTED_MIMES = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain", "text/csv"]`
- [x] T003 [P] Add `PyPDF2` and `python-docx` to `requirements.txt`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Features 001 (auth), 003 (shell/sidebar), 004 (AI client), 010 (components package) must be complete.

**⚠️ CRITICAL**: `src/app.py`, `src/pages/__init__.py`, `src/ai/client.py`, and `src/components/__init__.py` must exist.

*No tasks in this phase — dependency on 001/003/004/010 is external.*

---

## Phase 3: User Story 1 - Upload Documents for Grounding (Priority: P1) 🎯 MVP

**Goal**: User uploads PDF/DOCX/TXT/CSV files via sidebar uploader. System extracts text, chunks it, stores in session state. Document list shown with filename, type, size. Validation: type check, 10 MB limit, 5 files max. Warning if no text extracted.

**Independent Test**: Upload a PDF and a TXT file → both appear in document list with correct names and types → system confirms processing.

### Implementation for User Story 1

- [x] T004 [P] [US1] Implement text extraction in `src/docs/extractor.py` — create functions: `extract_pdf(file_bytes) -> list[dict]` using `PyPDF2.PdfReader` to extract text per page, returning chunks with `{"text": str, "page": int, "index": int}`; `extract_docx(file_bytes) -> list[dict]` using `docx.Document` to extract paragraph text, returning chunks with page=None; `extract_txt(file_bytes) -> list[dict]` using plain decode, returning chunks with page=None; `extract_csv(file_bytes) -> list[dict]` using `csv.reader`, joining rows as text, returning chunks with page=None. Each function splits text into ~500 char chunks (paragraph-aligned via `\n\n` splitting). Add a dispatcher `extract_text(file_bytes, file_type) -> list[dict]` that routes to the correct extractor.
- [x] T005 [P] [US1] Implement session-scoped document store in `src/docs/store.py` — functions: `get_documents() -> list[dict]` returns `st.session_state.get("uploaded_docs", [])`. `add_document(filename, file_type, size, chunks) -> None` appends a document record `{"filename": filename, "type": file_type, "size": size, "chunks": chunks, "active": True}` to session state list. Enforce `MAX_FILES` limit — return error message if exceeded. `remove_document(filename) -> None` sets `active=False` for the matching document. `get_active_documents() -> list[dict]` returns only docs where `active=True`.
- [x] T006 [US1] Create upload UI in `src/components/doc_uploader.py` — implement `render_doc_uploader()` function. Use `st.file_uploader("Upload documents", type=ACCEPTED_TYPES, accept_multiple_files=True, key="doc_upload")` in the sidebar. On upload: validate file size <= `MAX_FILE_SIZE_MB * 1024 * 1024`, validate file count with `get_documents()`, call `extract_text()` for each file, call `add_document()` to store. If extraction yields empty chunks, show `st.warning(f"No text content could be extracted from {filename}.")`. Display document list below uploader showing filename, type, size (formatted as KB/MB) for each active document. Import constants from `src.config`.
- [x] T007 [US1] Integrate doc uploader into `src/app.py` — in the sidebar section (after module navigation), call `render_doc_uploader()` from `src.components.doc_uploader`. This makes upload accessible across all modules. Only render when user is authenticated.

**Checkpoint**: Upload PDF/DOCX/TXT/CSV → documents appear in sidebar list. Size limit enforced. File count limited. Empty-text warning shown. Session-scoped only.

---

## Phase 4: User Story 2 - Grounded AI Output with Citations (Priority: P2)

**Goal**: When documents are uploaded, AI modules include top-K relevant excerpts as context. Output includes `[Source: filename.ext]` or `[Source: filename.ext, p.N]` citations. No documents = baseline behavior (no change). No relevant excerpts = no forced citations.

**Independent Test**: Upload a Versaterm PDF → go to KB Article Generator → paste related topic → generate → output includes citations from uploaded PDF.

### Implementation for User Story 2

- [x] T008 [US2] Implement keyword-based retriever in `src/docs/retriever.py` — create `retrieve_top_k(query: str, documents: list[dict], k: int = TOP_K) -> list[dict]` that: (1) collects all chunks from active documents, (2) tokenizes query into keywords (lowercase, strip punctuation, remove stopwords), (3) scores each chunk by keyword overlap count (weighted by rarity across all chunks — simple IDF), (4) returns top-K chunks sorted by score descending, each as `{"text": str, "page": int|None, "source": str, "score": float}`. Return empty list if no documents or no matches above threshold.
- [x] T009 [US2] Create grounding prompt builder in `src/ai/prompts/grounding.py` — implement `build_grounding_context(user_input: str) -> str` that: (1) calls `get_active_documents()` from store, (2) if no documents, returns empty string, (3) calls `retrieve_top_k(user_input, documents)`, (4) if no relevant chunks, returns empty string, (5) formats each chunk as `--- Reference: {source}, p.{page} ---\n{text}\n` (omit page if None), (6) wraps in a section: `"\n\nReference Context (from uploaded documents):\n{formatted_chunks}\n\nWhen you use information from the reference context above, cite the source as [Source: filename.ext] or [Source: filename.ext, p.N] if page information is available. If the reference context is not relevant to the query, ignore it and do not force citations."`. Return the full section string.
- [x] T010 [P] [US2] Integrate grounding into `src/pages/requirement_analyzer.py` — before calling the LLM, call `build_grounding_context(user_input)` and append the returned string to the user message (or system prompt). If empty string returned, skip (baseline behavior preserved).
- [x] T011 [P] [US2] Integrate grounding into `src/pages/kb_article_generator.py` — same pattern as T010: call `build_grounding_context(input_text)` and append to LLM call. If empty, skip.
- [x] T012 [P] [US2] Integrate grounding into `src/pages/onboarding_planner.py` — same pattern as T010: call `build_grounding_context(role + " " + product)` and append to LLM call. If empty, skip.

**Checkpoint**: Upload document → generate in any module → citations appear. No documents → baseline behavior. Irrelevant documents → no forced citations.

---

## Phase 5: User Story 3 - Manage Uploaded Documents (Priority: P3)

**Goal**: Document list shows filename, type, size. Each document has a "Remove" button. Removed documents excluded from grounding.

**Independent Test**: Upload 3 docs → remove one → generate output → removed doc's content not cited, others still cited.

### Implementation for User Story 3

- [x] T013 [US3] Add document management UI to `src/components/doc_uploader.py` — extend `render_doc_uploader()` to display each active document with a `st.button("Remove", key=f"remove_{filename}")` that calls `remove_document(filename)` and triggers `st.rerun()`. Show document metadata: filename, type badge, size formatted as human-readable string (e.g., "2.3 MB", "450 KB"). Use `st.columns` for layout: col1 for metadata, col2 for remove button.

**Checkpoint**: Remove document → disappears from list → not included in future generations.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases and validation

- [x] T014 Verify empty-text file handling — upload a PDF with no text layer (or empty TXT), confirm warning shown and file excluded from grounding context.
- [x] T015 Verify no-documents baseline — with no uploads, generate output in all 3 AI modules, confirm identical behavior to pre-012 baseline.
- [x] T016 Verify file limit enforcement — upload 5 files, attempt a 6th, confirm rejection with clear message.
- [x] T017 Run quickstart.md validation — upload a document, generate grounded output in all 3 modules, confirm citations present.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately (T001-T003)
- **Foundational (Phase 2)**: External — 001/003/004/010 must be complete
- **US1 (Phase 3)**: Depends on T001-T003 (package + config + deps) and 001/003/004/010
- **US2 (Phase 4)**: Depends on US1 (documents must be uploaded to ground)
- **US3 (Phase 5)**: Depends on US1 (documents must exist to manage). Independent of US2.
- **Polish (Phase 6)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Setup + external 001/003/004/010
- **User Story 2 (P2)**: Depends on US1 (need uploaded docs to ground against)
- **User Story 3 (P3)**: Depends on US1. Independent of US2 at code level.

### Parallel Opportunities

- T001, T002, T003 can all run in parallel (different files)
- T004 and T005 can run in parallel (different files: extractor vs store)
- T010, T011, T012 can run in parallel (different module pages)
- US2 and US3 can develop in parallel after US1

---

## Parallel Example: Module Integration

```bash
# Integrate grounding into all AI modules simultaneously:
Task: "Integrate grounding into requirement_analyzer.py"
Task: "Integrate grounding into kb_article_generator.py"
Task: "Integrate grounding into onboarding_planner.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 3: User Story 1 (T004-T007)
3. **STOP and VALIDATE**: Upload files → see in sidebar list → text extracted
4. Demo-ready — document upload functional

### Incremental Delivery

1. Setup → Package + config + dependencies ready
2. US1 → Upload + extract + store → Demo (MVP!)
3. US2 → Grounded output with citations → Demo (impressive!)
4. US3 → Document management (remove) → Demo (complete!)
5. Polish → Edge cases, baselines verified

---

## Notes

- Two new dependencies justified: `PyPDF2` (PDF parsing), `python-docx` (DOCX parsing)
- Keyword-based retrieval — no vector DB, no embeddings, no external API calls
- Session-scoped only — no disk persistence, no database
- Cross-cutting: modifies all 3 AI module pages (004, 006, 008)
- Same `build_grounding_context()` pattern used across all modules
- Citations are LLM-generated via prompt instruction, not post-processed
- Commit after each task
