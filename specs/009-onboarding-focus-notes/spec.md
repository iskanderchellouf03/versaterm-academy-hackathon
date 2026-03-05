# Feature Specification: Onboarding Focus Notes

**Feature Branch**: `009-onboarding-focus-notes`
**Created**: 2026-03-04
**Status**: Draft
**Input**: User description: "As HR/Manager, I want to add focus notes (e.g., safety-critical workflows) so the onboarding guide emphasizes what matters most."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add Focus Notes Before Plan Generation (Priority: P1)

An HR team member or manager navigates to the Onboarding
Plan Generator module. In addition to the existing role,
product, and level fields, they see an optional "Focus
notes" text area. They enter free-text guidance describing
what the onboarding plan should emphasize — for example:

- "Focus on safety-critical dispatch workflows and CAD
  data integrity checks"
- "Emphasize compliance reporting and audit trail features"
- "Prioritize mobile field operations and offline scenarios"

When the plan is generated, the Learning Plan, Key Terms,
and Checkpoints sections give extra weight to the topics
mentioned in the focus notes. Activities related to focus
areas appear earlier in the schedule, key terms include
focus-specific terminology, and checkpoints include
verification of focus-area competency.

**Why this priority**: This is the entire enhancement. Focus
notes let managers customize the plan to their team's real
priorities rather than accepting a generic plan. Without it,
all plans for the same role/product/level are identical.

**Independent Test**: Enter role "Support Analyst", product
"Computer Aided Dispatch", level "Beginner", and focus notes
"safety-critical dispatch workflows and data validation".
Generate the plan and confirm the Learning Plan frontloads
dispatch safety activities, Key Terms includes safety-
specific terminology, and Checkpoints include safety-focused
verification questions.

**Acceptance Scenarios**:

1. **Given** the user is on the Onboarding Plan Generator,
   **When** they look at the input area,
   **Then** a "Focus notes" text area is visible below or
   alongside the role, product, and level fields.

2. **Given** the user has entered focus notes about
   safety-critical workflows,
   **When** they generate the plan,
   **Then** the Learning Plan prioritizes safety-related
   activities earlier in the schedule compared to a plan
   generated without focus notes.

3. **Given** the user has entered focus notes,
   **When** the plan is generated,
   **Then** the Key Terms section includes terminology
   relevant to the focus areas.

4. **Given** the user has entered focus notes,
   **When** the plan is generated,
   **Then** the Checkpoints section includes at least one
   assessment item that verifies understanding of the
   focus area.

5. **Given** the user leaves the focus notes field empty,
   **When** they click "Generate Plan",
   **Then** the plan is generated normally without any
   focus-area emphasis (same behavior as
   008-onboarding-plan-generator baseline).

---

### User Story 2 - Multiple Focus Areas (Priority: P2)

The manager may want to specify multiple distinct focus
areas in the same notes field. The system recognizes and
addresses each mentioned topic in the generated plan. Focus
areas are not limited to one — the user can list several
priorities and the plan distributes attention across them.

**Why this priority**: Real onboarding often has multiple
priorities (e.g., "compliance AND field operations"). This
builds on US1 but the feature works with a single focus area.

**Independent Test**: Enter focus notes "1) compliance
reporting 2) mobile field operations 3) data migration".
Generate the plan and confirm all three topics appear in the
Learning Plan activities and at least two are covered in
Checkpoints.

**Acceptance Scenarios**:

1. **Given** the user has entered focus notes listing three
   distinct topics,
   **When** the plan is generated,
   **Then** the Learning Plan includes activities addressing
   each of the three topics.

2. **Given** the user has entered multiple focus areas,
   **When** the plan is generated,
   **Then** the Checkpoints section covers at least two of
   the specified focus areas.

---

### User Story 3 - Edit Focus Notes and Regenerate (Priority: P3)

After reviewing a generated plan, the manager may want to
adjust the focus notes and regenerate. The focus notes field
retains the previously entered text. Modifying the notes and
clicking "Generate Plan" produces a new plan that reflects
the updated emphasis.

