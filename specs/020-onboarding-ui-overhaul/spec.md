# Feature Specification: Onboarding Planner UI Overhaul

**Feature Branch**: `020-onboarding-ui-overhaul`
**Created**: 2026-03-04
**Status**: Implemented
**Input**: User description: "As a user, I want the Onboarding Planner to have a modern, visually appealing UI with step indicators, styled sections, metric cards, tabbed results, and branded headers/footers — matching the polish level of the rest of the app."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Step Progress Indicator (Priority: P1)

At the top of the Onboarding Planner, a visual step
progress bar shows 3 steps:
1. Upload CV (Optional)
2. Configure Plan
3. Generated Plan

The current step is highlighted in teal. Completed steps
show a different visual state. This helps users understand
where they are in the workflow.

**Why this priority**: The step indicator provides
orientation in a multi-section page. Without it, the page
feels like a long disconnected form.

**Independent Test**: Open the Onboarding Planner and
confirm the 3-step indicator is visible at the top with
appropriate visual states.

**Acceptance Scenarios**:

1. **Given** the user opens the Onboarding Planner,
   **When** the page loads,
   **Then** a 3-step progress indicator is visible.

2. **Given** the user is in the CV upload section,
   **When** they view the step indicator,
   **Then** Step 1 is highlighted as active.

---

### User Story 2 - Branded Header and Footer (Priority: P2)

The page displays:
- A dark gradient header with the white Versaterm logo,
  page title, and description.
- A footer with the dark logo, tagline, and copyright.

These match the visual pattern used on the Home page and
Company Resources module.

**Why this priority**: Consistent branding across all
modules creates a polished, cohesive experience.

**Independent Test**: Open the Onboarding Planner and
confirm the branded header and footer are visible and
match the Home page style.

**Acceptance Scenarios**:

1. **Given** the user opens the Onboarding Planner,
   **When** the page loads,
   **Then** a branded header with logo and title is
   displayed on a dark gradient background.

2. **Given** the user scrolls to the bottom,
   **When** they view the footer,
   **Then** the dark logo and tagline are displayed.

---

### User Story 3 - Styled Form Sections (Priority: P2)

Each major section (CV Upload, Plan Configuration) is
wrapped in a styled card with:
- Section label with teal left-border accent.
- Light background container.
- Consistent padding and border radius.

Form inputs are organized in a clean column layout within
styled containers.

**Why this priority**: Styled sections create visual
hierarchy and make the form feel organized rather than a
flat list of inputs.

**Independent Test**: Confirm each section has a labeled
header with teal accent and is wrapped in a styled card.

**Acceptance Scenarios**:

1. **Given** the user views the Plan Configuration section,
   **When** they see the form inputs,
   **Then** inputs are inside a styled card with a teal
   left-border section label.

---

### User Story 4 - Tabbed Results Display (Priority: P2)

When a plan is generated, the results are displayed in
tabs rather than a single long document:
- **Overview** — What It Is, Why It Matters, Key Terms.
- **Learning Plan** — The day-by-day 2-week schedule.
- **Checkpoints** — Milestone assessments and self-checks.

Copy and download actions are available above the tabs.

**Why this priority**: Tabs break up long content and
let users focus on specific sections. This is especially
valuable for plans that can be 2000+ words.

**Independent Test**: Generate a plan and confirm the
output is split into 3 tabs with correct content in each.
Confirm copy/download still work.

**Acceptance Scenarios**:

1. **Given** a plan is generated,
   **When** the results display,
   **Then** content is organized into 3 tabs: Overview,
   Learning Plan, Checkpoints.

2. **Given** the user clicks the "Learning Plan" tab,
   **When** the tab content loads,
   **Then** the day-by-day schedule is displayed.

3. **Given** the user clicks Copy or Download,
   **When** the action executes,
   **Then** the complete plan (all tabs) is copied or
   downloaded.

---

### Edge Cases

- What happens if the AI output doesn't contain clear
  section markers for tab splitting? The full plan is
  displayed in the first tab with other tabs empty or
  hidden.
- What happens if the plan is very short? Tabs still
  display — short content is fine.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display a 3-step progress
  indicator at the top of the Onboarding Planner.
- **FR-002**: System MUST display a branded header with
  white logo, title, and description on a dark gradient.
- **FR-003**: System MUST display a footer with dark logo
  and tagline.
- **FR-004**: Each form section MUST be wrapped in a styled
  card with a teal-accented section label.
- **FR-005**: Generated plan results MUST be displayed in
  3 tabs: Overview, Learning Plan, Checkpoints.
- **FR-006**: Copy and Download actions MUST export the
  complete plan content (all tabs combined).
- **FR-007**: All headings in custom HTML MUST use `<div>`
  elements to avoid CSS specificity conflicts.
- **FR-008**: The CV analysis MUST render in styled metric
  cards, skill pills, and timeline entries.

### Key Entities

- **Step Indicator**: Visual progress bar. Attributes:
  step number, title, active state.
- **Result Tabs**: Tabbed output container. Tabs: Overview,
  Learning Plan, Checkpoints.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Step indicator displays correctly on 100%
  of page loads.
- **SC-002**: Tabbed results split content correctly for
  90% of generated plans.
- **SC-003**: Copy/Download export the full plan (all tabs)
  in 100% of cases.
- **SC-004**: 85% of users rate the UI as "modern and
  professional" compared to the previous plain layout.

## Assumptions

- The tab splitting logic uses keyword matching on section
  headers (e.g., "Learning Plan", "Checkpoint") in the
  generated markdown. The exact parsing is an implementation
  detail.
- The step indicator is purely visual — it does not enforce
  a linear workflow. Users can interact with any section
  at any time.
- CSS uses inline styles with `<div>` elements to avoid
  Streamlit theme specificity conflicts (learned from
  013-branded-theme).
- Dependencies: 008-onboarding-plan-generator (base module),
  013-branded-theme (visual patterns), 015-cv-upload-analysis
  (CV dashboard), 010-copy-download-export (copy/download).
