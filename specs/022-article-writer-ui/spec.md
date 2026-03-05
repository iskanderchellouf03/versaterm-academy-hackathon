# Feature Specification: Article Writer UI Overhaul

**Feature Branch**: `022-article-writer-ui`
**Created**: 2026-03-05
**Status**: Implemented

## Summary

Renamed "KB Article Generator" to "Article Writer" for clarity. Full UI redesign with modern pill selectors, structured preview, and improved UX.

## Changes

### Rename
- Module renamed from "KB Article Generator" to "Article Writer" across sidebar, home page cards, and hero header

### UI Overhaul
- Dark gradient hero header with logo and description
- Audience selector as pill buttons with icons and descriptions (Internal/External/Support)
- Tone selector as pill buttons with icons (Formal/Conversational/Concise)
- Yellow privacy reminder card
- Character counter for input text

### Structured Output
- Preview/Edit tabs for results
- Title rendered prominently in styled card
- Tags as colored pill badges
- Body and Summary as separate section cards with colored borders
- Context badges showing audience + tone used during generation

## Key Files
- `src/modules/kb_article_generator.py` — Full module rewrite
- `src/modules/__init__.py` — Registry key updated
- `src/modules/home.py` — MODULE_CARDS entry updated