**Why this priority**: Iterative refinement is natural but
the module works without it — the user can manually clear
and retype. Convenience enhancement.

**Independent Test**: Generate a plan with focus notes about
"compliance", then change the notes to "mobile operations",
regenerate, and confirm the output shifts emphasis
accordingly.

**Acceptance Scenarios**:

1. **Given** a plan has been generated with focus notes,
   **When** the user modifies the focus notes and clicks
   "Generate Plan",
   **Then** the output reflects the updated focus areas.

2. **Given** a plan has been generated,
   **When** the user looks at the focus notes field,
   **Then** the previously entered text is still present
   and editable.

---

### Edge Cases

- What happens when the focus notes are very long (e.g., a
  full paragraph of detailed instructions)? The system MUST
  accept focus notes up to 1,000 characters. Input exceeding
  this limit is truncated with a warning.
- What happens when the focus notes conflict with the
  selected role or product (e.g., focus on "iOS development"
  for a Support Analyst role)? The system processes it
  best-effort, incorporating the focus as stated. A note in
  the plan may flag the unusual combination.
- What happens when the focus notes are vague (e.g., "make
  it good")? The system treats vague notes as low-signal
  and generates a plan similar to one without focus notes.
  No error is thrown.
- What happens when focus notes mention topics not related
  to the selected product? The system includes the topics
  as best it can. The plan may note that some focus areas
  fall outside the product's typical scope.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display an optional "Focus notes"
  text area on the Onboarding Plan Generator module.
- **FR-002**: The focus notes field MUST accept free-text
  input up to 1,000 characters.
- **FR-003**: The focus notes field MUST be optional — an
  empty field does not block plan generation.
- **FR-004**: When focus notes are provided, the generated
  Learning Plan MUST prioritize activities related to the
  specified focus areas earlier in the schedule.
- **FR-005**: When focus notes are provided, the Key Terms
  section MUST include terminology relevant to the focus
  areas.
- **FR-006**: When focus notes are provided, the Checkpoints
  section MUST include at least one assessment item related
  to the focus areas.
- **FR-007**: The system MUST support multiple distinct focus
  areas within a single notes entry and address each in the
  generated plan.
- **FR-008**: When focus notes are empty, the generated plan
  MUST be identical in behavior to the baseline
  008-onboarding-plan-generator output.
- **FR-009**: The focus notes field MUST retain its value
  after plan generation so the user can modify and
  regenerate.
- **FR-010**: The focus notes control MUST be visible
  alongside the existing role, product, and level fields.

### Key Entities

- **Onboarding Context**: Extends the Onboarding Inputs
  entity from 008-onboarding-plan-generator. New attribute:
  focus notes (free text, max 1,000 characters, optional).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: When focus notes are provided, the generated
  Learning Plan includes at least one activity per specified
  focus area in 90% of cases.
- **SC-002**: When focus notes are provided, focus-related
  activities appear in the first week of the Learning Plan
  in at least 80% of cases.
- **SC-003**: Plans generated with focus notes are rated as
  "more relevant to our team's needs" by 85% of managers
  compared to plans without focus notes.
- **SC-004**: Generation with focus notes completes within
  the same 30-second timeout as baseline generation.
- **SC-005**: 100% of plans generated without focus notes
  are unaffected by this feature (no regression).

## Assumptions

- This feature extends 008-onboarding-plan-generator. It
  adds a text area to the existing module UI; it does not
  create a separate module.
- Focus notes are incorporated into the AI prompt alongside
  role, product, and level. The quality of focus-area
  emphasis depends on the AI model's ability to interpret
  free-text guidance.
- There is no predefined list of valid focus areas — the
  field is entirely free-text. The system interprets
  whatever the user writes.
- This feature depends on 008-onboarding-plan-generator
  (the base plan generation flow), 003-app-shell-layout
  (sidebar module slot), and 001-employee-auth (access gate).
- Focus notes do not change the plan's overall structure
  (still 5 sections, still 2 weeks). They influence the
  content and ordering within those sections.
