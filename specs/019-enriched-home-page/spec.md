# Feature Specification: Enriched Home Page

**Feature Branch**: `019-enriched-home-page`
**Created**: 2026-03-04
**Status**: Implemented
**Input**: User description: "As a user, I want a polished home page with the company logo, a hero banner, step-by-step guide, user tips, audience descriptions, and a branded footer so the app feels complete and guides users on first visit."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Branded Hero Banner (Priority: P1)

When an authenticated user lands on the Home page, they
see a prominent hero banner at the top with:
- The Versaterm white logo.
- A large welcome title ("Welcome to Versaterm Academy").
- A subtitle describing the platform's purpose.

The banner uses the same dark gradient (charcoal to navy)
used across other module headers for visual consistency.

**Why this priority**: The hero banner is the first thing
users see. It establishes brand identity and communicates
the platform's purpose instantly.

**Independent Test**: Log in and land on the Home page.
Confirm the hero banner shows the white logo, title, and
subtitle on the dark gradient background.

**Acceptance Scenarios**:

1. **Given** the user lands on the Home page,
   **When** the page loads,
   **Then** a hero banner with logo, title, and subtitle
   is prominently displayed.

2. **Given** the logo file is missing,
   **When** the page renders,
   **Then** the title and subtitle still display correctly
   (graceful degradation).

---

### User Story 2 - How It Works Guide (Priority: P2)

Below the hero banner, a "How It Works" section displays
three numbered steps explaining the workflow:
1. Choose a Module
2. Provide Context
3. Generate & Export

Each step shows a numbered teal circle, step title, and
brief description arranged in a 3-column layout.

**Why this priority**: New users need guidance on how to
use the platform. This eliminates confusion on first visit.

**Independent Test**: View the Home page and confirm three
steps are displayed with numbered circles, titles, and
descriptions in a horizontal layout.

**Acceptance Scenarios**:

1. **Given** the user views the Home page,
   **When** they scroll below the hero,
   **Then** a "How It Works" section with 3 steps is visible.

2. **Given** the three steps are displayed,
   **When** the user reads them,
   **Then** each step has a numbered circle, title, and
   descriptive text.

---

### User Story 3 - Module Cards with Navigation (Priority: P1)

An "Available Modules" section displays cards for each
module: Requirement Analyzer, KB Article Generator,
Onboarding Planner, and Company Resources. Each card shows
an icon, title, description, and an "Open" button. Clicking
a button navigates to that module.

**Why this priority**: Module cards are the primary
navigation mechanism from the home page.

**Independent Test**: Click "Open Requirement Analyzer" on
the home page and confirm navigation to the Requirement
Analyzer module.

**Acceptance Scenarios**:

1. **Given** the user views the module cards,
   **When** they click "Open [Module Name]",
   **Then** the sidebar selection updates and the module
   renders.

2. **Given** the module cards are displayed,
   **When** the user views them,
   **Then** each card shows an icon, title, and description
   with a teal top-border accent.

---

### User Story 4 - Tips and Audience Guidance (Priority: P3)

Two side-by-side cards provide additional guidance:
- **Tips for Best Results** — practical advice on uploading
  documents, being specific with inputs, using CV upload,
  and export capabilities.
- **Who Is This For?** — audience breakdown listing Product
  Managers, Technical Writers, Team Leads & HR, and New
  Employees with role-specific descriptions.

**Why this priority**: Additional guidance helps users get
maximum value but the page is functional without it.

**Independent Test**: View the Home page and confirm two
guidance cards are displayed side-by-side below the module
cards.

**Acceptance Scenarios**:

1. **Given** the user scrolls below the module cards,
   **When** they view the guidance section,
   **Then** two cards ("Tips for Best Results" and "Who Is
   This For?") are displayed side-by-side.

2. **Given** the user reads the Tips card,
   **When** they review the content,
   **Then** they see practical advice about document upload
   and input quality.

---

### User Story 5 - About Banner and Footer (Priority: P3)

An "About Versaterm" banner (dark gradient) provides
company context. Below it, a footer displays:
- The Versaterm dark logo.
- "Versaterm Academy — AI-Powered Training & Development"
  tagline.
- Copyright notice.

**Why this priority**: Footer and about section add polish
and completeness to the page.

**Independent Test**: Scroll to the bottom of the Home page
and confirm the About banner and footer with logo and
copyright are visible.

**Acceptance Scenarios**:

1. **Given** the user scrolls to the bottom,
   **When** they view the footer,
   **Then** the dark logo, tagline, and copyright are
   displayed.

---

### Edge Cases

- What happens if logo files are missing? The page renders
  without logos — all text content remains intact.
- What happens on narrow screens? Cards stack vertically
  and the step circles remain readable.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Home page MUST display a branded hero banner
  with white logo, title, and subtitle.
- **FR-002**: Home page MUST display a "How It Works"
  section with 3 numbered steps.
- **FR-003**: Home page MUST display module cards for all
  available modules with navigation buttons.
- **FR-004**: Module "Open" buttons MUST navigate to the
  corresponding module.
- **FR-005**: Home page MUST display "Tips for Best Results"
  and "Who Is This For?" guidance cards.
- **FR-006**: Home page MUST display an "About Versaterm"
  banner with company description.
- **FR-007**: Home page MUST display a footer with dark
  logo, tagline, and copyright.
- **FR-008**: All headings MUST use `<div>` elements (not
  `<h1>`/`<h3>`) to avoid CSS specificity conflicts with
  Streamlit's theme system.
- **FR-009**: Logo rendering MUST support both SVG (white)
  and PNG (dark) formats with base64 embedding.

### Key Entities

- **Module Card**: A navigation card for an app module.
  Attributes: icon, title, description, navigation key.
- **Step**: A "How It Works" step. Attributes: number,
  title, description.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of module navigation buttons work
  correctly.
- **SC-002**: The hero banner, steps, module cards, tips,
  about banner, and footer are all visible on first load.
- **SC-003**: Logo renders correctly in both hero (white)
  and footer (dark) positions.
- **SC-004**: 90% of first-time users understand how to use
  the platform after reading the Home page.

## Assumptions

- The Home page is the default landing page after
  authentication (first item in the sidebar).
- Logo files are located at src/assets/logo.png and
  src/assets/logo-white.svg.
- The page is purely informational and navigational — no
  AI functionality or data input.
- Dependencies: 003-app-shell-layout (sidebar navigation),
  013-branded-theme (visual consistency).
