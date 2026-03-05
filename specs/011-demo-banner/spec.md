# Feature Specification: Demo Scope Banner

**Feature Branch**: `011-demo-banner`
**Created**: 2026-03-04
**Status**: Partially Implemented
**Input**: User description: "As the web owner, I want a visible demo banner ('no persistence, local only') so stakeholders understand scope and data handling at a glance at least for now."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Persistent Demo Banner on All Pages (Priority: P1)

Any person viewing the app — whether an authenticated
employee, a stakeholder in a demo, or someone evaluating
the tool — sees a prominent banner at the top of every page.
The banner clearly communicates two key messages:

1. This is a **demo/prototype** — not a production system.
2. **No data is persisted** — all data is local and
   session-only.

The banner is always visible, cannot be accidentally
dismissed, and does not interfere with the app's
functionality. It sets expectations immediately so
stakeholders do not mistake the prototype for a finished
product or assume their data is being saved.

**Why this priority**: This is the entire feature — a single
visible element that communicates scope. Without it,
stakeholders may make incorrect assumptions about the app's
maturity and data handling.

**Independent Test**: Open the app (authenticated or on the
login screen), and confirm the banner is visible at the top
of the page with text communicating "demo" and "no data
persistence". Navigate to different modules and confirm the
banner remains visible on every page.

**Acceptance Scenarios**:

1. **Given** any user visits the app,
   **When** any page loads (including the login screen),
   **Then** a banner is visible at the top of the page with
   text indicating this is a demo with no data persistence.

2. **Given** an authenticated user navigates between modules,
   **When** each module page renders,
   **Then** the banner remains visible and does not
   disappear or move.

3. **Given** the banner is displayed,
   **When** the user scrolls down the page,
   **Then** the banner remains fixed at the top of the
   viewport (always visible).

4. **Given** the banner is displayed,
   **When** the user interacts with the app normally,
   **Then** the banner does not overlap or obscure any
   functional controls (input fields, buttons, output
   areas).

---

### User Story 2 - Banner Dismissibility (Priority: P2)

To reduce visual noise during extended use, the user can
optionally dismiss the banner for the current session. A
small "X" or "Dismiss" control on the banner hides it. The
banner reappears on the next session (new browser tab or
after re-authentication) to ensure first-time viewers always
see it.

**Why this priority**: The banner is most important on first
impression. During an extended demo or working session, it
may become distracting. Session-scoped dismissal balances
visibility with usability. The app is functional without
this (US1 covers the core need).

**Independent Test**: Dismiss the banner, navigate between
modules to confirm it stays hidden, then close and reopen
the browser tab (or log out and back in) to confirm the
banner reappears.

**Acceptance Scenarios**:

1. **Given** the banner is displayed,
   **When** the user clicks the dismiss control,
   **Then** the banner is hidden for the remainder of the
   current session.

2. **Given** the user has dismissed the banner,
   **When** they navigate between modules,
   **Then** the banner remains hidden.

3. **Given** the user has dismissed the banner and starts a
   new session (new tab or re-authentication),
   **When** the page loads,
   **Then** the banner is visible again.

---

### Edge Cases

- What happens on very narrow screens (mobile width)? The
  banner adapts to the screen width. Text may wrap but MUST
  remain fully readable. The banner MUST NOT consume more
  than 15% of the viewport height.
- What happens if the banner text needs to be updated later
  (e.g., changing from "demo" to "beta")? The banner text
  is configurable — stored in a single location so it can
  be updated without modifying multiple files. This is an
  implementation convenience assumption, not a user-facing
  requirement.
- What happens when the banner is shown on the login screen
  (before authentication)? The banner is visible on the
  login screen as well. It does not require authentication
  to display.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display a banner at the top of
  every page, including the login screen.
- **FR-002**: The banner MUST contain text that clearly
  communicates: (a) the application is a demo/prototype,
  and (b) no data is persisted beyond the current session.
- **FR-003**: The banner MUST be fixed to the top of the
  viewport so it remains visible during scrolling.
- **FR-004**: The banner MUST NOT overlap or obscure any
  functional UI elements (buttons, inputs, output areas).
- **FR-005**: The banner MUST be visually distinct from the
  rest of the UI (e.g., contrasting background color) so it
  is immediately noticeable.
- **FR-006**: The banner MUST include an optional dismiss
  control that hides the banner for the current session
  only.
- **FR-007**: After dismissal, the banner MUST reappear on
  the next session (new browser tab or re-authentication).
- **FR-008**: The banner MUST be readable on all supported
  screen sizes without truncation. Text may wrap but MUST
  remain fully visible.
- **FR-009**: The banner MUST NOT consume more than 15% of
  the viewport height on any screen size.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The banner is visible on 100% of pages
  (including login) for users who have not dismissed it.
- **SC-002**: 95% of first-time viewers can identify the
  app as a demo and understand that data is not persisted
  within 5 seconds of seeing the banner.
- **SC-003**: The banner does not interfere with any
  functional interaction — 0% of users report the banner
  blocking a button, input, or output area.
- **SC-004**: After dismissal, the banner does not reappear
  until a new session begins in 100% of cases.

## Assumptions

- The default banner text is: "Demo — This is a prototype.
  No data is persisted. All information is local to your
  current session." The exact wording can be adjusted but
  MUST convey both the demo status and the no-persistence
  message.
- The banner is a temporary feature. It is expected to be
  removed or replaced when the application moves beyond the
  demo/prototype stage. The feature is designed for easy
  removal.
- The banner appears on all pages regardless of
  authentication status — it is the first thing stakeholders
  see, even before logging in.
- This feature has no dependencies on specific AI modules.
  It depends only on 003-app-shell-layout (page layout
  structure) for consistent placement across pages.
- The dismiss state is session-scoped (not persisted to a
  database). It is stored in the same mechanism as the user
  session.

> **Note (2026-03-05)**: The sidebar "Dismiss Banner" button
> (`render_banner_dismiss`) has been removed. The banner itself
> (`render_demo_banner`) still renders at the top of all pages.
> The dismiss functionality is no longer exposed in the sidebar
> UI. FR-006 and FR-007 are no longer active.
