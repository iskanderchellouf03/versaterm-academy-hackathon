# Quickstart: Demo Scope Banner

## Overview

Displays a fixed amber banner on every page communicating
demo status and no-persistence policy. Dismissible per session.

## Prerequisites

- Feature 003 (app shell layout) for consistent page structure

## How It Works

1. `app.py` calls `render_demo_banner()` at the very top
2. Function checks `st.session_state["banner_dismissed"]`
3. If not dismissed: renders fixed HTML banner with dismiss button
4. If dismissed: renders nothing
5. Banner appears on login screen and all authenticated pages

## Code Location

- `src/components/demo_banner.py` — Banner component
- `src/app.py` — Call site (top of file, before auth gate)
- `src/config.py` — `DEMO_BANNER_TEXT` constant

## Customizing Banner Text

Edit `DEMO_BANNER_TEXT` in `src/config.py`:
```python
DEMO_BANNER_TEXT = "Beta — Data is not persisted between sessions."
```

## Removing the Banner

Delete the `render_demo_banner()` call in `app.py` and
optionally remove `src/components/demo_banner.py`.

## Testing

```bash
cd src && pytest tests/ -k "banner"
```

Verify:
- Banner visible on login screen
- Banner visible on all authenticated pages
- Dismiss hides banner for current session
- New session shows banner again
- Banner doesn't overlap functional controls
