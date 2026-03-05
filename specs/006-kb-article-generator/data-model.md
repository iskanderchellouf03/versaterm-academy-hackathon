# Data Model: KB Article Generator

Stateless feature — no persistent data. All state in
Streamlit session state.

## Session State: KB Input

| Field | Type | Description |
|-------|------|-------------|
| kb_input_text | string | Raw text entered by user |

### Validation Rules

- MUST NOT be empty (FR-003)
- Maximum 10,000 characters (FR-001); truncated with warning

## Session State: KB Output

| Field | Type | Description |
|-------|------|-------------|
| kb_article_result | string | Full Markdown article from LLM |
| kb_article_edited | string | User-edited version (from text_area) |
| kb_article_loading | bool | Whether generation is in progress |

### Output Sections (within kb_article_result)

Enforced by 014-structured-output-format, four `##` sections:

1. **Title** — Concise, under 80 characters
2. **Summary** — 1-2 sentence overview
3. **Body** — Headings, numbered steps, clear paragraphs
4. **Tags** — 3-7 keywords

### State Transitions

```
[Empty]
  → User pastes text → kb_input_text set
  → User clicks "Generate" → kb_article_loading=True
  → LLM responds → kb_article_result set, kb_article_edited=result, loading=False
  → User edits output → kb_article_edited updated
  → User clicks "Generate" again → previous result/edits replaced
```

## Relationships

- Registered in `src/pages/__init__.py` (from 003)
- Uses shared LLM client from `src/ai/client.py` (from 004)
- Uses output formatting from `src/output/` (from 014)
- Auth gate required (001)
