# versaterm-academy-hackathon Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-03-05

## Active Technologies
- Python 3.11+ + Streamlit (UI rendering, session state, theming, CSS injection)
- `openai` Python package (Azure OpenAI LLM API client)
- `PyPDF2` (PDF text extraction), `python-docx` (DOCX text extraction)
- `re` (stdlib — regex for Markdown normalization and section parsing)
- `html` (stdlib — escaping user content in HTML)
- `base64`, `os` (stdlib — logo embedding, file paths)
- `functools.lru_cache` (stdlib — CSS, logo, and client caching)
- In-memory storage via Streamlit session state (no disk persistence)

## Project Structure

```text
src/
  app.py                  # Main entry point, login flow, sidebar, module dispatch, nav arrows, shared footer
  config.py               # All configuration: env vars, brand settings, resource data, JIRA config
  assets/
    logo.png              # Dark logo (for light backgrounds / footer)
    logo-white.svg        # White logo (for dark gradient headers)
  auth/
    db.py                 # SQLite auth database (with init guard)
    service.py            # Auth logic: validate, generate code, sessions
    email.py              # SMTP email sending
  ai/
    client.py             # Azure OpenAI client wrapper (lazy import + singleton)
    prompts/
      grounding.py        # Document grounding context injection
      requirement_analyzer.py  # Requirement analyzer system prompt (with scoring)
  docs/
    extractor.py          # Text extraction from PDF/DOCX/TXT/CSV + chunking
    store.py              # In-memory document store (session state)
    retriever.py          # TF-IDF document retrieval (retrieve_top_k)
  export/
    formatters.py         # Markdown-to-JIRA and Markdown-to-Confluence converters
    jira_client.py        # JIRA ticket creation (mock + real mode)
  modules/
    __init__.py           # Module registry (lazy-loaded MODULES dict)
    home.py               # Home page: hero, steps, module cards, tips
    requirement_analyzer.py   # Requirement analysis: scoring, product context, JIRA, Send to QA Lab
    qa_test_lab.py            # QA Test Lab: ticket queue, test suite generation, chat refinement
    kb_article_generator.py   # Article Writer: audience/tone pills, preview tabs
    onboarding_planner.py     # Onboarding plans: CV upload, company/product, knowledge base
    company_resources.py      # Company resources: product card selector, categorized links
    placeholder.py            # Placeholder renderer
  ai/prompts/
    qa_test_lab.py        # QA Test Lab AI prompts (SYSTEM_PROMPT, CHAT_FOLLOWUP_PROMPT)
  output/
    schema.py             # Module output section schemas (includes "027" for QA Test Lab)
  components/
    branding.py           # Reusable branding component (cached logo + title)
    demo_banner.py        # Dismissible demo/prototype banner
    copy_button.py        # Clipboard copy button component
    download_button.py    # File download button component
  theme/
    css.py                # Global CSS injection (cached theme, sidebar, login, typography)
.streamlit/
  config.toml             # Streamlit theme config (colors, font)
specs/                    # Feature specifications (001–027)
```

## Commands

cd src; pytest; ruff check .

## Code Style

- Python 3.11+: Follow standard conventions
- Custom HTML uses `<div>` for headings (not `<h1>`/`<h3>`) to avoid CSS specificity conflicts with Streamlit theme
- **All custom HTML must be single-line concatenated strings** — indented HTML in triple-quote f-strings gets treated as markdown code blocks (4+ spaces = `<pre>`)
- Inline styles use `!important` for color overrides in custom HTML blocks
- Use CSS class injection via `<style>` blocks when global CSS overrides inline styles (e.g., `.jira-badge` for link colors)
- CSS heading rules scoped to `[data-testid="stMarkdownContainer"] > h1/h2/h3` only
- Always `html.escape()` user-generated content before injecting into HTML strings
- Use `@lru_cache` for expensive repeated computations (CSS strings, logo base64, client instances)
- Lazy-load modules and heavy imports (openai) — only import when needed

