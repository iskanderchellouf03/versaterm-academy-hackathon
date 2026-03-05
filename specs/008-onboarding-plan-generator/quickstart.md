# Quickstart: Onboarding Plan Generator

## Overview

The Onboarding Plan Generator creates 2-week learning plans
from role, product, and level inputs. Output includes What
It Is, Why It Matters, Key Terms, Learning Plan, Checkpoints.

## Prerequisites

- Features 001 (auth), 003 (shell), 004 (shared AI client), 014 (output format)
- `OPENAI_API_KEY` environment variable set

## How It Works

1. User navigates to "Onboarding Planner" in sidebar
2. Enters role (free text), product (free text), level (dropdown)
3. Clicks "Generate Plan"
4. Prompt includes role/product/level context + formatting rules
5. LLM produces 5-section plan with day-by-day schedule
6. Output displayed, copy button available

## Code Location

- `src/pages/onboarding_planner.py` — Module UI
- `src/ai/prompts/onboarding_planner.py` — System prompt
- `src/ai/client.py` — Shared LLM client (from 004)
- `src/output/schema.py` — Section definitions for "008"

## Adding to Module Registry

In `src/pages/__init__.py`:
```python
from src.pages.onboarding_planner import render

MODULES = {
    ...
    "Onboarding Planner": render,
}
```

## Testing

```bash
cd src && pytest tests/ -k "onboarding"
```

Verify:
- Empty fields show validation errors
- Beginner level produces fundamentals-first plan
- Advanced level skips basics
- Different roles for same product produce different plans
- All 5 sections present in every output
- Learning Plan spans exactly 10 business days
- Key Terms has >= 5 entries
- Checkpoints has >= 2 items
