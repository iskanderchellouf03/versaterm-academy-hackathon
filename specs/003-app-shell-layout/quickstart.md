# Quickstart: App Shell Layout with Sidebar Navigation

## Overview

The app shell provides the authenticated layout: a left
sidebar for module switching and a main content area that
renders the selected module.

## Prerequisites

- Feature 001-employee-auth (auth gate)
- Feature 002-session-logout (sign-out button in sidebar)

## How It Works

1. User authenticates (001)
2. `app.py` renders the shell: sidebar + main content
3. Sidebar shows module list via `st.sidebar.radio()`
4. User clicks a module → `st.session_state["active_module"]`
   updates → content area renders that module's page function
5. Sign-out button (002) sits below the module list

## Code Location

- `src/app.py` — Shell layout, auth gate, sidebar, dispatch
- `src/pages/__init__.py` — Module registry (`MODULES` dict)
- `src/pages/placeholder.py` — Placeholder for unbuilt modules

## Adding a New Module

1. Create `src/pages/my_module.py` with a `render()` function
2. In `src/pages/__init__.py`, add:
   ```python
   from src.pages.my_module import render as my_module_render

   MODULES = {
       ...
       "My Module": my_module_render,
   }
   ```
3. The sidebar and dispatch automatically pick it up.

## Running

```bash
streamlit run src/app.py
```

## Testing

```bash
cd src && pytest tests/ -k "shell or layout or sidebar"
```

Verify:
- Sidebar renders all modules from the registry
- Clicking a module updates the content area
- Default module loads on first visit
- Unauthenticated users see login, not the shell