## Feature Inventory

| # | Feature | Status | Key Files |
|---|---------|--------|-----------|
| 001 | Employee Auth (email + code) | Implemented | `auth/`, `app.py` |
| 002 | Session & Logout | Implemented | `auth/service.py`, `app.py` |
| 003 | App Shell Layout (sidebar nav) | Implemented | `app.py`, `modules/__init__.py` |
| 004 | Requirement Analyzer | Implemented | `modules/requirement_analyzer.py` |
| 005 | NFR & Platform Context | Implemented | `modules/requirement_analyzer.py`, `config.py` |
| 006 | KB Article Generator | Implemented | `modules/kb_article_generator.py` |
| 007 | KB Audience & Tone | Implemented | `modules/kb_article_generator.py`, `config.py` |
| 008 | Onboarding Plan Generator | Implemented | `modules/onboarding_planner.py` |
| 009 | Onboarding Focus Notes | Implemented | `modules/onboarding_planner.py` |
| 010 | Copy/Download Export | Implemented | `modules/*.py` |
| 011 | Demo Banner | Implemented | `components/demo_banner.py` |
| 012 | Local Document Grounding | Partially Deprecated | `docs/`, `ai/prompts/grounding.py` (sidebar upload removed) |
| 013 | Branded Theme | Implemented | `theme/css.py`, `components/branding.py`, `.streamlit/config.toml` |
| 014 | Structured Output Format | Implemented | `modules/*.py` |
| 015 | CV Upload & AI Analysis | Implemented | `modules/onboarding_planner.py` |
| 016 | Company & Product Selection | Implemented | `modules/onboarding_planner.py`, `config.py` |
| 017 | Per-Product Knowledge Base | Implemented | `modules/onboarding_planner.py` |
| 018 | Company Resources Module | Implemented | `modules/company_resources.py`, `config.py` |
| 019 | Enriched Home Page | Implemented | `modules/home.py` |
| 020 | Onboarding Planner UI Overhaul | Implemented | `modules/onboarding_planner.py` |
| 021 | Requirement Analyzer UI + Enhancements | Implemented | `modules/requirement_analyzer.py`, `export/`, `ai/prompts/` |
| 022 | Article Writer UI Overhaul | Implemented | `modules/kb_article_generator.py` |
| 023 | JIRA & Confluence Export | Implemented | `export/formatters.py`, `export/jira_client.py` |
| 024 | Company Resources UX Redesign | Implemented | `modules/company_resources.py` |
| 025 | Performance Optimization | Implemented | `modules/__init__.py`, `ai/client.py`, `theme/css.py`, `auth/db.py` |
| 026 | Sidebar & Navigation Enhancements | Implemented | `app.py`, `theme/css.py` |
| 027 | QA Test Lab | Implemented | `modules/qa_test_lab.py`, `ai/prompts/qa_test_lab.py` |

## Recent Changes
- Sidebar nav: replaced st.radio with st.button per module (fixes cross-group selection bugs)
- Logout button: red stroke style via #sidebar_logout CSS ID, visually distinct from nav buttons
- Removed: sidebar "Dismiss Banner" button (render_banner_dismiss)
- TestLink added to Company Resources: global + per-product (Kore, Komlog, SIT911, Kontact, Komuync)
- 027-qa-test-lab: AI test suite generation from tickets or manual input, chat refinement, JIRA/score badges
- Sidebar grouped navigation: General, Planning, Quality groups with audience hints
- Home page 3-2 card grid layout (3 top + 2 centered bottom)
- Removed: sidebar document upload, build_grounding_context calls, difflib version compare, CSV export
- 026-sidebar-navigation: User avatar, active page highlight, page nav arrows, shared footer, login fixes
- 025-performance-optimization: Lazy imports, cached CSS/logos, singleton OpenAI client, DB init guard


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
