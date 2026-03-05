# Implementation Plan: Structured Output Formatting

**Branch**: `014-structured-output-format` | **Date**: 2026-03-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/014-structured-output-format/spec.md`

## Summary

Enforce strict section headings, concise tone, and clean
Markdown across all AI module outputs (004, 006, 008). This
is a cross-cutting feature implemented through: (1) a shared
output format configuration that defines per-module section
headings and order, (2) system prompt templates that embed
formatting rules (structure, tone, Markdown style), and
(3) a lightweight Markdown normalizer that post-processes
LLM output to fix minor formatting inconsistencies (e.g.,
`*` → `-` for lists, stray HTML removal).

No new UI pages. No new data storage. This feature provides
utilities consumed by each AI module during output generation.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit (UI rendering), `re` (stdlib — regex for Markdown normalization)
**Storage**: N/A (no persistence)
**Testing**: pytest
**Target Platform**: Web (Streamlit app)
**Project Type**: Cross-cutting library module within web application
**Performance Goals**: Post-processing adds < 50ms to output rendering
**Constraints**: All Python ecosystem, no external dependencies beyond stdlib + Streamlit
**Scale/Scope**: 3 AI modules (004, 006, 008), extensible to future modules

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after
Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. User-Centric Design | PASS | Directly supports employee use case: "predictable, scannable outputs ready to paste into Confluence/Jira." Every FR maps to reducing manual editing work. |
| II. Simplicity First | PASS | Uses stdlib `re` for normalization, plain Python dicts for section config. No templating engine, no AST parser. |
| MVP-first | PASS | Section heading enforcement (US1/P1) is independently demoable. Tone and Markdown polish are incremental. |
| Demo-ready | PASS | Outputs are usable even without this feature; this adds polish. |
| No gold-plating | PASS | No Markdown AST parsing, no automated summarization, no truncation logic. Simple regex-based normalization only. |
| Tech stack | PASS | Pure Python. |
| Single-repo | PASS | All code in this repository. |

**Post-design re-check**: PASS — no violations introduced
during Phase 1 design.

## Project Structure

### Documentation (this feature)

```text
specs/014-structured-output-format/
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
├── output/
│   ├── __init__.py
│   ├── schema.py          # Per-module section definitions (names, order)
│   ├── prompt.py           # System prompt builder for formatting rules
│   └── normalizer.py       # Post-process LLM output (fix Markdown)
└── config.py               # Shared config (already planned in 001)
```

**Structure Decision**: Single `src/output/` package added
to the existing `src/` tree. Three files: schema (section
definitions), prompt (system prompt builder), normalizer
(Markdown cleanup). Each AI module (004, 006, 008) will
import from `src/output/` when generating responses.

## Complexity Tracking

No violations to justify. All choices align with constitution
principles.
