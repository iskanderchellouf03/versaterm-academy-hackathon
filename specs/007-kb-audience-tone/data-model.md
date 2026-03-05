# Data Model: KB Audience & Tone Selection

No persistent storage. Extends 006 session state.

## Session State: Generation Context (extends 006)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| kb_audience | string | "Internal" | Selected audience |
| kb_tone | string | "Formal" | Selected tone |

## Constants: Audiences

| Value | Prompt Description |
|-------|--------------------|
| Internal | Internal employees. Company jargon OK, reference internal tools, assume product knowledge. |
| External | External customers. Plain language, no jargon, full context for outsiders. |
| Support | Support agents. Troubleshooting structure, step-by-step resolution, ticket/escalation references. |

## Constants: Tones

| Value | Prompt Description |
|-------|--------------------|
| Formal | Professional third-person. Passive voice OK. No contractions or colloquialisms. |
| Conversational | Friendly second-person ("you"). Contractions OK. Approachable and warm. |
| Concise | Minimal prose. Bullet lists, imperative voice, short sentences. Quick-reference style. |

## Valid Combinations

All 9 audience × tone combinations (3 × 3) are valid. No
restricted pairings.

## Relationships

- Extends 006's session state (adds `kb_audience` and
  `kb_tone` alongside `kb_input_text`)
- Both values passed to the prompt builder in
  `src/ai/prompts/kb_article_generator.py`
- No new entities, no database changes
