# Quickstart: Local Document Grounding

## Overview

Upload PDF, DOCX, TXT, or CSV files to provide grounding context
for all AI modules. The system extracts text, selects relevant
excerpts via keyword matching, and injects them into LLM prompts
with source citations.

## Prerequisites

- Feature 001 (employee auth) for access gate
- Feature 003 (app shell layout) for sidebar placement
- Feature 004/006/008 (AI modules) to consume grounding context
- `pip install PyPDF2 python-docx`

## How It Works

1. User uploads files via `st.file_uploader` in the sidebar
2. `extractor.py` extracts text per format (PyPDF2, python-docx, stdlib)
3. Text is split into ~500-char paragraph-aligned chunks
4. Chunks stored in `st.session_state["uploaded_docs"]`
5. When an AI module generates output, `retriever.py` scores all
   active chunks against the user's input using keyword overlap
6. Top-K chunks (default 3) are selected
7. `grounding.py` formats excerpts with source metadata and appends
   to the LLM system prompt
8. LLM generates output with `[Source: filename.ext]` citations

## Code Location

- `src/docs/extractor.py` — Text extraction (PDF, DOCX, TXT, CSV)
- `src/docs/store.py` — Session-scoped document store operations
- `src/docs/retriever.py` — Top-K keyword-based excerpt selection
- `src/components/doc_uploader.py` — Sidebar upload UI component
- `src/ai/prompts/grounding.py` — Prompt section builder for context
- `src/config.py` — MAX_FILE_SIZE_MB, MAX_FILES, TOP_K, CHUNK_SIZE

## Adding Grounding to an AI Module

In any AI module page (e.g., `requirement_analyzer.py`):

```python
from src.ai.prompts.grounding import build_grounding_context

# After user submits input:
grounding_section = build_grounding_context(user_input_text)
# grounding_section is "" if no docs or no relevant excerpts

# Append to system prompt:
system_prompt = base_system_prompt + grounding_section
```

## Upload Flow

```python
from src.components.doc_uploader import render_doc_uploader

# In sidebar:
with st.sidebar:
    render_doc_uploader()
```

## Removing a Document

The `render_doc_uploader` component renders a "Remove" button per
document. Clicking it sets `active=False` on the document record,
excluding it from future retrievals.

## Testing

```bash
cd src && pytest tests/ -k "doc"
```

Verify:
- PDF/DOCX/TXT/CSV upload and text extraction
- Unsupported format rejection
- File size and count limits enforced
- Keyword-based chunk scoring returns relevant excerpts
- Grounding context appears in LLM prompt when docs uploaded
- No grounding context when no docs uploaded (baseline behavior)
- Citations include correct filenames
- Remove excludes document from grounding
