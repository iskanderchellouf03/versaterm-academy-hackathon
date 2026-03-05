# Feature Specification: JIRA & Confluence Export

**Feature Branch**: `023-jira-confluence-export`
**Created**: 2026-03-05
**Status**: Implemented

## Summary

Export AI-generated requirement analysis to JIRA markup, Confluence HTML, and create JIRA tickets directly from the app.

## Changes

### Markdown-to-JIRA Converter
- `## Heading` to `h3. Heading`
- `- item` to `* item`
- `**bold**` to `*bold*`
- Metadata header with system type and NFRs

### Markdown-to-Confluence Converter
- `## Heading` to `<h2>`
- Bullets to `<ul><li>`
- Info/warning macros for Risks section
- Metadata panel at top

### JIRA Ticket Creation
- Mock mode (default): simulates ticket creation with random key, styled card UI
- Real mode: calls JIRA REST API v3 with basic auth
- Auto-generates labels from system type and NFR selections
- Config via environment variables: `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, `JIRA_PROJECT_KEY`, `JIRA_MOCK_MODE`

### Download Buttons
- Three side-by-side: Markdown (.md), JIRA (.txt), Confluence (.html)

## Key Files
- `src/export/formatters.py` — `to_jira()` and `to_confluence()` converters
- `src/export/jira_client.py` — `create_ticket()` with mock/real dual mode
- `src/config.py` — JIRA environment variable configuration
