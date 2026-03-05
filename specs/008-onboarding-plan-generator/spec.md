# Feature Specification: Onboarding Plan Generator

**Feature Branch**: `008-onboarding-plan-generator`
**Created**: 2026-03-04
**Status**: Draft
**Input**: User description: "As a new hire/HR, I want to enter role, product, and level to get a 2-week learning plan (what it is, why it matters, key terms, plan, checkpoints) to ramp faster."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate a 2-Week Learning Plan (Priority: P1)

A new hire or HR team member navigates to the Onboarding
Plan Generator module in the sidebar. They fill in three
fields:

1. **Role** — the new hire's job function (e.g., Support
   Analyst, QA Engineer, Implementation Specialist, Sales
   Engineer).
2. **Product** — the Versaterm product they need to learn
   (e.g., Records Management System, Computer Aided
   Dispatch, Mobile Responder).
3. **Level** — the new hire's experience level (Beginner,
   Intermediate, Advanced).

They click "Generate Plan" and the system produces a
structured 2-week onboarding plan with five sections:

1. **What It Is** — a concise overview of the product and
   its purpose in the public safety ecosystem.
2. **Why It Matters** — the product's value to end users
   and the organization, framed for the specific role.
3. **Key Terms** — a glossary of essential terminology the
   new hire needs to know, tailored to the product and role.
4. **Learning Plan** — a day-by-day or week-by-week schedule
   of learning activities, readings, and hands-on exercises
   spanning 2 weeks, adjusted to the selected level.
5. **Checkpoints** — milestone assessments or self-check
   questions at key intervals (end of week 1, end of week 2)
   to verify the new hire's understanding.

**Why this priority**: This is the entire core value. Without
the generation of a structured plan from the three inputs,
the module has no function.

**Independent Test**: Select "QA Engineer" as role, "Computer
Aided Dispatch" as product, "Beginner" as level, click
"Generate Plan", and confirm all five output sections are
populated with content relevant to QA testing of a dispatch
system at a beginner level.

**Acceptance Scenarios**:

1. **Given** the user is on the Onboarding Plan Generator,
   **When** they fill in role, product, and level and click
   "Generate Plan",
   **Then** the system displays a structured plan with all
   five sections (What It Is, Why It Matters, Key Terms,
   Learning Plan, Checkpoints).

2. **Given** the user selects "Beginner" level,
   **When** the plan is generated,
   **Then** the Learning Plan section starts with
   foundational concepts and progresses gradually, with
   no assumed prior knowledge of the product.

3. **Given** the user selects "Advanced" level,
   **When** the plan is generated,
   **Then** the Learning Plan section skips basics, focuses
   on advanced workflows and edge cases, and includes
   deeper technical activities.

4. **Given** the user leaves one or more fields empty,
   **When** they click "Generate Plan",
   **Then** the system displays a validation message
   indicating which fields are required.

5. **Given** two users select the same product but different
   roles (e.g., "Support Analyst" vs. "QA Engineer"),
   **When** both plans are generated,
   **Then** the Why It Matters and Learning Plan sections
   reflect role-specific perspectives (support workflows
   vs. testing workflows).

---

### User Story 2 - Copy Generated Plan (Priority: P2)

After reviewing the onboarding plan, the user wants to copy
it for sharing with the new hire, pasting into an email, or
importing into an HR onboarding tool. The system provides a
"Copy plan" action that copies the entire plan to the
clipboard in markdown format.

**Why this priority**: The plan is useful on screen, but the
real value is sharing it with the new hire or their manager.
This depends on US1 producing the plan first.

**Independent Test**: Generate a plan, click "Copy plan",
paste into a text editor, and confirm all five sections are
present with proper formatting.

**Acceptance Scenarios**:

1. **Given** a generated plan is displayed,
   **When** the user clicks "Copy plan",
   **Then** the complete plan (all five sections) is copied
   to the clipboard in markdown format.

2. **Given** the user has copied the plan,
   **When** they paste it into a markdown-compatible tool,
   **Then** headings, lists, and formatting render correctly.

---

### User Story 3 - Adjust Inputs and Regenerate (Priority: P3)

After reviewing the generated plan, the user may want to
change one or more inputs (e.g., switch from "Beginner" to
"Intermediate") and regenerate. The input fields retain their
previous values so the user can modify only what changed.
Clicking "Generate Plan" again produces a new plan replacing
the previous output.

**Why this priority**: Iterative adjustment improves plan
quality and allows HR to experiment with different
combinations, but the module is fully functional without it.

**Independent Test**: Generate a plan, change the level from
"Beginner" to "Intermediate", click "Generate Plan", and
confirm the output updates with more advanced content.

**Acceptance Scenarios**:

1. **Given** a plan has been generated,
   **When** the user changes the level and clicks "Generate
   Plan" again,
   **Then** the output updates to reflect the new level.

