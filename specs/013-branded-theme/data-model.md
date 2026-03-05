# Data Model: Professional Branded Theme

No persistent data. No session state. Configuration-only feature.

## Configuration Constants (config.py)

### Branding

| Constant | Type | Value | Description |
|----------|------|-------|-------------|
| BRAND_LOGO_PATH | str | "src/assets/logo.png" | Path to logo image file |
| BRAND_TITLE | str | "Versaterm Academy" | Application title text |
| BRAND_SUBTITLE | str | "AI-Powered Employee Assistant" | Tagline text |

### Colors

| Constant | Type | Value | Description |
|----------|------|-------|-------------|
| BRAND_PRIMARY_COLOR | str | "#1B4F72" | Primary accent (buttons, links, headings) |
| BRAND_SIDEBAR_BG | str | "#2C3E50" | Sidebar background |
| BRAND_SIDEBAR_TEXT | str | "#ECF0F1" | Sidebar text color |
| BRAND_BG_COLOR | str | "#FFFFFF" | Main content background |
| BRAND_SECONDARY_BG | str | "#F8F9FA" | Secondary background (cards, panels) |
| BRAND_TEXT_COLOR | str | "#2C3E50" | Main text color |

## Streamlit Theme Config (.streamlit/config.toml)

```toml
[theme]
primaryColor = "#1B4F72"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F8F9FA"
textColor = "#2C3E50"
font = "sans serif"
```

## CSS Injection Targets

| Selector | Property | Value | Purpose |
|----------|----------|-------|---------|
| [data-testid="stSidebar"] | background-color | #2C3E50 | Dark sidebar |
| [data-testid="stSidebar"] * | color | #ECF0F1 | Light sidebar text |
| h1 | font-size, font-weight, color | 2rem, 700, #1B4F72 | Heading level 1 |
| h2 | font-size, font-weight, color | 1.5rem, 600, #1B4F72 | Heading level 2 |
| h3 | font-size, font-weight, color | 1.25rem, 600, #1B4F72 | Heading level 3 |
| body | font-family | system font stack | Consistent typography |

## Relationships

- **Depends on**: 003-app-shell-layout (sidebar structure to style)
- **Compatible with**: 011-demo-banner (banner renders above themed
  header; banner's amber color contrasts with navy theme)
- **Compatible with**: 012-local-doc-grounding (upload UI inherits
  sidebar styling)
- **Affects**: All pages — login screen, sidebar, all module pages
