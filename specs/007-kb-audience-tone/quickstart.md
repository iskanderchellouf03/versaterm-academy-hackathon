# Quickstart: KB Audience & Tone Selection

## Overview

Adds audience (Internal/External/Support) and tone
(Formal/Conversational/Concise) selectors to the KB Article
Generator (006). Context injected into the LLM prompt.

## Prerequisites

- Feature 006 (KB article generator) must be implemented
- All 006 prerequisites (001, 003, 004, 014)

## How It Works

1. User selects audience (defaults to "Internal")
2. User selects tone (defaults to "Formal")
3. User pastes raw text and clicks "Generate"
4. Prompt builder appends audience + tone descriptions
5. LLM produces article matching the audience and tone

## Code Changes (no new files)

- `src/pages/kb_article_generator.py` — Add two `st.selectbox` widgets
- `src/ai/prompts/kb_article_generator.py` — Extend prompt with audience/tone
- `src/config.py` — Add `AUDIENCES` and `TONES` constants

## Testing

```bash
cd src && pytest tests/ -k "audience or tone"
```

Verify:
- Audience defaults to "Internal"
- Tone defaults to "Formal"
- "External" produces plain, jargon-free language
- "Concise" produces bullet-heavy, minimal prose
- Same input with different audience/tone produces different output
- Selections persist across regenerations in same session
