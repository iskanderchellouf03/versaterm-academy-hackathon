# Feature Specification: KB Audience & Tone Selection

**Feature Branch**: `007-kb-audience-tone`
**Created**: 2026-03-04
**Status**: Draft
**Input**: User description: "As a KMS user, I want to choose audience (Internal/External/Support) and tone so the KB output matches the readers' expectations."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Select Target Audience Before Generation (Priority: P1)

A KMS user navigates to the KB Article Generator module and,
before submitting raw text, selects the target audience from
a predefined list: Internal, External, or Support. When the
article is generated, the language, detail level, and
assumptions in the output reflect the chosen audience:

- **Internal**: Uses company jargon freely, references
  internal tools and processes, assumes familiarity with
  the product architecture.
- **External**: Uses plain language, avoids internal jargon,
  explains concepts from a customer perspective, includes
  context that an outsider would need.
- **Support**: Uses a troubleshooting-oriented structure,
  includes step-by-step resolution procedures, references
  ticket workflows and escalation paths.

**Why this priority**: Audience determines the fundamental
voice and content of the article. An internal KB article
written in external-customer language (or vice versa) is
unusable. This is the most impactful context selection.

**Independent Test**: Paste the same raw notes, generate
once with "Internal" selected and once with "External".
Compare the two outputs and confirm the Internal version
uses technical/internal language while the External version
uses plain, customer-friendly language.

**Acceptance Scenarios**:

1. **Given** the user is on the KB Article Generator module,
   **When** they look at the input area,
   **Then** an audience selector is visible with options:
   Internal, External, and Support.

2. **Given** the user has selected "External" as the audience,
   **When** they submit raw text and receive a generated
   article,
   **Then** the article uses plain language, avoids internal
   jargon, and provides context a customer would need.

3. **Given** the user has selected "Support" as the audience,
   **When** they submit raw text and receive a generated
   article,
   **Then** the article includes troubleshooting steps,
   resolution procedures, and support-specific structure.

4. **Given** the user has not explicitly selected an audience,
   **When** they click "Generate",
   **Then** the system defaults to "Internal" and proceeds.

---

### User Story 2 - Select Tone Before Generation (Priority: P2)

Alongside the audience selector, the user can choose a tone
for the generated article from a predefined list: Formal,
Conversational, or Concise. The tone affects the writing
style of the output without changing the content structure:

- **Formal**: Professional, third-person, passive voice
  acceptable, suitable for official documentation.
- **Conversational**: Friendly, second-person ("you"),
  approachable, suitable for onboarding guides and FAQs.
- **Concise**: Minimal prose, bullet-heavy, imperative voice,
  suitable for quick-reference guides and cheat sheets.

**Why this priority**: Tone adds a layer of refinement to
the audience selection. The module is functional with just
audience context (US1), but tone control produces articles
that better match the publication channel (e.g., a formal
policy doc vs. a friendly FAQ).

**Independent Test**: Paste the same raw notes with
"External" audience, generate once with "Formal" tone and
once with "Conversational" tone. Confirm the Formal output
uses third-person and professional language while the
Conversational output uses "you" and a friendlier style.

**Acceptance Scenarios**:

1. **Given** the user is on the KB Article Generator module,
   **When** they look at the input area,
   **Then** a tone selector is visible with options: Formal,
   Conversational, and Concise.

2. **Given** the user has selected "Concise" as the tone,
   **When** they submit raw text and receive a generated
   article,
   **Then** the article body uses bullet lists, minimal
   prose, and imperative voice.

3. **Given** the user has not explicitly selected a tone,
   **When** they click "Generate",
   **Then** the system defaults to "Formal" and proceeds.

---

### User Story 3 - Combined Audience + Tone Context (Priority: P3)

The audience and tone selections work together. For example,
"External" + "Conversational" produces a customer-facing FAQ
style, while "Support" + "Concise" produces a compact
troubleshooting reference card. The combination is reflected
in both the language and the structure of the output.

**Why this priority**: Each dimension delivers value
independently, but the intersection produces the most
targeted output. This is a refinement on US1 + US2.

