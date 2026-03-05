# Quickstart: AI Requirement Analyzer

## Overview

The Requirement Analyzer is the first AI module. Users paste
a raw requirement and get structured output: rewritten
requirements, acceptance criteria, test cases, edge cases,
and risks.

## Prerequisites

- Features 001 (auth), 003 (shell layout), 014 (output format)
- `OPENAI_API_KEY` environment variable set
- `OPENAI_BASE_URL` (optional, defaults to OpenAI)
- `OPENAI_MODEL` (optional, defaults to `gpt-4o`)

## Setup

```bash
pip install openai
echo "OPENAI_API_KEY=sk-..." >> .env
streamlit run src/app.py
```

## How It Works

1. User navigates to "Requirement Analyzer" in sidebar
2. Pastes requirement text (up to 5,000 chars)
3. Clicks "Analyze"
4. System builds prompt:
   - Module-specific content instructions
   - Formatting rules from 014 (`get_system_prompt("004")`)
5. Sends to LLM via shared client (`src/ai/client.py`)
6. Post-processes response (`normalize_output("004", text)`)
7. Displays five sections with copy buttons

## Code Location

- `src/pages/requirement_analyzer.py` — Module UI (input, button, output)
- `src/ai/client.py` — Shared LLM client
- `src/ai/prompts/requirement_analyzer.py` — System prompt
- `src/output/schema.py` — Section definitions for "004"

## Adding to Module Registry

In `src/pages/__init__.py`:
```python
from src.pages.requirement_analyzer import render

MODULES = {
    "Requirement Analyzer": render,
    ...
}
```

## Testing

```bash
cd src && pytest tests/ -k "requirement_analyzer"
```

Verify:
- Empty input shows validation error
- Input > 5,000 chars is truncated with warning
- LLM call returns all 5 sections
- Output renders as valid Markdown
- Copy buttons work for each section
- 30-second timeout displays error message
