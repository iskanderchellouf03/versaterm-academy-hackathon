# Quickstart: Onboarding Focus Notes

## Overview

Adds an optional "Focus notes" text area to the Onboarding
Plan Generator (008). Focus topics are emphasized in the
generated plan's activities, terms, and checkpoints.

## Prerequisites

- Feature 008 (onboarding plan generator) must be implemented
- All 008 prerequisites (001, 003, 004, 014)

## How It Works

1. User fills in role, product, level (from 008)
2. Optionally enters focus notes (up to 1,000 chars)
3. Clicks "Generate Plan"
4. If focus notes provided, prompt includes "Priority Focus
   Areas" section
5. LLM frontloads focus-related activities, adds focus terms,
   includes focus checkpoints

## Code Changes (no new files)

- `src/pages/onboarding_planner.py` — Add `st.text_area` for focus notes
- `src/ai/prompts/onboarding_planner.py` — Conditionally append focus section

## Testing

```bash
cd src && pytest tests/ -k "focus"
```

Verify:
- Empty focus notes = baseline 008 behavior
- Focus notes about "safety" produce safety-prioritized plan
- Multiple focus areas all addressed in output
- Focus notes persist across regenerations
- 1,000 char limit enforced
