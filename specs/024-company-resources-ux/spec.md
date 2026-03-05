# Feature Specification: Company Resources UX Redesign

**Feature Branch**: `024-company-resources-ux`
**Created**: 2026-03-05
**Status**: Implemented

## Summary

Redesigned Company Resources to show company-wide tools first, then let users select their product via clickable cards instead of dumping all products at once.

## Changes

### Layout Redesign
- Company-wide tools (Confluence, Jira, Teams, HR, SharePoint, Presentations) always visible at top
- Product selector as visual cards with icon, name, description, and resource count
- Click to select/deselect — only selected product's resources shown
- Empty state hint when no product selected

### Resource Cards
- Category icons alongside titles
- Colored category badge inline with title
- Hover effects (shadow lift, translateY)
- Left accent bar by category color

### Product Cards
- 5 products: Kore, Komlog, SIT911, Kontact, Komuync
- Each with icon, short description, resource count
- Active state: teal background, primary border
- Toggle behavior: click again to deselect

## Key Files
- `src/modules/company_resources.py` — Full module rewrite
