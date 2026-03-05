# Research: Local Document Grounding

## R1 — Text Extraction Libraries

**Decision**: Use `PyPDF2` for PDF, `python-docx` for DOCX,
stdlib `csv` for CSV, and plain `open()` for TXT. Each
format has a dedicated extraction function in `extractor.py`.

**Rationale**: Minimal dependency footprint. `PyPDF2` is the
most popular pure-Python PDF reader (no C dependencies).
`python-docx` is the standard DOCX reader. CSV and TXT
need no external libraries.

**Alternatives considered**:
- `pdfplumber`: More accurate for complex layouts but heavier.
  Over-engineering for MVP. Rejected.
- `pymupdf` (fitz): C-based, faster but harder to install.
  Rejected per Simplicity First.
- `tika` (Apache Tika): Java-based, requires JVM. Rejected —
  violates Python-only stack.
- `unstructured`: Heavy dependency with many sub-deps.
  Rejected per Simplicity First.

## R2 — Excerpt Selection Strategy

**Decision**: Simple keyword-based relevance scoring. When
an AI module generates output:
1. Split each document into chunks (~500 chars, paragraph-
   aligned)
2. Score each chunk against the user's input using keyword
   overlap (TF-IDF-like: count matching words, weight by
   rarity across all chunks)
3. Select top-K chunks (K=3-5, configurable)
4. Append to the LLM prompt as "Reference Context"

**Rationale**: Keyword matching is sufficient for a demo with
5 documents max. No external services, no vector database,
no embeddings API call. Runs entirely in-memory in
milliseconds. Produces reasonable results for document-backed
Q&A.

**Alternatives considered**:
- Embedding-based semantic search (e.g., OpenAI embeddings +
  cosine similarity): Better quality but adds API calls,
  latency, and cost per generation. Rejected for MVP.
- Vector database (e.g., ChromaDB, FAISS): External
  dependency, over-engineering for 5 session-scoped
  documents. Rejected per Simplicity First.
- No relevance filtering (include all text): Exceeds LLM
  context window for large documents. Rejected.
- BM25 (via `rank-bm25`): Slightly better than keyword
  overlap but adds a dependency. Could upgrade later.
  Rejected for MVP.

## R3 — Document Chunking

**Decision**: Split extracted text into chunks of ~500
characters, breaking at paragraph boundaries (`\n\n`) when
possible. Track page numbers for PDF (each page is a natural
chunk boundary). For DOCX/TXT/CSV, use paragraph splitting.

**Rationale**: 500-char chunks are small enough for precise
relevance matching but large enough to retain context. Page-
aligned chunks for PDF enable `[Source: file.pdf, p.N]`
citations. Paragraph splitting is the simplest boundary
heuristic.

**Alternatives considered**:
- Sentence-level splitting: Too granular — loses context.
  Rejected.
- Fixed-size byte chunks: May split mid-word. Rejected.
- Semantic chunking (topic-based): Requires NLP. Over-
  engineering. Rejected.

## R4 — Citation Format

**Decision**: Inject citation instructions into the LLM
prompt: "When you use information from the reference context,
cite the source as [Source: filename.ext] or
[Source: filename.ext, p.N] if page information is available."

The prompt includes each excerpt with its source metadata:
```
--- Reference: report.pdf, p.5 ---
[excerpt text]
```

**Rationale**: The LLM naturally incorporates citations when
instructed and when the source is labeled in the context.
Simple prompt-based approach — no post-processing needed.

**Alternatives considered**:
- Post-processing to inject citations: Requires matching
  output text back to source chunks. Complex and error-prone.
  Rejected.
- Footnote-style citations: More complex formatting. The
  inline `[Source: ...]` style is simpler and spec-compliant.
  Rejected for MVP.

## R5 — Upload UI Design

**Decision**: Use `st.file_uploader()` in the sidebar with
`accept_multiple_files=True`. Limit to accepted MIME types.
Below the uploader, show a list of uploaded documents with
filename, type, size, and a "Remove" button per document.

**Rationale**: Sidebar placement (FR-014) keeps the upload
area accessible across all modules. `st.file_uploader` is
Streamlit's native upload widget — handles file selection,
drag-and-drop, and type filtering.

**Alternatives considered**:
- Separate upload page: Requires navigation away from
  modules. Rejected per spec (accessible from sidebar).
- Expandable panel in main content: Takes space from module
  output. Sidebar is better. Rejected.

## R6 — Session-Scoped Storage

**Decision**: Store extracted documents in
`st.session_state["uploaded_docs"]` as a list of dicts:
`{"filename": str, "type": str, "size": int, "chunks": list,
"active": bool}`. No disk persistence.

**Rationale**: Session state is the natural storage for
session-scoped data in Streamlit. The list of dicts is
simple, searchable, and directly accessible from any module.

**Alternatives considered**:
- Temp files on disk: Adds cleanup logic, persistence risk.
  Rejected per spec (no disk persistence).
- SQLite in-memory: Over-engineering for a list of 5
  documents. Rejected.
