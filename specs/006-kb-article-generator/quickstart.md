# Quickstart: KB Article Generator

## Overview

The KB Article Generator transforms messy notes, transcripts,
or raw text into structured knowledge base articles with
Title, Summary, Body, and Tags.

## Prerequisites

- Features 001 (auth), 003 (shell), 004 (shared AI client), 014 (output format)
- `OPENAI_API_KEY` environment variable set

## How It Works

1. User navigates to "KB Article Generator" in sidebar
2. Sees sensitive-data reminder banner
3. Pastes raw text (up to 10,000 chars)
4. Clicks "Generate"
5. System builds prompt (content + formatting from 014)
6. LLM produces structured article
7. Output displayed in editable text area
8. User can edit, then copy

## Code Location

- `src/pages/kb_article_generator.py` — Module UI
- `src/ai/prompts/kb_article_generator.py` — System prompt
- `src/ai/client.py` — Shared LLM client (from 004)
- `src/output/schema.py` — Section definitions for "006"

## Adding to Module Registry

In `src/pages/__init__.py`:
```python
from src.pages.kb_article_generator import render

MODULES = {
    ...
    "KB Article Generator": render,
}
```

## Testing

```bash
cd src && pytest tests/ -k "kb_article"
```

Verify:
- Empty input shows validation error
- Input > 10,000 chars truncated with warning
- Output has all 4 sections (Title, Summary, Body, Tags)
- Output is editable in text area
- Copy button copies edited content
- 30-second timeout shows error message
- Sensitive data reminder always visible
