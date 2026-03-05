# Data Model: AI Requirement Analyzer

This feature is stateless — no persistent data entities.
All data exists in Streamlit session state during the active
session only.

## Session State: Requirement Input

| Field | Type | Description |
|-------|------|-------------|
| req_input_text | string | Raw requirement text entered by user |

### Validation Rules

- MUST NOT be empty (FR-003)
- Maximum 5,000 characters (FR-001); truncated with warning if exceeded

## Session State: Analysis Output

| Field | Type | Description |
|-------|------|-------------|
| req_analysis_result | string | Full Markdown output from LLM |
| req_analysis_loading | bool | Whether analysis is in progress |

### Output Sections (within req_analysis_result)

The Markdown string contains five `##` sections in this
fixed order (enforced by 014-structured-output-format):

1. **Rewritten Requirements** — Clear, testable requirement statements
2. **Acceptance Criteria** — Given/When/Then scenarios
3. **Test Cases** — Concrete test scenarios with expected outcomes
4. **Edge Cases** — Boundary conditions and unusual scenarios
5. **Risks** — Potential issues, assumptions, gaps

### State Transitions

```
[Empty]
  → User types/pastes text → req_input_text set
  → User clicks "Analyze" → req_analysis_loading=True
  → LLM responds → req_analysis_result set, req_analysis_loading=False
  → User edits input → req_input_text updated
  → User clicks "Analyze" again → previous result replaced
```

## Shared Entity: LLM Client Configuration

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| api_key | string | `OPENAI_API_KEY` env var | API authentication |
| base_url | string | `OPENAI_BASE_URL` env var | API endpoint (default: OpenAI) |
| model | string | `OPENAI_MODEL` env var | Model name (default: `gpt-4o`) |
| timeout | int | hardcoded | 30 seconds per spec |

## Relationships

- Module registered in `src/pages/__init__.py` (from 003)
- Uses shared LLM client from `src/ai/client.py`
- Uses output formatting from `src/output/` (from 014)
- Auth gate required (001)