2. **Given** a plan has been generated,
   **When** the user looks at the input fields,
   **Then** the previously selected values are still present.

---

### Edge Cases

- What happens when the user enters a role or product name
  that the system doesn't recognize (e.g., a custom or
  misspelled role)? The system processes it best-effort
  using the AI's general knowledge and flags in the output
  that the plan is based on inferred understanding of the
  role/product. No error is thrown.
- What happens when the generated plan references specific
  Versaterm documentation or training materials that may not
  exist? The plan includes generic activity descriptions
  (e.g., "Review the product's admin guide") rather than
  linking to specific URLs or documents. A note reminds the
  user to verify resource availability.
- What happens if generation takes too long? The system
  displays a loading indicator. If generation exceeds 30
  seconds, a timeout message is shown with a retry option.
- What happens when the user selects a role that doesn't
  typically interact with the selected product? The system
  generates a plan anyway, tailoring it to the intersection.
  It may note in the output that the role-product combination
  is unusual and suggest a more typical pairing.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a Role input field that
  accepts free-text entry of the new hire's job function.
- **FR-002**: System MUST provide a Product input field that
  accepts free-text entry of the Versaterm product name.
- **FR-003**: System MUST provide a Level selector with
  exactly three options: Beginner, Intermediate, Advanced.
- **FR-004**: All three fields (Role, Product, Level) MUST
  be required. The system MUST validate that none are empty
  before processing.
- **FR-005**: System MUST provide a "Generate Plan" button
  that triggers plan generation from the entered inputs.
- **FR-006**: System MUST display the generated plan in five
  clearly labeled sections: What It Is, Why It Matters, Key
  Terms, Learning Plan, and Checkpoints.
- **FR-007**: The Learning Plan section MUST be structured as
  a day-by-day or week-by-week schedule spanning exactly 2
  weeks (10 business days).
- **FR-008**: The Learning Plan MUST be adjusted to the
  selected level — Beginner starts with fundamentals,
  Intermediate assumes basic familiarity, Advanced focuses
  on expert-level workflows.
- **FR-009**: The Checkpoints section MUST include at least
  one checkpoint per week (minimum 2 total) with self-
  assessment questions or verification activities.
- **FR-010**: The Key Terms section MUST include at least 5
  terms relevant to the selected product and role.
- **FR-011**: System MUST display a loading indicator while
  generation is in progress.
- **FR-012**: If generation exceeds 30 seconds, the system
  MUST display a timeout message and allow retry.
- **FR-013**: System MUST provide a "Copy plan" action that
  copies the complete plan to the clipboard in markdown
  format.
- **FR-014**: Input fields MUST retain their values after
  generation so the user can modify and regenerate.
- **FR-015**: Regenerating MUST replace the previous output
  with new results.

### Key Entities

- **Onboarding Inputs**: The context provided by the user.
  Attributes: role (free text), product (free text), level
  (enum: Beginner, Intermediate, Advanced).
- **Onboarding Plan**: The structured output. Attributes:
  what-it-is (text), why-it-matters (text), key-terms (list
  of term-definition pairs, minimum 5), learning-plan
  (day-by-day schedule for 10 business days), checkpoints
  (list of assessment items, minimum 2). Each plan is tied
  to a single set of inputs.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 90% of plan generations complete and display
  results within 20 seconds of clicking "Generate Plan".
- **SC-002**: 100% of generated plans contain all five
  required sections with non-empty content.
- **SC-003**: The Learning Plan section spans exactly 2
  weeks (10 business days) in 100% of generated plans.
- **SC-004**: 80% of HR users or managers rate the generated
  plan as "useful starting point that requires minor
  customization or less".
- **SC-005**: Users can copy the complete plan to clipboard
  in a single click.
- **SC-006**: Plans generated for the same product but
  different roles produce visibly different learning
  activities in at least 80% of cases.

## Assumptions

- Role and Product are free-text fields (not dropdowns with
  fixed lists) because the range of Versaterm products and
  job titles is broad and evolving. Predefined lists would
  require ongoing maintenance.
- The AI generation uses general knowledge of Versaterm
  products and public safety domains. The quality of product-
  specific content depends on the AI model's training data.
  No proprietary Versaterm training materials are ingested.
- The module is available within the app shell layout
  (003-app-shell-layout) as a sidebar module entry.
- Generation is stateless — there is no history of past
  plans. Each submission is independent. Persisting plan
  history is out of scope.
- The output format is markdown. Rich-text or PDF export is
  out of scope.
- Authentication is required (per 001-employee-auth). No
  additional role-based access control — all authenticated
  employees can use it.
- The 2-week (10 business days) plan duration is fixed for
  this version. Customizable duration is out of scope.
- The generated plan includes generic activity descriptions,
  not links to specific internal resources. Users are
  expected to supplement with actual training materials.
