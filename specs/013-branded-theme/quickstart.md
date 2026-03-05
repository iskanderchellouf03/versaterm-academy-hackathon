# Quickstart: Professional Branded Theme

## Overview

Professional visual theme for the Streamlit app: logo, title,
subtitle, corporate color palette, and consistent typography.
All values configurable from `src/config.py`.

## Prerequisites

- Feature 003 (app shell layout) for sidebar structure
- A logo image file at `src/assets/logo.png` (optional — fallback
  to text-only if missing)

## How It Works

1. `.streamlit/config.toml` sets Streamlit's native theme colors
2. `app.py` calls `inject_theme_css()` at the top to inject
   custom CSS overrides (sidebar, headings, fonts)
3. `app.py` calls `render_branding()` in the sidebar to display
   logo + title
4. Login screen also calls `render_branding()` for consistent
   appearance

## Code Location

- `.streamlit/config.toml` — Streamlit native theme colors
- `src/theme/css.py` — CSS injection function
- `src/components/branding.py` — Logo + title + subtitle component
- `src/assets/logo.png` — Logo image file
- `src/config.py` — All BRAND_* constants

## Changing the Branding

Edit `src/config.py`:
```python
BRAND_TITLE = "Your App Name"
BRAND_SUBTITLE = "Your Tagline"
BRAND_PRIMARY_COLOR = "#FF6600"  # Your accent color
BRAND_SIDEBAR_BG = "#333333"    # Your sidebar color
```

## Changing the Logo

Replace `src/assets/logo.png` with your logo file. Keep the
filename the same, or update `BRAND_LOGO_PATH` in `config.py`.

## Testing

```bash
cd src && pytest tests/ -k "theme or brand"
```

Verify:
- Logo, title, subtitle visible on login screen
- Logo and title visible in sidebar on all pages
- Color palette consistent across all pages
- Text meets WCAG AA contrast (4.5:1 body, 3:1 large text)
- Single font family used throughout
- Graceful fallback when logo file is missing
- Branding changes by editing only config.py
