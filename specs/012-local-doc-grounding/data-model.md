# Data Model: Local Document Grounding

## Session State

### Uploaded Documents Store

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| uploaded_docs | list[dict] | [] | List of processed document records |

### Document Record (dict in uploaded_docs)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| filename | str | Yes | Original upload filename (e.g., "manual.pdf") |
| type | str | Yes | File extension lowercase ("pdf", "docx", "txt", "csv") |
| size | int | Yes | File size in bytes |
| chunks | list[dict] | Yes | Extracted text chunks (see Chunk below) |
| active | bool | Yes | Whether document is included in grounding (default True) |

### Chunk Record (dict in chunks list)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| text | str | Yes | Chunk text content (~500 chars, paragraph-aligned) |
| page | int or None | Yes | Page number (1-based) for PDF; None for other formats |
| index | int | Yes | Sequential chunk index within the document |

## Configuration Constants (config.py)

| Constant | Type | Value | Description |
|----------|------|-------|-------------|
| MAX_FILE_SIZE_MB | int | 10 | Maximum upload size per file in MB |
| MAX_FILES | int | 5 | Maximum documents per session |
| CHUNK_SIZE | int | 500 | Target chunk size in characters |
| TOP_K | int | 3 | Number of top excerpts to include in prompt |
| ACCEPTED_TYPES | list[str] | ["pdf", "docx", "txt", "csv"] | Allowed file extensions |
| ACCEPTED_MIMES | list[str] | ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain", "text/csv"] | MIME types for st.file_uploader |

## State Transitions

```
[No documents uploaded]
  → uploaded_docs = []
  → AI modules behave as baseline (no grounding context)

[User uploads file]
  → Validate: type in ACCEPTED_TYPES, size <= MAX_FILE_SIZE_MB, len(uploaded_docs) < MAX_FILES
  → Extract text → split into chunks → append document record
  → uploaded_docs grows by 1
  → If extraction yields no text: add record with chunks=[], show warning

[User removes document]
  → Set doc["active"] = False (or remove from list)
  → Document excluded from retrieval

[AI module generates output]
  → Collect chunks from all active documents
  → Score chunks against user input (keyword overlap)
  → Select top-K chunks
  → Format as reference context with source metadata
  → Append to LLM prompt
  → If no relevant chunks found: skip grounding (no citation)
  → If no documents uploaded: skip entirely (baseline behavior)

[New session]
  → uploaded_docs defaults to [] → clean slate
```

## Relationships

- **Depends on**: 001-employee-auth (user must be authenticated),
  003-app-shell-layout (sidebar placement for upload UI)
- **Enhances**: 004-requirement-analyzer, 006-kb-article-generator,
  008-onboarding-plan-generator (all AI modules receive grounding context)
- **Compatible with**: 010-copy-download-export (citations appear in
  exported output), 011-demo-banner (no conflict), 013-branded-theme
  (upload UI inherits theme)

## Entities Diagram

```
Session State
  └── uploaded_docs: list
        └── Document Record
              ├── filename: str
              ├── type: str
              ├── size: int
              ├── active: bool
              └── chunks: list
                    └── Chunk Record
                          ├── text: str
                          ├── page: int | None
                          └── index: int
```
