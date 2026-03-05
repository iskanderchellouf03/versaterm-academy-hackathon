# Implementation Plan: Professional Branded Theme

**Branch**: `013-branded-theme` | **Date**: 2026-03-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/013-branded-theme/spec.md`

## Summary

Apply a professional branded theme across the entire Streamlit app:
logo, title, subtitle in sidebar/login, neutral color palette via
Streamlit's `config.toml` theming, and consistent typography via
injected CSS. All branding values (logo path, title, subtitle,
colors) configurable from `src/config.py`. Uses `st.markdown` with
`unsafe_allow_html=True` for CSS injection and `st.image` for logo.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit (theming, layout, CSS injection)
**Storage**: N/A (no data storage — purely visual)
**Testing**: pytest (unit tests for config, visual verification manual)
**Target Platform**: Web (Streamlit app)
**Project Type**: Cross-cutting visual enhancement to web application
**Performance Goals**: N/A (static CSS/HTML — negligible overhead)
**Constraints**: Single light theme only, no dark mode, no theme switching
**Scale/Scope**: Applies to all pages (login, sidebar, all modules)

## Constitution Check

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. User-Centric Design | PASS | "Polished header with logo immediately conveys professionalism." Direct demo value for leadership presentation. |
| II. Simplicity First | PASS | Streamlit native `config.toml` for colors, `st.image` for logo, `st.markdown` for CSS. No external CSS framework, no build step. |
| MVP-first | PASS | US1 (logo/title/subtitle) is independently demoable. Color palette and typography are incremental polish. |
| Demo-ready | PASS | Professional appearance for leadership demo. |
| No gold-plating | PASS | No dark mode, no theme switching, no custom fonts requiring downloads. System font stack only. |
| Tech stack | PASS | Pure Streamlit + inline CSS. Zero new dependencies. |
| Single-repo | PASS | Logo image stored in repo. All config in Python. |

**Post-design re-check**: PASS. Zero new dependencies. All theming
uses Streamlit's built-in capabilities (`config.toml`, `st.markdown`
with HTML/CSS, `st.image`).

## Project Structure

### Documentation (this feature)

```text
specs/013-branded-theme/
├── plan.md
├── research.md
├── data-model.md
└── quickstart.md
```

### Source Code (repository root)

```text
src/
├── components/
│   └── branding.py          # Logo + title + subtitle rendering
├── theme/
│   ├── __init__.py
│   └── css.py               # CSS injection function (colors, fonts)
├── assets/
│   └── logo.png             # Logo image file (placeholder)
├── config.py                # (modify) — add BRAND_* constants
└── app.py                   # (modify) — call render_branding(), inject_css()

.streamlit/
└── config.toml              # Streamlit theme configuration (colors)
```

**Structure Decision**: New `src/theme/` package for CSS injection.
New `src/components/branding.py` for logo/title rendering. New
`src/assets/` for static files (logo). Streamlit's native
`.streamlit/config.toml` for primary/background/text colors.

## Complexity Tracking

No constitution violations. Zero new dependencies.
