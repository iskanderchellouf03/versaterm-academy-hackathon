# Feature Specification: One-Click Copy & Markdown Download

**Feature Branch**: `010-copy-download-export`
**Created**: 2026-03-04
**Status**: Draft
**Input**: User description: "As a user, I want one-click copy and Markdown download so I can reuse AI outputs in Confluence, tickets, or docs immediately."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - One-Click Copy to Clipboard (Priority: P1)

An authenticated employee has just generated output from any
AI-powered module (Requirement Analyzer, KB Article
Generator, Onboarding Plan Generator). Next to the output
area, they see a "Copy" button. They click it once and the
entire output is copied to their clipboard in markdown
format. A brief visual confirmation (e.g., "Copied!" tooltip
or button state change) indicates success. The employee then
pastes the content into Confluence, a Jira ticket, an email,
or any markdown-compatible tool.

This is a **cross-module** feature — the copy action works
identically across all modules that produce AI-generated
output.

**Why this priority**: Copy-to-clipboard is the fastest path
from generation to reuse. It requires no file management and
works instantly. This is the most common export action.

**Independent Test**: Generate output in any module, click
"Copy", paste into a text editor, and confirm the clipboard
contains the full output in markdown format with correct
headings, lists, and formatting.

**Acceptance Scenarios**:

1. **Given** an AI-generated output is displayed in any
   module,
   **When** the user clicks the "Copy" button,
   **Then** the complete output is copied to the clipboard
   in markdown format.

2. **Given** the user clicks "Copy",
   **When** the copy succeeds,
   **Then** a visual confirmation is displayed (e.g.,
   "Copied!" text or button icon change) for at least 2
   seconds.

3. **Given** the user pastes the copied content into a
   markdown-compatible tool (e.g., Confluence, GitHub),
   **When** the content renders,
   **Then** headings, lists, bold text, and other markdown
   elements display correctly.

4. **Given** no output has been generated yet,
   **When** the user looks at the module,
   **Then** the "Copy" button is either hidden or disabled.

---

### User Story 2 - Download as Markdown File (Priority: P2)

Alongside the "Copy" button, a "Download" button is
available. Clicking it downloads the AI-generated output as
a `.md` file to the user's local machine. The filename is
auto-generated based on the module name and a timestamp
(e.g., `requirement-analysis-2026-03-04.md` or
`kb-article-2026-03-04.md`).

**Why this priority**: Download provides a persistent,
shareable artifact. It complements copy-to-clipboard for
cases where the user needs to attach a file (email, shared
drive, document management system). Depends on output being
generated (US1 establishes the pattern).

**Independent Test**: Generate output in any module, click
"Download", and confirm a `.md` file is saved to the
browser's default download location with the correct content
and a descriptive filename.

**Acceptance Scenarios**:

1. **Given** an AI-generated output is displayed,
   **When** the user clicks the "Download" button,
   **Then** a `.md` file is downloaded to their machine
   containing the complete output.

2. **Given** the user downloads the file,
   **When** they open it in a text editor or markdown viewer,
   **Then** the content matches the on-screen output with
   correct markdown formatting.

3. **Given** the download completes,
   **When** the user checks the filename,
   **Then** it follows the pattern
   `{module-name}-{YYYY-MM-DD}.md` (e.g.,
   `kb-article-2026-03-04.md`).

4. **Given** no output has been generated yet,
   **When** the user looks at the module,
   **Then** the "Download" button is either hidden or
   disabled.

---

### User Story 3 - Per-Section Copy (Priority: P3)

For modules that produce multi-section output (e.g.,
Requirement Analyzer with 5 sections, KB Article Generator
with 4 sections), the user can copy individual sections
rather than the entire output. Each section has its own small
"Copy" icon. This allows the user to paste only the
acceptance criteria into a Jira ticket or only the key terms
into a wiki page.

**Why this priority**: Full-output copy (US1) covers most
cases. Per-section copy is a convenience for users who need
to distribute sections across different destinations. Nice
to have but not blocking.

