# Quickstart: One-Click Copy & Markdown Download

## Overview

Cross-cutting utility providing copy-to-clipboard, .md file
download, and per-section copy for all AI module outputs.

## Prerequisites

- Features 001 (auth), 003 (shell), at least one AI module (004/006/008)
- HTTPS for clipboard API (localhost works for development)

## How It Works

1. AI module generates output and stores in session state
2. Module page calls shared helpers after rendering output:
   - `render_copy_button(text)` — clipboard copy via JS
   - `render_download_button(text, slug)` — .md file download
   - `render_section_copy_buttons(text)` — per-section copy

## Code Location

- `src/components/copy_button.py` — Clipboard copy helper
- `src/components/download_button.py` — Download helper
- Each module page imports from `src/components/`

## Usage in a Module Page

```python
from src.components.copy_button import render_copy_button, render_section_copy_buttons
from src.components.download_button import render_download_button

# After rendering output
if output:
    col1, col2 = st.columns(2)
    with col1:
        render_copy_button(output)
    with col2:
        render_download_button(output, "requirement-analysis")
    render_section_copy_buttons(output)
```

## Testing

```bash
cd src && pytest tests/ -k "copy or download"
```

Verify:
- Copy button copies full markdown to clipboard
- "Copied!" confirmation visible for 2 seconds
- Download produces .md file with correct filename pattern
- Per-section copy copies only one section
- Buttons hidden/disabled when no output
- Clipboard fallback message on non-HTTPS
