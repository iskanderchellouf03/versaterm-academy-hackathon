# Quickstart: NFR & Platform Context

## Overview

Adds system type selection and NFR checkboxes to the
Requirement Analyzer (004). The selected context is injected
into the LLM prompt for platform- and quality-aware output.

## Prerequisites

- Feature 004 (requirement analyzer) must be implemented
- All 004 prerequisites (001 auth, 003 shell, LLM API key)

## How It Works

1. User selects system type (defaults to "Web")
2. User optionally checks NFRs (Performance, Security, etc.)
3. User pastes requirement and clicks "Analyze"
4. Prompt builder appends platform context + NFR descriptions
5. LLM produces platform-aware, quality-constrained analysis

## Code Changes (no new files)

- `src/pages/requirement_analyzer.py` — Add `st.selectbox` + `st.multiselect`
- `src/ai/prompts/requirement_analyzer.py` — Extend prompt with context injection
- `src/config.py` — Add `SYSTEM_TYPES` and `NFR_OPTIONS` constants

## Usage

```python
# In the prompt builder
def build_prompt(requirement, system_type, nfrs):
    context = f"Target system: {system_type}."
    if nfrs:
        context += " NFRs: " + ", ".join(nfrs) + "."
    return base_prompt + "\n\n" + context + "\n\nRequirement:\n" + requirement
```

## Testing

```bash
cd src && pytest tests/ -k "nfr or platform"
```

Verify:
- System type defaults to "Web" when unselected
- Mobile selection produces mobile-specific test cases
- Multiple NFRs produce quality-specific items
- No NFRs selected = baseline 004 behavior
- Selections persist across re-analyses in same session