**Independent Test**: Generate a multi-section output (e.g.,
Requirement Analyzer), click the copy icon on just the
"Test Cases" section, paste into a text editor, and confirm
only that section's content was copied.

**Acceptance Scenarios**:

1. **Given** a multi-section output is displayed,
   **When** the user clicks the copy icon on a specific
   section,
   **Then** only that section's content (including its
   heading) is copied to the clipboard.

2. **Given** the user copies a single section,
   **When** they paste it,
   **Then** the section's markdown formatting is preserved.

---

### Edge Cases

- What happens when the clipboard API is not available (e.g.,
  older browser, non-HTTPS context)? The system displays a
  fallback message suggesting the user manually select and
  copy the text. The "Copy" button shows an error state
  rather than silently failing.
- What happens when the user clicks "Copy" or "Download"
  while a new generation is in progress? The buttons are
  disabled while generation is running. They become active
  only when the output is fully rendered.
- What happens when the output is very long? Copy and
  download handle the full output regardless of length. No
  truncation occurs.
- What happens when the user generates new output after
  copying/downloading? The previous copy/download state
  resets. The buttons apply to the current output only.
- What happens if the user edits the output (in modules that
  support inline editing) before copying/downloading? The
  copy and download actions use the current on-screen
  content, including any user edits.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Every module that produces AI-generated output
  MUST display a "Copy" button adjacent to the output area.
- **FR-002**: Clicking "Copy" MUST copy the complete output
  to the clipboard in markdown format.
- **FR-003**: After a successful copy, the system MUST
  display a visual confirmation for at least 2 seconds.
- **FR-004**: Every module that produces AI-generated output
  MUST display a "Download" button adjacent to the output
  area.
- **FR-005**: Clicking "Download" MUST trigger a browser
  download of a `.md` file containing the complete output.
- **FR-006**: Downloaded filenames MUST follow the pattern
  `{module-name}-{YYYY-MM-DD}.md`.
- **FR-007**: Both "Copy" and "Download" buttons MUST be
  disabled or hidden when no output is available.
- **FR-008**: Both buttons MUST be disabled while a
  generation is in progress.
- **FR-009**: For multi-section outputs, each section MUST
  have an individual copy icon that copies only that
  section's content.
- **FR-010**: Copy and download MUST use the current
  on-screen content, including any user edits made to the
  output.
- **FR-011**: If the clipboard API is unavailable, the
  system MUST display a user-friendly fallback message
  instead of silently failing.
- **FR-012**: The copy and download behavior MUST be
  consistent across all AI-powered modules.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can copy full output to clipboard in a
  single click across 100% of AI-powered modules.
- **SC-002**: Users can download output as a `.md` file in
  a single click across 100% of AI-powered modules.
- **SC-003**: 100% of copied/downloaded content preserves
  correct markdown formatting when pasted or opened.
- **SC-004**: Copy confirmation is visible within 500ms of
  clicking the button.
- **SC-005**: 90% of users report that the copy/download
  feature reduces the time from generation to reuse in
  external tools.

## Assumptions

- This is a cross-cutting feature that applies to all
  modules producing AI-generated output: Requirement
  Analyzer (004), KB Article Generator (006), and
  Onboarding Plan Generator (008). Future modules that
  produce AI output MUST also include these controls.
- The copy action uses the browser's Clipboard API
  (navigator.clipboard). HTTPS is assumed for production
  deployment.
- The download action uses the browser's native file
  download mechanism. No server-side file generation is
  needed.
- Markdown is the only export format. PDF, HTML, or DOCX
  export is out of scope for this version.
- This feature replaces the per-module "Copy" actions
  already specified in features 004, 006, and 008. Those
  specs described copy as part of their P2 stories; this
  feature consolidates and standardizes the behavior
  across all modules with the addition of download.
- Depends on 003-app-shell-layout (module rendering) and
  001-employee-auth (access gate). Compatible with all
  modules that produce AI output.