**Independent Test**: Select "Support" + "Concise", paste
troubleshooting notes, and confirm the output is a compact,
bullet-heavy troubleshooting guide with support-specific
references. Then switch to "External" + "Conversational"
with the same input and confirm a friendlier, customer-
facing FAQ style.

**Acceptance Scenarios**:

1. **Given** the user has selected "External" audience and
   "Conversational" tone,
   **When** they submit raw text and receive a generated
   article,
   **Then** the output uses plain customer-friendly language
   in a friendly second-person style.

2. **Given** the user has selected "Support" audience and
   "Concise" tone,
   **When** they submit raw text and receive a generated
   article,
   **Then** the output is a compact troubleshooting
   reference with bullet lists and support-specific
   terminology.

---

### Edge Cases

- What happens when the user changes the audience or tone
  after an article has been generated? The previous output
  remains visible. The new selections take effect on the
  next "Generate" click. No automatic re-generation occurs.
- What happens when the raw input already has a strong tone
  (e.g., very informal notes) and the user selects "Formal"?
  The system overrides the input tone — the generated output
  MUST match the selected tone, not the input's tone.
- What happens when the audience/tone combination seems
  unusual (e.g., "Internal" + "Conversational")? The system
  processes it without warning. All combinations are valid
  and supported.
- What happens if audience/tone selections increase
  generation time? The same 30-second timeout from
  006-kb-article-generator applies. Context is included in
  the same generation request, not as separate calls.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display an audience selector with
  exactly three options: Internal, External, Support.
- **FR-002**: The audience selector MUST default to
  "Internal" when no selection has been made.
- **FR-003**: The selected audience MUST influence the
  generated article's language, assumptions, detail level,
  and terminology.
- **FR-004**: System MUST display a tone selector with
  exactly three options: Formal, Conversational, Concise.
- **FR-005**: The tone selector MUST default to "Formal"
  when no selection has been made.
- **FR-006**: The selected tone MUST influence the generated
  article's writing style, voice, and prose density.
- **FR-007**: When both audience and tone are selected, the
  generated output MUST reflect the intersection of both
  (e.g., External + Concise = customer-facing quick
  reference).
- **FR-008**: The audience and tone controls MUST be visible
  alongside the text input, above or beside the "Generate"
  button.
- **FR-009**: Selections MUST persist across re-generations
  within the same session.
- **FR-010**: The generated output MUST match the selected
  tone regardless of the input text's original tone or
  style.

### Key Entities

- **Generation Context**: Extends the Raw Input entity from
  006-kb-article-generator. Attributes: selected audience
  (enum: Internal, External, Support), selected tone (enum:
  Formal, Conversational, Concise).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: When different audiences are selected for the
  same input, the generated articles MUST differ in
  terminology and assumed reader knowledge in at least 80%
  of cases.
- **SC-002**: When different tones are selected for the same
  input, the generated articles MUST differ in writing style
  (voice, prose density, formatting) in at least 80% of
  cases.
- **SC-003**: Generation with audience + tone context
  completes within the same 30-second timeout as baseline
  generation.
- **SC-004**: 85% of users rate the audience-tailored output
  as "appropriate for the selected reader" without requiring
  significant manual rewriting.
- **SC-005**: Users can configure audience and tone in under
  5 seconds (selections before clicking "Generate").

## Assumptions

- This feature extends 006-kb-article-generator. It adds
  controls to the existing module UI; it does not create a
  separate module.
- The audience list (Internal, External, Support) and tone
  list (Formal, Conversational, Concise) are fixed. Custom
  audiences or tones are out of scope for this version.
- Audience and tone context is incorporated into the AI
  prompt. The quality of audience/tone adaptation depends on
  the AI model's capabilities — no separate audience-specific
  templates or style guides are required.
- This feature depends on 006-kb-article-generator (the base
  article generation flow), 003-app-shell-layout (sidebar
  module slot), and 001-employee-auth (access gate).
- All nine audience-tone combinations (3 x 3) are valid.
  There are no restricted or unsupported pairings.
