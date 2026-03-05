# Data Model: Onboarding Plan Generator

Stateless feature — no persistent storage. All state in
Streamlit session state.

## Session State: Onboarding Inputs

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| onb_role | string | "" | New hire's job function (free text) |
| onb_product | string | "" | Versaterm product name (free text) |
| onb_level | string | "Beginner" | Experience level (Beginner/Intermediate/Advanced) |

### Validation Rules

- All three fields MUST be non-empty (FR-004)
- Level MUST be one of: Beginner, Intermediate, Advanced

## Session State: Plan Output

| Field | Type | Description |
|-------|------|-------------|
| onb_plan_result | string | Full Markdown plan from LLM |
| onb_plan_loading | bool | Whether generation is in progress |

### Output Sections (within onb_plan_result)

Enforced by 014-structured-output-format, five `##` sections:

1. **What It Is** — Product overview (text)
2. **Why It Matters** — Value framed for the role (text)
3. **Key Terms** — Minimum 5 term-definition pairs (list)
4. **Learning Plan** — Day 1-10 schedule (structured list)
5. **Checkpoints** — Minimum 2 assessment items (list)

### State Transitions

```
[Empty]
  → User fills role, product, level
  → User clicks "Generate Plan" → onb_plan_loading=True
  → LLM responds → onb_plan_result set, loading=False
  → User changes inputs → fields updated
  → User clicks "Generate Plan" again → previous result replaced
```

## Constants: Experience Levels

| Value | Prompt Behavior |
|-------|-----------------|
| Beginner | Start with fundamentals, no assumed knowledge, gradual progression |
| Intermediate | Assume basic familiarity, focus on workflows and integrations |
| Advanced | Skip basics, focus on expert workflows, edge cases, advanced config |

## Relationships

- Registered in `src/pages/__init__.py` (from 003)
- Uses shared LLM client from `src/ai/client.py` (from 004)
- Uses output formatting from `src/output/` (from 014)
- Auth gate required (001)
- Can be enhanced by 009 (focus notes) and 012 (doc grounding)
