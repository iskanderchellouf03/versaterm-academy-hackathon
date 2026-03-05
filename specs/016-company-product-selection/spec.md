# Feature Specification: Company & Product Selection

**Feature Branch**: `016-company-product-selection`
**Created**: 2026-03-04
**Status**: Implemented
**Input**: User description: "As HR, I want to select the company (Versaterm HQ, Komutel, DroneSense) and the specific product the new hire will work on, so the onboarding plan is tailored to the right organizational context."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Company and Product Selectors (Priority: P1)

In the Onboarding Planner's plan configuration section,
the user sees two new dropdown selectors:

1. **Company** — a dropdown listing Versaterm subsidiary
   companies: Versaterm Public Safety (HQ), Komutel,
   DroneSense.
2. **Product** — a dynamic dropdown that updates based on
   the selected company, showing only products belonging
   to that company.

Company-product mappings:
- **Versaterm Public Safety (HQ)**: Versaterm Adashi C&C,
  Blue Team, CAD, CallTriage, TargAir.
- **Komutel**: Kore, Komlog, SIT911, Kontact, Komuync.
- **DroneSense**: (no specific products listed).

**Why this priority**: The company and product context is
essential for generating relevant onboarding content. The
AI needs to know which organizational unit and product the
new hire belongs to.

**Independent Test**: Select "Komutel" as company, confirm
the Product dropdown shows Kore, Komlog, SIT911, Kontact,
Komuync. Switch to "Versaterm Public Safety (HQ)", confirm
products update to Versaterm Adashi C&C, Blue Team, etc.

**Acceptance Scenarios**:

1. **Given** the user is on the Onboarding Planner,
   **When** they select a company from the dropdown,
   **Then** the Product dropdown updates to show only
   products for that company.

2. **Given** the user selects "Komutel",
   **When** they open the Product dropdown,
   **Then** they see: Kore, Komlog, SIT911, Kontact,
   Komuync.

3. **Given** the user selects a company with no products
   (e.g., DroneSense with empty list),
   **When** they view the Product dropdown,
   **Then** the dropdown is empty or shows a placeholder
   indicating no products are defined.

4. **Given** the user switches companies after selecting
   a product,
   **When** the company changes,
   **Then** the Product dropdown resets to show the new
   company's products.

---

### User Story 2 - Company & Product in Plan Generation (Priority: P2)

The selected company and product are passed to the AI
prompt as additional context when generating the onboarding
plan. The AI tailors the plan content to the specific
company culture and product domain.

**Why this priority**: Without passing these to the AI, the
selectors are just UI elements with no impact on output
quality. Depends on US1 for the selector values.

**Independent Test**: Generate two plans — one for
"Komutel / Kore" and one for "Versaterm HQ / CAD". Confirm
the plans reference different products, technologies, and
organizational contexts.

**Acceptance Scenarios**:

1. **Given** the user selects company and product,
   **When** they generate a plan,
   **Then** the AI prompt includes the company name and
   product name as context.

2. **Given** two plans for different company/product combos,
   **When** compared,
   **Then** they contain distinct content relevant to each
   product domain.

---

### Edge Cases

- What happens if a company has an empty product list?
  The Product field is disabled or shows "N/A". Plan
  generation proceeds with company context only.
- What happens if new products are added later? The
  COMPANY_PRODUCTS config in config.py is the single
  source of truth and can be updated without code changes
  in the module.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a Company dropdown with
  options: Versaterm Public Safety (HQ), Komutel,
  DroneSense.
- **FR-002**: System MUST provide a Product dropdown that
  dynamically updates based on the selected company.
- **FR-003**: Company-product mappings MUST be configurable
  from a single location (config.py).
- **FR-004**: The selected company and product MUST be
  included in the AI generation prompt.
- **FR-005**: Switching companies MUST reset the Product
  dropdown to the new company's product list.

### Key Entities

- **Company**: A Versaterm subsidiary. Attributes: name,
  list of products.
- **Product**: A software product within a company.
  Attributes: name, parent company.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Product dropdown correctly updates for 100%
  of company selections.
- **SC-002**: Plans generated for different company/product
  combinations produce visibly different content in 80%+ of
  cases.
- **SC-003**: Adding a new company or product requires
  editing only config.py — 0 module file changes.

## Assumptions

- The company and product lists are hardcoded in config.py
  for the hackathon. A database-driven approach is out of
  scope.
- DroneSense has no defined products currently but the
  structure supports adding them later.
- Dependencies: 008-onboarding-plan-generator (base module).
