# Research: Session Sign-Out

## R1 — Streamlit Session Termination

**Decision**: Clear all authentication-related keys from
`st.session_state` and call `st.rerun()` to force the app
back to the login gate.

**Rationale**: Streamlit has no built-in "logout" or "session
destroy" API. Session state is a Python dict scoped to the
browser tab's WebSocket connection. Clearing auth keys
(`authenticated`, `user_email`, etc.) and rerunning the
script effectively resets the user to the unauthenticated
state. This is the standard Streamlit pattern for logout.

**Alternatives considered**:
- `st.session_state.clear()`: Clears everything, including
  non-auth state. Too aggressive — may wipe module-specific
  data unnecessarily. Rejected for now; can revisit if no
  other state exists.
- Redirect to a separate logout page: Over-engineering for
  a single Streamlit app. Rejected per Simplicity First.
- Server-side session store (Redis, database): Adds external
  dependency for no value — Streamlit session state is
  already server-side (in the Streamlit process memory).
  Rejected.

## R2 — Sign-Out Button Placement

**Decision**: Place the "Sign out" button in the Streamlit
sidebar, below navigation but always visible. Use
`st.sidebar.button("Sign out")`.

**Rationale**: The sidebar is persistent across all pages in
a Streamlit app (spec 003 establishes sidebar as the primary
navigation container). Placing sign-out there ensures FR-001
(visible on every authenticated page) and FR-006 (text label,
not icon-only). Bottom of sidebar is a conventional location
for account actions.

**Alternatives considered**:
- Top-right header area: Streamlit has limited control over
  the top bar. Would require custom CSS injection. Rejected
  per Simplicity First.
- Separate settings page: Violates FR-001 (must be visible
  on every page without navigation). Rejected.

## R3 — Browser Back Button Protection

**Decision**: No special handling needed. Streamlit apps
re-execute the full script on every interaction (including
back-button-triggered loads). The auth gate at the top of
`app.py` checks `st.session_state.get("authenticated")`.
After logout, this check fails, and the user sees the login
screen regardless of navigation history.

**Rationale**: Streamlit's execution model inherently
protects against cached page access. There is no static HTML
to cache — every render is server-driven. The browser back
button triggers a rerun, which hits the auth gate.

**Alternatives considered**:
- Cache-Control headers: Not exposed by Streamlit's API.
  Unnecessary given the rerun model. Rejected.
- JavaScript-based history manipulation: Violates Python-
  only constraint. Rejected.

## R4 — Multi-Tab Behavior

**Decision**: Each Streamlit tab has its own independent
session state (tied to its WebSocket connection). Signing
out in one tab only affects that tab. Other tabs remain
authenticated until their next rerun, at which point the
session is still valid (different WebSocket = different
session state).

**Rationale**: Streamlit does not share session state across
tabs. True multi-tab session invalidation would require a
server-side session store (e.g., database), which is
over-engineering for an MVP. The spec acknowledges this:
"Other tabs MUST redirect to the login screen on their next
interaction." Since each tab is independent, "next
interaction" in another tab will still have its own valid
session — this is acceptable per the spec's "next server
interaction" language for the MVP.

**Alternatives considered**:
- Shared session store with invalidation: Adds database
  dependency and polling/push logic. Rejected per MVP-first
  and Simplicity First.
- BroadcastChannel API (JavaScript): Violates Python-only
  stack. Rejected.
