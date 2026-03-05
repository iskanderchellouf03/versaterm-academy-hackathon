# Data Model: Onboarding Focus Notes

No persistent storage. Extends 008 session state.

## Session State: Focus Notes (extends 008)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| onb_focus_notes | string | "" | Optional free-text focus areas |

### Validation Rules

- Optional (empty is valid)
- Maximum 1,000 characters (enforced by `st.text_area(max_chars=1000)`)

## Prompt Behavior

| Focus Notes State | Prompt Section | Effect on Output |
|-------------------|----------------|------------------|
| Empty | Omitted entirely | Baseline 008 behavior |
| Non-empty | "Priority Focus Areas" appended | Activities frontloaded, terms included, checkpoints added |

## Relationships

- Extends 008's session state (adds `onb_focus_notes`)
- Value passed to prompt builder in
  `src/ai/prompts/onboarding_planner.py`
- No new entities, no database changes
