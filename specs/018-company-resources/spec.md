# Feature Specification: Company Resources Module

**Feature Branch**: `018-company-resources`
**Created**: 2026-03-04
**Status**: Implemented
**Input**: User description: "As a new hire or employee, I want a dedicated module with quick links to Confluence, Jira, SharePoint, and other company resources organized by product, so I can find everything I need in one place."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Browse Company Resources (Priority: P1)

An employee navigates to the "Company Resources" module
from the sidebar. They see a branded header with the
Versaterm logo, followed by a product filter dropdown.

Resources are organized into two tiers:
1. **Global resources** — available to all employees
   (Confluence wiki, Jira dashboard, Teams, HR portal,
   SharePoint, Presentations).
2. **Product-specific resources** — per-product links to
   technical docs (SharePoint), Confluence space, and Jira
   board for each Komutel product (Kore, Komlog, SIT911,
   Kontact, Komuync).

Each resource is displayed as a clickable card with:
- Category label (color-coded: Documentation, Knowledge
  Base, Project Management, Communication, HR & Onboarding,
  Presentations).
- Title and description.
- External link arrow opening in a new tab.

**Why this priority**: This is the entire module's purpose
— providing quick access to company resources.

**Independent Test**: Open Company Resources, confirm
global resources are visible. Select "Kore" from the
product filter, confirm Kore-specific resources appear
first, followed by global resources.

**Acceptance Scenarios**:

1. **Given** the user opens Company Resources,
   **When** "All Products" is selected (default),
   **Then** global resources and all product resources
   are displayed.

2. **Given** the user selects a specific product (e.g.,
   "Kore"),
   **When** the page updates,
   **Then** Kore resources appear first, then global
   resources, then other products below.

3. **Given** the user clicks a resource card,
   **When** the link opens,
   **Then** it opens in a new browser tab.

4. **Given** a resource has a category (e.g., "Knowledge
   Base"),
   **When** it renders,
   **Then** the category label is color-coded according
   to the category color map.

---

### User Story 2 - Product Sorting and Filtering (Priority: P2)

When a specific product is selected, the page prioritizes
that product's resources at the top, followed by general
resources, then other products shown with muted styling.
This helps the user focus on what's relevant while still
seeing the full resource directory.

**Why this priority**: Sorting improves usability for
users who know which product they need.

**Independent Test**: Select "SIT911", confirm SIT911
resources appear under a blue-accented header, general
resources follow, then other products appear with gray
accents.

**Acceptance Scenarios**:

1. **Given** "Komlog" is selected,
   **When** the page renders,
   **Then** Komlog resources show first with a blue accent,
   general resources next, other products below with gray
   accents.

2. **Given** "All Products" is selected,
   **When** the page renders,
   **Then** general resources show first, then all products
   in order.

---

### Edge Cases

- What happens if a product has no resources defined? That
  product section is simply not shown.
- What happens if global resources list is empty? The
  global section is skipped.
- What happens if resource URLs are invalid? Links open
  in a new tab — the destination's availability is not
  validated by the system.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a "Company Resources"
  module accessible from the sidebar navigation.
- **FR-002**: System MUST display a product filter dropdown
  with "All Products" and each Komutel product.
- **FR-003**: Resources MUST be displayed as clickable cards
  with category, title, description, and external link.
- **FR-004**: Category labels MUST be color-coded per a
  defined color map.
- **FR-005**: Resource links MUST open in a new browser tab.
- **FR-006**: When a product is selected, its resources MUST
  appear first, followed by global, then other products.
- **FR-007**: Resource data MUST be configurable from a
  single location (KOMUTEL_RESOURCES in config.py).
- **FR-008**: The module MUST display a branded header with
  the Versaterm logo and a footer.

### Key Entities

- **Resource**: A company link/tool. Attributes: category,
  title, description, URL.
- **Resource Category**: A classification with associated
  color. Options: Documentation, Knowledge Base, Project
  Management, Communication, HR & Onboarding, Presentations.
- **Product Resources**: Resources grouped by Komutel
  product. Key: product name.
- **Global Resources**: Resources available to all employees.
  Key: "_global".

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of resource cards are clickable and open
  correct URLs in new tabs.
- **SC-002**: Product filtering correctly reorders resources
  for all 5 Komutel products.
- **SC-003**: Adding a new resource or product requires
  editing only config.py — 0 module file changes.
- **SC-004**: New hires can find relevant resources within
  30 seconds of opening the module.

## Assumptions

- The module is scoped to Komutel company resources only
  for this version. Expanding to other Versaterm subsidiaries
  is a future enhancement.
- Resource URLs point to real company tools (Confluence,
  Jira, SharePoint, Teams) but the system does not validate
  URL availability or authentication status.
- Resource data is hardcoded in KOMUTEL_RESOURCES config
  for the hackathon. A CMS or database-driven approach is
  out of scope.
- Each Komutel product has 3 resources: SharePoint technical
  docs, Confluence space, and Jira board.
- Global resources include: Confluence wiki, Jira dashboard,
  Teams, HR portal, SharePoint engineering docs, and
  Presentations.
- Dependencies: 003-app-shell-layout (sidebar module entry),
  013-branded-theme (visual consistency).
