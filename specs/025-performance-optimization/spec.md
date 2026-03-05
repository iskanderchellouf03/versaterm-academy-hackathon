# Feature Specification: Performance Optimization

**Feature Branch**: `025-performance-optimization`
**Created**: 2026-03-05
**Status**: Implemented

## Summary

Optimized app startup and module switching speed by eliminating eager imports, caching CSS/logo generation, and avoiding redundant DB operations.

## Changes

### Lazy Module Loading
- `src/modules/__init__.py` changed from eager imports to wrapper functions
- Each module only imports when the user navigates to it
- OpenAI package no longer loaded at startup for non-AI pages (Home, Company Resources)

### Lazy + Singleton OpenAI Client
- `from openai import AzureOpenAI` moved inside `get_client()` function
- Client instance cached in module-level `_client` variable — created once, reused

### Cached CSS Generation
- Theme CSS and Login CSS strings built via `@lru_cache(maxsize=1)`
- Large f-strings computed once per process, reused on every Streamlit rerun

### Cached Logo Base64
- Logo file reads and base64 encoding cached with `@lru_cache`
- Applied in `branding.py`, `home.py`, `company_resources.py`, `app.py`

### DB Init Guard
- `init_db()` tracks `_db_initialized` flag — DDL only runs once per process

## Key Files
- `src/modules/__init__.py` — Lazy wrapper functions
- `src/ai/client.py` — Lazy import + singleton
- `src/theme/css.py` — `_build_theme_css()` and `_build_login_css()` with `lru_cache`
- `src/components/branding.py` — `_logo_b64()` with `lru_cache`
- `src/auth/db.py` — `_db_initialized` guard
