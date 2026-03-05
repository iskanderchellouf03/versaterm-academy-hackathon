# Implementation Plan: Local Document Grounding

**Branch**: `012-local-doc-grounding` | **Date**: 2026-03-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/012-local-doc-grounding/spec.md`

## Summary

Add document upload (PDF/DOCX/TXT/CSV) with text extraction,
session-scoped storage, top-K excerpt retrieval, and citation
injection into all AI module prompts. Uses `st.file_uploader`
for upload, `PyPDF2` for PDF extraction, `python-docx` for
DOCX, stdlib for TXT/CSV. Simple keyword-based relevance
scoring for excerpt selection (no vector database). Excerpts
appended to the LLM prompt with citation instructions.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit (file upload, UI), `PyPDF2` (PDF text), `python-docx` (DOCX text), `openai` (from 004)
**Storage**: In-memory (session state) — no disk persistence
**Testing**: pytest
**Target Platform**: Web (Streamlit app)
**Project Type**: Cross-cutting enhancement to web application
**Performance Goals**: Upload + extraction < 10s for files under 5 MB
**Constraints**: All Python, 10 MB/file, 5 files/session, no OCR, session-only
**Scale/Scope**: Enhances all 3 AI modules (004, 006, 008)

## Constitution Check

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. User-Centric Design | PASS | "Upload real docs so AI output references Versaterm materials." Direct employee value. |
| II. Simplicity First | PASS | Keyword-based excerpt selection (no vector DB, no embeddings). `PyPDF2` and `python-docx` are lightweight, focused libraries. |
| MVP-first | PASS | US1 (upload) is independently demoable. Grounding (US2) and management (US3) are incremental. |
| Demo-ready | PASS | Upload a PDF, generate output, see citations. Impressive demo. |
| No gold-plating | PASS | No OCR, no vector store, no semantic search, no permanent storage. |
| Tech stack | PASS | Python libraries. Two new deps justified — no stdlib alternative for PDF/DOCX parsing. |
| Single-repo | PASS | All code in repo. Files stored in memory only. |

**Post-design re-check**: PASS. Two new dependencies
(`PyPDF2`, `python-docx`) are justified — stdlib cannot parse
PDF or DOCX formats. Both are lightweight, widely-used Python
packages.

## Project Structure

### Documentation (this feature)

```text
specs/012-local-doc-grounding/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```text
src/
├── docs/
│   ├── __init__.py
│   ├── extractor.py         # Text extraction (PDF, DOCX, TXT, CSV)
│   ├── store.py             # Session-scoped document store (in-memory)
│   └── retriever.py         # Top-K excerpt selection (keyword relevance)
├── components/
│   └── doc_uploader.py      # Upload UI (sidebar panel)
├── ai/
│   └── prompts/
│       └── grounding.py     # Prompt section builder for grounding context
├── pages/
│   ├── requirement_analyzer.py   # (modify) — inject grounding context
│   ├── kb_article_generator.py   # (modify) — inject grounding context
│   └── onboarding_planner.py     # (modify) — inject grounding context
└── config.py                     # (modify) — add MAX_FILE_SIZE, MAX_FILES, TOP_K
```

**Structure Decision**: New `src/docs/` package for document
handling (extraction, storage, retrieval). New upload
component in `src/components/`. Grounding prompt builder in
`src/ai/prompts/grounding.py`. Each AI module page modified
to call the grounding context builder before sending to LLM.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| `PyPDF2` dependency | PDF text extraction requires a parser — no stdlib solution | Reading raw bytes is not viable for PDF format |
| `python-docx` dependency | DOCX text extraction requires XML parsing — no stdlib solution | DOCX is a ZIP of XML files; manual parsing is fragile |
