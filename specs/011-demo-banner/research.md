# Research: Demo Scope Banner

## R1 — Fixed Banner in Streamlit

**Decision**: Use `st.markdown()` with `unsafe_allow_html=True`
to inject a styled `<div>` with inline CSS for fixed
positioning, background color, and padding. The banner
renders at the top of every page.

**Rationale**: Streamlit has no native "banner" or "toast"
component that stays fixed. `st.markdown` with HTML/CSS is
the standard approach for custom fixed elements. Inline CSS
avoids external stylesheet files.

**Alternatives considered**:
- `st.warning()` or `st.info()`: These are not fixed — they
  scroll with content and disappear on rerun. Rejected —
  FR-003 requires fixed positioning.
- `st.toast()`: Temporary notification, disappears after a
  few seconds. Rejected — banner must be persistent.
- Custom Streamlit component: Over-engineering for a static
  banner. Rejected per Simplicity First.
- CSS file injection via `st.set_page_config()`: Streamlit
  doesn't support external CSS. Rejected.

## R2 — Dismiss Mechanism

**Decision**: Add a small "Dismiss" button rendered via
Streamlit (`st.button`) placed in a column next to the
banner text. When clicked, set
`st.session_state["banner_dismissed"] = True`. The
`render_demo_banner()` function checks this flag and skips
rendering if True.

**Rationale**: Session state persists for the tab's WebSocket
lifetime — matches "dismissed for current session" (FR-006).
New tab/re-auth = new session state = banner reappears
(FR-007). No database needed.

**Alternatives considered**:
- JavaScript-based dismiss (hide DOM element): Works but
  resets on every Streamlit rerun (Streamlit re-renders the
  full page). Rejected — would flash on each interaction.
- CSS-only dismiss: Not possible without JS or server state.
  Rejected.
- No dismiss at all: Violates FR-006. Rejected.

## R3 — Banner Styling

**Decision**: Contrasting background color (amber/yellow),
dark text, centered content, small font. Fixed to top of
viewport via `position: fixed; top: 0; z-index: 999`.
Add `padding-top` to the main content container to prevent
overlap (FR-004).

**Rationale**: Amber/yellow is universally associated with
warnings and notices. High contrast ensures readability
(FR-008). Fixed positioning keeps it visible during scroll
(FR-003). Z-index ensures it's above Streamlit's own
elements.

**Alternatives considered**:
- Red banner: Too alarming — suggests error. Rejected.
- Blue/info banner: Blends too much with Streamlit defaults.
  Rejected.
- Bottom-of-page banner: Less visible on first impression.
  Rejected.

## R4 — Configurable Banner Text

**Decision**: Store banner text as `DEMO_BANNER_TEXT` in
`src/config.py`. Default: "Demo — This is a prototype. No
data is persisted. All information is local to your current
session."

**Rationale**: Single location for text updates. Easy to
change from "demo" to "beta" or remove entirely when the
app graduates from prototype status.

**Alternatives considered**:
- Hardcoded in the component: Works but violates FR edge
  case about easy updates. Rejected.
- Environment variable: Over-engineering for static text.
  Rejected.

## R5 — Login Screen Visibility

**Decision**: Call `render_demo_banner()` at the very top of
`app.py`, before the auth gate check. This ensures the banner
appears on both the login screen and all authenticated pages.

**Rationale**: FR-001 requires the banner on "every page,
including the login screen." Placing the call before the auth
gate guarantees this.

**Alternatives considered**:
- Separate banner call in login page and in shell: Duplicates
  the call. Rejected — single call at top of app.py is DRY.
