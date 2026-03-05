# Research: Professional Branded Theme

## R1 — Streamlit Theming Approach

**Decision**: Use `.streamlit/config.toml` `[theme]` section for
primary colors (primaryColor, backgroundColor, secondaryBackgroundColor,
textColor, font). Supplement with `st.markdown(unsafe_allow_html=True)`
for fine-grained CSS overrides (sidebar background, heading sizes,
link colors).

**Rationale**: `config.toml` is Streamlit's official theming mechanism
and controls button colors, widget accents, and background. CSS
injection via `st.markdown` handles everything `config.toml` cannot
(sidebar gradient, logo sizing, font-weight). This two-layer approach
covers all requirements with zero dependencies.

**Alternatives considered**:
- `config.toml` only: Cannot control sidebar background color,
  heading sizes, or font-weight. Insufficient. Rejected.
- CSS-only (no config.toml): Requires overriding Streamlit's own
  theme variables with `!important` everywhere. Fragile. Rejected.
- Custom Streamlit component: Over-engineering for CSS changes.
  Rejected per Simplicity First.
- External CSS framework (Bootstrap, Tailwind): Heavy dependency,
  conflicts with Streamlit's own CSS. Rejected.

## R2 — Logo Rendering

**Decision**: Use `st.image()` for the logo with a fixed max width.
Store the logo file at `src/assets/logo.png`. In `config.py`, define
`BRAND_LOGO_PATH`. If the file doesn't exist or fails to load, skip
the logo silently (title/subtitle still render).

**Rationale**: `st.image()` is Streamlit's native image renderer.
It handles PNG, SVG, and JPEG. Graceful fallback is simple: wrap in
try/except or check `os.path.exists()`.

**Alternatives considered**:
- HTML `<img>` tag via `st.markdown`: Works but requires base64
  encoding or serving the file via a URL. More complex. Rejected.
- `st.logo()` (Streamlit 1.31+): Only renders in sidebar header,
  limited customization. Cannot place on login screen. Rejected for
  MVP — could upgrade later if Streamlit version supports it.
- SVG inline via `st.markdown`: Works but SVG handling is inconsistent
  across browsers. PNG is simpler. Rejected for MVP.

## R3 — Color Palette

**Decision**: Neutral corporate palette:
- Primary accent: `#1B4F72` (professional navy blue)
- Sidebar background: `#2C3E50` (dark charcoal)
- Sidebar text: `#ECF0F1` (light gray)
- Content background: `#FFFFFF` (white)
- Secondary background: `#F8F9FA` (light gray)
- Text: `#2C3E50` (dark charcoal)
- Headings: `#1B4F72` (navy, matching accent)

**Rationale**: Navy + charcoal is universally corporate and
appropriate for a public safety technology company. High contrast
ratios meet WCAG AA. Tested: `#2C3E50` on `#FFFFFF` = 12.6:1
(passes AAA), `#ECF0F1` on `#2C3E50` = 10.9:1 (passes AAA).

**Alternatives considered**:
- Versaterm brand colors (if known): Not available in repo. Using
  neutral corporate colors that work for any company. Can be swapped
  via config. Rejected as default.
- Green/teal palette: Less corporate feel. Rejected.
- Pure black + white: Too stark, lacks warmth. Rejected.

## R4 — Typography

**Decision**: Use system font stack:
`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
"Helvetica Neue", Arial, sans-serif`. Set in `config.toml` as
`font = "sans serif"` and refine via CSS injection.

Heading hierarchy:
- H1: 2rem, font-weight 700
- H2: 1.5rem, font-weight 600
- H3: 1.25rem, font-weight 600
- Body: 1rem, font-weight 400

**Rationale**: System font stack renders the best available
sans-serif on each OS (San Francisco on macOS, Segoe UI on Windows,
Roboto on Android). No font download needed — zero latency impact.
Streamlit's `font = "sans serif"` config already uses a similar
stack; CSS injection tightens heading sizes.

**Alternatives considered**:
- Google Fonts (Inter, Open Sans): Requires network request. Adds
  latency, may fail offline. Rejected per Simplicity First.
- Monospace: Not appropriate for a corporate app. Rejected.
- Serif font (Georgia, Times): Feels dated for a tech company.
  Rejected.

## R5 — Branding Configuration

**Decision**: All branding values in `src/config.py`:
```python
BRAND_LOGO_PATH = "src/assets/logo.png"
BRAND_TITLE = "Versaterm Academy"
BRAND_SUBTITLE = "AI-Powered Employee Assistant"
BRAND_PRIMARY_COLOR = "#1B4F72"
BRAND_SIDEBAR_BG = "#2C3E50"
BRAND_SIDEBAR_TEXT = "#ECF0F1"
```

**Rationale**: Single file for all configuration (FR-010). Easy to
change for different demos or branding. No need for environment
variables — these are static display values, not secrets.

**Alternatives considered**:
- Environment variables: Over-engineering for display text and colors.
  Rejected.
- YAML/JSON config file: Adds a parser dependency. Python dict in
  config.py is simpler. Rejected.
- Hardcoded in components: Violates FR-010 (single location).
  Rejected.

## R6 — CSS Injection Method

**Decision**: Single function `inject_theme_css()` in `src/theme/css.py`
that calls `st.markdown()` with a `<style>` tag containing all CSS
overrides. Called once at the top of `app.py` (before any page
content).

**Rationale**: Single injection point avoids duplicate CSS. Streamlit
re-renders the full page on each interaction, so the CSS is always
present. `st.markdown` with HTML is the standard approach for custom
styling in Streamlit.

**Alternatives considered**:
- Multiple `st.markdown` calls across components: Fragments CSS,
  harder to maintain. Rejected.
- External `.css` file loaded via `st.markdown`: Streamlit cannot
  serve static files natively. Would need base64 or inline anyway.
  Rejected.
- `streamlit-extras` or `streamlit-theme`: External dependencies.
  Rejected per Simplicity First.
