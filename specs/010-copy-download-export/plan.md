# Implementation Plan: One-Click Copy & Markdown Download

**Branch**: `010-copy-download-export` | **Date**: 2026-03-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/010-copy-download-export/spec.md`

## Summary

Build a cross-cutting copy/download utility used by all AI
modules. Provides: (1) "Copy" button using a small JS snippet
via `st.components.v1.html()` for clipboard access, (2)
"Download" button using `st.download_button()` for .md file
export, (3) per-section copy icons for multi-section outputs.
Implemented as shared helper functions imported by each module
page.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit (`st.download_button`, `st.components.v1.html`)
**Storage**: N/A (no persistence)
**Testing**: pytest
**Target Platform**: Web (Streamlit app, HTTPS assumed)
**Project Type**: Cross-cutting utility within web application
**Performance Goals**: Copy confirmation within 500ms
**Constraints**: All Python (minimal JS for clipboard API only), single repo
**Scale/Scope**: 3 AI modules (004, 006, 008), extensible

## Constitution Check

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. User-Centric Design | PASS | "Copy/download for reuse in Confluence, Jira, docs." Directly accelerates employee workflow. |
| II. Simplicity First | PASS | `st.download_button` is built-in. Clipboard requires minimal JS (6 lines). Shared helpers, not a framework. |
| MVP-first | PASS | US1 (full-output copy) is independently demoable. Download (US2) and per-section (US3) are incremental. |
| Demo-ready | PASS | Click Copy, paste into Confluence. Instant demo value. |
| No gold-plating | PASS | No PDF/HTML/DOCX export, no email integration, no share links. |
| Tech stack | PASS | Python + Streamlit. Minimal JS for clipboard only (browser API, not a dependency). |
| Single-repo | PASS | All code in repo. |

**Post-design re-check**: PASS. The small JS snippet for
clipboard is justified — Streamlit has no native clipboard
API. Constitution says "Full-stack Python" but clipboard
access is a browser API that requires JS by definition. This
is a 6-line utility, not a framework dependency.

## Project Structure

### Documentation (this feature)

```text
specs/010-copy-download-export/
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
├── components/
│   ├── __init__.py
│   ├── copy_button.py       # Clipboard copy via st.components.v1.html
│   └── download_button.py   # st.download_button wrapper with filename generation
├── pages/
│   ├── requirement_analyzer.py   # (modify) — use shared copy/download
│   ├── kb_article_generator.py   # (modify) — use shared copy/download
│   └── onboarding_planner.py     # (modify) — use shared copy/download
└── config.py                     # (unchanged)
```

**Structure Decision**: New `src/components/` package for
shared UI utilities. Two files: `copy_button.py` (clipboard)
and `download_button.py` (file download). Each module page
imports and calls these helpers. Replaces per-module copy
implementations from 004/006/008.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Small JS snippet (6 lines) | Browser Clipboard API requires JavaScript — no pure-Python alternative exists | `st.code()` copy icon works for code blocks only, not arbitrary markdown content |
