# Data Model: One-Click Copy & Markdown Download

No persistent data. This feature operates on the existing
output strings already in session state from each module.

## Inputs (from existing session state)

| Source Module | Session State Key | Type |
|---------------|-------------------|------|
| 004 Requirement Analyzer | req_analysis_result | string (Markdown) |
| 006 KB Article Generator | kb_article_edited | string (Markdown) |
| 008 Onboarding Planner | onb_plan_result | string (Markdown) |

## Derived Data

### Section Parsing (for per-section copy)

Sections are extracted by splitting output on `\n## `
headings. Each section includes its heading and body.

| Field | Type | Description |
|-------|------|-------------|
| heading | string | Section heading text (e.g., "Test Cases") |
| content | string | Full section: heading + body text |

### Download Filename

Generated as: `{module_slug}-{YYYY-MM-DD}.md`

| Module | Slug | Example Filename |
|--------|------|------------------|
| 004 | requirement-analysis | requirement-analysis-2026-03-04.md |
| 006 | kb-article | kb-article-2026-03-04.md |
| 008 | onboarding-plan | onboarding-plan-2026-03-04.md |

## Relationships

- Reads output from each module's session state
- No writes to session state (read-only utility)
- Compatible with 014 structured output (relies on `##`
  headings for section splitting)
