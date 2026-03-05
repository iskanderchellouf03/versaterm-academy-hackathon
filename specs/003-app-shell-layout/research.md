# Research: App Shell Layout with Sidebar Navigation

## R1 — Streamlit Sidebar Navigation Pattern

**Decision**: Use `st.sidebar.radio()` to render module names
as a selectable list. Track the selected module in
`st.session_state["active_module"]`. Dispatch to the
corresponding page function using a dict lookup.

**Rationale**: `st.sidebar.radio()` provides built-in active
state highlighting, keyboard accessibility, and a clean UI
without custom CSS. It renders as a vertical list of options
with the selected item visually distinguished. Combined with
a dispatch dict (`{"Module Name": render_function}`), this
is the simplest pattern for single-page module switching in
Streamlit.

**Alternatives considered**:
- `st.sidebar.selectbox()`: Dropdown is less scannable than
  radio buttons for a small number of modules. Rejected —
  sidebar radio is more visible.
- `st.sidebar.button()` per module: Requires manual state
  tracking and no built-in active highlighting. More code
  for the same result. Rejected.
- Streamlit multipage app (`pages/` directory convention):
  Creates separate URL routes per page with Streamlit's
  built-in page navigation. However, this adds file-system
  coupling and the sidebar is auto-generated with less
  control over ordering and naming. Rejected — the dict-based
  dispatch gives full control over the module list.
- Third-party router (e.g., `streamlit-option-menu`): Adds
  external dependency. Rejected per Simplicity First.

## R2 — Module Registry Design

**Decision**: A `MODULES` ordered dict in `src/pages/__init__.py`
mapping display name → render function. Each module registers
by adding an entry. The shell reads this dict to build the
sidebar and dispatch.

**Rationale**: Centralizes module registration in one file.
Adding a new module = adding one import + one dict entry.
No decorators, no auto-discovery, no class hierarchy.

**Alternatives considered**:
- Auto-discovery via directory scan: Magic behavior, harder
  to debug, requires naming conventions. Rejected per
  Simplicity First.
- Decorator-based registration: Over-abstraction for 3-5
  modules. Rejected — YAGNI.
- Config file (YAML/JSON): Adds parsing overhead. The
  registry is code, not config. Rejected.

## R3 — Responsive Sidebar Behavior

**Decision**: Rely on Streamlit's built-in sidebar collapse
behavior. Streamlit automatically renders the sidebar as
collapsible on narrow screens (< ~768px). No custom CSS
needed.

**Rationale**: Streamlit's default responsive behavior
satisfies FR-007 (sidebar collapses on narrow screens) out
of the box. The sidebar gets a toggle hamburger menu on
mobile viewports. Testing confirms this works on Chrome,
Firefox, and Safari.

**Alternatives considered**:
- Custom CSS media queries: Streamlit's CSS injection
  (`st.markdown(unsafe_allow_html=True)`) is fragile and
  breaks across Streamlit versions. Rejected.
- JavaScript-based responsive logic: Violates Python-only
  constraint. Rejected.

## R4 — Placeholder Pages for Unimplemented Modules

**Decision**: Create a single `placeholder.py` with a
`render_placeholder(module_name)` function that displays
"[Module Name] — Coming soon." All unimplemented modules
point to this function in the registry.

**Rationale**: Ensures the shell is demoable before any AI
modules are built (per spec edge case: "no content yet →
placeholder message"). One function handles all placeholders
via the module name parameter.

**Alternatives considered**:
- Empty page (blank screen): Violates spec edge case
  requirement. Rejected.
- Per-module placeholder files: Unnecessary duplication for
  identical content. Rejected.

## R5 — Visual Separation (Sidebar vs Content)

**Decision**: Use Streamlit's default sidebar styling, which
provides a distinct background color and border between
sidebar and main content. Optionally add a subtle divider
line via `st.sidebar.divider()` between navigation and the
sign-out button area.

**Rationale**: Streamlit's built-in sidebar already satisfies
FR-008 (clear visual separation) with its default gray
background against the white content area. No custom CSS
needed for MVP.

**Alternatives considered**:
- Custom CSS for sidebar colors: Over-engineering for MVP.
  Feature 013 (branded theme) will handle theming later.
  Rejected.
