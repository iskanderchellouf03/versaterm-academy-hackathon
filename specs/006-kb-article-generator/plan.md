# Implementation Plan: KB Article Generator

**Branch**: `006-kb-article-generator` | **Date**: 2026-03-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/006-kb-article-generator/spec.md`

## Summary

Build the second AI module: a KB Article Generator that
accepts messy notes or raw text and produces a structured
knowledge base article (Title, Summary, Body, Tags). Uses
the shared LLM client from 004, structured output formatting
from 014, and registers as a module in the app shell (003).
Includes editable output via `st.text_area` and copy
functionality.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit (UI), `openai` (shared from 004)
**Storage**: N/A (stateless — no article history)
**Testing**: pytest
**Target Platform**: Web (Streamlit app)
**Project Type**: Web application (Streamlit) — AI module
**Performance Goals**: 90% of generations within 15 seconds
**Constraints**: All Python, 10,000 char input limit, 30s timeout
**Scale/Scope**: Single module within the app shell (003)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after
Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. User-Centric Design | PASS | KMS/Support/QA use case: "paste messy notes, get clean KB article." Directly accelerates documentation workflow. |
| II. Simplicity First | PASS | Single LLM call, reuses shared client (004) and output formatting (014). One new page file + one prompt file. |
| MVP-first | PASS | US1 (generate article) is independently demoable. Copy (US2) and edit/regen (US3) are incremental. |
| Demo-ready | PASS | Paste notes, click Generate, see structured article. Immediately impressive. |
| No gold-plating | PASS | No article history, no templates, no WYSIWYG editor, no auto-redaction. |
| Tech stack | PASS | Pure Python + Streamlit + openai. |
| Single-repo | PASS | All code in repo. |

**Post-design re-check**: PASS — no violations.

## Project Structure

### Documentation (this feature)

```text
specs/006-kb-article-generator/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```text
src/
├── pages/
│   ├── __init__.py              # (modify) — register kb_article_generator
│   └── kb_article_generator.py  # Module UI: input, generate, editable output
├── ai/
│   ├── client.py                # (existing from 004)
│   └── prompts/
│       └── kb_article_generator.py  # System prompt for 006
├── output/                      # (existing from 014)
└── config.py                    # (existing)
```

**Structure Decision**: Follows the same pattern as 004. New
page file + new prompt file. Reuses shared `ai/client.py`
and `output/` package. No new packages or directories beyond
what's established.

## Complexity Tracking

No violations to justify. All choices align with constitution
principles.
