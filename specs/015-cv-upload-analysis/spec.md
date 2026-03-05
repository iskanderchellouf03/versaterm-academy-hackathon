# Feature Specification: CV Upload & AI Analysis

**Feature Branch**: `015-cv-upload-analysis`
**Created**: 2026-03-04
**Status**: Implemented
**Input**: User description: "As HR or a team lead, I want to upload a candidate's CV/resume in the Onboarding Planner so the AI can analyze it and auto-fill experience level, extract skills, and personalize the onboarding plan."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Upload CV for AI Analysis (Priority: P1)

An HR team member or team lead navigates to the Onboarding
Planner module. Before configuring the plan, they see a
CV upload section where they can upload the new hire's
resume (PDF, DOCX, or TXT). The system extracts text from
the CV and sends it to the AI for structured analysis.

The AI returns a structured analysis including:
1. **Candidate Name** — extracted from the CV.
2. **Experience Level** — Beginner, Intermediate, or
   Advanced, inferred from work history and skills.
3. **Key Skills** — a list of relevant technical and
   professional skills found in the CV.
4. **Focus Areas** — recommended areas for the onboarding
   plan to emphasize based on gaps or strengths.
5. **Experience Summary** — a brief overview of the
   candidate's professional background.

**Why this priority**: CV analysis is the foundation for
personalized onboarding. Without it, the planner relies
solely on manual input.

**Independent Test**: Upload a sample resume PDF, confirm
the system extracts text and displays a structured analysis
with all five sections populated.

**Acceptance Scenarios**:

1. **Given** the user is on the Onboarding Planner,
   **When** they upload a PDF resume,
   **Then** the system extracts text and displays a
   structured CV analysis.

2. **Given** the CV analysis completes,
   **When** the user views the results,
   **Then** they see candidate name, experience level,
   key skills, focus areas, and experience summary.

3. **Given** the CV analysis identifies an experience level,
   **When** the user proceeds to plan configuration,
   **Then** the experience level selector is auto-set to
   the AI-inferred value.

4. **Given** the user uploads an empty or unreadable file,
   **When** text extraction fails,
   **Then** the system displays a warning and allows the
   user to proceed without CV context.

---

### User Story 2 - CV Context in Plan Generation (Priority: P2)

When a CV has been analyzed, the AI uses the extracted
information (skills, experience, focus areas) as additional
context when generating the onboarding plan. The resulting
plan is personalized to the candidate's background.

A visual badge indicates when a plan was personalized using
CV data.

**Why this priority**: This delivers the core value of
CV-informed onboarding plans. Depends on US1 providing
the analysis.

**Independent Test**: Upload a CV, generate a plan, and
confirm the output references the candidate's specific
skills and background. Compare with a plan generated
without CV upload.

**Acceptance Scenarios**:

1. **Given** a CV has been analyzed,
   **When** the user generates an onboarding plan,
   **Then** the plan content references the candidate's
   skills and tailors activities accordingly.

2. **Given** a CV-informed plan is displayed,
   **When** the user views the output,
   **Then** a "Personalized from CV" badge is visible.

3. **Given** no CV has been uploaded,
   **When** the user generates a plan,
   **Then** the module works exactly as before with no
   errors or CV-related messaging.

---

### User Story 3 - Visual CV Analysis Dashboard (Priority: P3)

The CV analysis results are displayed in a modern,
visually rich dashboard format including:
- Metric cards for experience level and years of experience.
- Skill pills/tags for key skills.
- Focus area cards with visual indicators.
- Experience timeline entries.
- Expandable raw analysis section.

**Why this priority**: Visual polish for the CV analysis
improves readability and demo appeal. The feature works
without it (raw text would suffice), but the dashboard
makes it presentation-ready.

**Independent Test**: Upload a CV and confirm the analysis
renders as styled metric cards, skill pills, and timeline
entries rather than raw text.

**Acceptance Scenarios**:

1. **Given** a CV analysis completes,
   **When** the user views the results,
   **Then** they see styled metric cards, skill tags,
   and focus area cards.

2. **Given** the AI returns skills in the analysis,
   **When** the skills section renders,
   **Then** each skill appears as a styled pill/tag.

3. **Given** the CV text cannot be parsed into structured
   sections,
   **When** the analysis displays,
   **Then** a graceful fallback shows the raw analysis text.

---

### Edge Cases

- What happens if the CV is in a language other than English?
  The AI processes it best-effort. Results may be mixed
  language. No error is thrown.
- What happens if the CV contains no identifiable skills
  or experience? The analysis returns with available
  sections populated and others noted as "Not identified."
- What happens if the uploaded file is very large? Files
  are subject to the same 10 MB limit from the document
  upload feature (012).
- What happens if the AI fails to return a structured
  analysis? The system displays a warning and allows the
  user to proceed without CV context.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a CV upload area in the
  Onboarding Planner accepting PDF, DOCX, and TXT formats.
- **FR-002**: System MUST extract text from the uploaded CV
  and send it to the AI for structured analysis.
- **FR-003**: The AI analysis MUST return: candidate name,
  experience level, key skills, focus areas, and experience
  summary.
- **FR-004**: The inferred experience level MUST auto-set
  the Level selector in the plan configuration form.
- **FR-005**: When a CV is available, the plan generation
  prompt MUST include the CV analysis as additional context.
- **FR-006**: A "Personalized from CV" badge MUST appear
  on plans generated with CV context.
- **FR-007**: The CV analysis MUST be displayed in a styled
  dashboard with metric cards, skill pills, and focus areas.
- **FR-008**: If structured parsing fails, the system MUST
  fall back to displaying the raw analysis text.
- **FR-009**: CV upload is optional. The module MUST work
  fully without any CV uploaded.

### Key Entities

- **CV Upload**: The uploaded resume file. Attributes:
  filename, file type, extracted text content.
- **CV Analysis**: AI-generated structured analysis.
  Attributes: candidate name, experience level (enum),
  key skills (list), focus areas (list), experience
  summary (text), raw analysis text.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: CV analysis completes within 15 seconds for
  files under 5 MB in 90% of cases.
- **SC-002**: The experience level auto-fill matches a
  human reviewer's assessment in 75% of cases.
- **SC-003**: Plans generated with CV context are rated as
  "more personalized" than plans without CV in 80% of
  user comparisons.
- **SC-004**: The structured dashboard renders correctly
  for 90% of CV uploads (10% may fall back to raw text).

## Assumptions

- CV text extraction uses the same pipeline as the document
  grounding feature (012-local-doc-grounding): PyPDF2 for
  PDF, python-docx for DOCX, plain read for TXT.
- The AI analysis uses a dedicated prompt that instructs
  the model to return structured sections. The exact prompt
  is an implementation detail.
- CV data is stored in session state only. No CV content
  is persisted to disk or sent to external services beyond
  the AI API.
- The structured parser uses fuzzy keyword matching on
  section headings to handle variation in AI output format.
- Dependencies: 008-onboarding-plan-generator (base module),
  012-local-doc-grounding (text extraction pipeline).
