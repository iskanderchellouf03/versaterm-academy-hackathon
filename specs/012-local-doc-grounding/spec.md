# Feature Specification: Local Document Grounding

**Feature Branch**: `012-local-doc-grounding`
**Created**: 2026-03-04
**Status**: Partially Deprecated
**Input**: User description: "As a user, I want to upload local PDFs/DOCX/TXT/CSV and include top-K excerpts as context with simple citations so outputs can reference real Versaterm docs without integrations."

> **Note (2026-03-05)**: The global sidebar document upload panel
> has been removed for performance. Document upload is now limited
> to module-specific contexts (e.g., CV upload in Onboarding
> Planner). The `src/components/doc_uploader.py` file has been
> deleted and `build_grounding_context()` calls have been removed
> from all AI modules. Per-module file uploads (like CV analysis)
> remain functional.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Upload Documents for Grounding (Priority: P1)

An authenticated employee navigates to a document management
area (accessible from the sidebar or within a module). They
upload one or more files in supported formats (PDF, DOCX,
TXT, CSV). The system processes each file, extracts its text
content, and makes it available as grounding context for AI
modules. The user sees a list of uploaded documents with
their names and file types.

Uploaded documents persist for the current session only (no
permanent storage). When the user starts a new session, the
document library is empty.

**Why this priority**: Without document upload, there is no
source material for grounding. This is the prerequisite for
all other stories.

**Independent Test**: Upload a PDF and a TXT file, confirm
both appear in the document list with correct names and
types, and confirm the system acknowledges successful
processing.

**Acceptance Scenarios**:

1. **Given** the user is in the document management area,
   **When** they upload a PDF file,
   **Then** the file is processed, its text content is
   extracted, and it appears in the uploaded documents list.

2. **Given** the user uploads a DOCX, TXT, or CSV file,
   **When** the upload completes,
   **Then** the file appears in the documents list with
   its name and file type.

3. **Given** the user uploads a file in an unsupported
   format (e.g., .exe, .png),
   **When** the upload is attempted,
   **Then** the system rejects the file with a clear
   message listing supported formats.

4. **Given** the user uploads multiple files,
   **When** all uploads complete,
   **Then** all files appear in the documents list and are
   available for grounding.

5. **Given** the user has uploaded documents,
   **When** they start a new session,
   **Then** the documents list is empty (no persistence
   across sessions).

---

### User Story 2 - Grounded AI Output with Citations (Priority: P2)

When documents have been uploaded, the AI modules
(Requirement Analyzer, KB Article Generator, Onboarding
Plan Generator) automatically include relevant excerpts
from the uploaded documents as context when generating
output. The AI output includes simple citations referencing
the source document and the relevant excerpt, so the user
can verify where the information came from.

Citations follow a simple format: `[Source: filename.pdf]`
or `[Source: filename.pdf, p.12]` when page information is
available.

**Why this priority**: Grounding outputs in real documents
is the core value of this feature — it transforms generic
AI output into document-backed output. This depends on US1
(documents being uploaded and processed first).

**Independent Test**: Upload a Versaterm product manual PDF,
go to the KB Article Generator, paste a requirement related
to that product, generate the article, and confirm the
output includes excerpts and citations from the uploaded
document.

**Acceptance Scenarios**:

1. **Given** documents have been uploaded and the user is in
   an AI module,
   **When** they generate output,
   **Then** the AI includes relevant excerpts from uploaded
   documents as context and the output contains citations.

2. **Given** the AI output includes a claim or detail from
   an uploaded document,
   **When** the user reads the output,
   **Then** a citation is present indicating the source
   document name (and page number if available).

3. **Given** documents have been uploaded but none are
   relevant to the current input,
   **When** the user generates output,
   **Then** the output is generated without citations
   (graceful fallback to non-grounded behavior).

4. **Given** no documents have been uploaded,
   **When** the user generates output in any module,
   **Then** the module works exactly as before (no change
   in behavior, no error).

---

### User Story 3 - Manage Uploaded Documents (Priority: P3)

The user can view the list of uploaded documents, see basic
metadata (filename, file type, size), and remove individual
documents. Removing a document excludes it from future
grounding context. The user can also upload additional
documents at any time.

**Why this priority**: Document management improves usability
but the feature works without it — documents uploaded in US1
are automatically used in US2. This adds control over which
documents are active.

**Independent Test**: Upload three documents, remove one from
the list, generate AI output, and confirm the removed
document's content is not cited while the remaining two are.

**Acceptance Scenarios**:

1. **Given** documents have been uploaded,
   **When** the user views the document list,
   **Then** each document shows its filename, file type,
   and approximate file size.

2. **Given** the user clicks "Remove" on a document,
   **When** the removal completes,
   **Then** the document disappears from the list and is
   no longer used as grounding context.

3. **Given** the user has removed a document,
   **When** they generate AI output,
   **Then** the removed document's content is not included
   in the grounding context or citations.

---

### Edge Cases

- What happens when the uploaded file is empty or contains
  no extractable text (e.g., a scanned PDF with no OCR)?
  The system adds the file to the list but displays a
  warning: "No text content could be extracted from this
  file." The file is excluded from grounding context.
- What happens when the total uploaded content is very large
  (e.g., 10 large PDFs)? The system uses the top-K most
  relevant excerpts (not the entire content of all files).
  A maximum of 5 files can be uploaded per session to keep
  processing manageable.
- What happens when the uploaded CSV has no clear text
  content (e.g., purely numeric data)? The system extracts
  whatever text is present. If the content is not useful for
  grounding, it simply will not be selected as a relevant
  excerpt.
- What happens when two documents contain conflicting
  information? The AI may cite both sources. Resolving
  conflicts is the user's responsibility — the system
  provides citations so the user can identify the conflict.
- What happens if the file exceeds the maximum size limit?
  The system rejects the upload with a message indicating
  the maximum allowed file size.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support file upload for the
  following formats: PDF, DOCX, TXT, CSV.
- **FR-002**: System MUST reject uploads of unsupported file
  formats with a clear error message listing accepted types.
- **FR-003**: System MUST enforce a maximum file size of
  10 MB per file.
- **FR-004**: System MUST enforce a maximum of 5 uploaded
  files per session.
- **FR-005**: System MUST extract text content from uploaded
  files and make it available as grounding context.
- **FR-006**: If no text can be extracted from a file, the
  system MUST display a warning and exclude the file from
  grounding context.
- **FR-007**: When documents are available and the user
  generates AI output, the system MUST include the top-K
  most relevant excerpts from uploaded documents as context
  for the AI.
- **FR-008**: AI output that references information from
  uploaded documents MUST include a citation in the format
  `[Source: filename.ext]` or `[Source: filename.ext, p.N]`
  when page information is available.
- **FR-009**: When no uploaded documents are relevant to the
  input, the system MUST generate output without citations
  (no error, no forced citation).
- **FR-010**: When no documents have been uploaded, all AI
  modules MUST behave identically to their non-grounded
  baseline (no regression).
- **FR-011**: System MUST display a list of uploaded
  documents showing filename, file type, and approximate
  size.
- **FR-012**: System MUST provide a "Remove" action for
  each uploaded document that excludes it from the documents
  list and future grounding context.
- **FR-013**: Uploaded documents MUST NOT persist beyond the
  current session. A new session starts with an empty
  document library.
- **FR-014**: The document upload area MUST be accessible
  from the sidebar or as a persistent panel visible across
  modules.

### Key Entities

- **Uploaded Document**: A file uploaded by the user for
  grounding. Attributes: filename, file type (PDF/DOCX/TXT/
  CSV), file size, extracted text content, upload timestamp,
  active status (included/removed).
- **Document Excerpt**: A segment of extracted text selected
  as relevant to a given AI generation. Attributes: source
  document reference, excerpt text, page number (if
  available), relevance ranking.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can upload a document and see it in the
  list within 10 seconds for files under 5 MB.
- **SC-002**: When relevant documents are uploaded, at least
  80% of AI-generated outputs include at least one citation
  referencing an uploaded document.
- **SC-003**: 100% of citations include the correct source
  filename.
- **SC-004**: AI modules with no uploaded documents behave
  identically to their baseline — 0% regression.
- **SC-005**: 85% of users report that grounded outputs are
  "more relevant and trustworthy" than non-grounded outputs.
- **SC-006**: Users can remove a document and confirm it is
  excluded from subsequent generations within 5 seconds.

## Assumptions

- Text extraction from PDF uses basic text layer extraction
  (not OCR). Scanned image-only PDFs will yield no text.
  OCR is out of scope.
- The "top-K" excerpt selection uses a simple relevance
  matching approach (e.g., keyword or semantic similarity).
  The specific retrieval method is an implementation detail.
  K defaults to 3-5 excerpts per generation.
- Uploaded documents are stored in memory for the current
  session only. No files are written to disk permanently or
  sent to external services.
- This feature is cross-cutting: it enhances all AI modules
  (004 Requirement Analyzer, 006 KB Article Generator, 008
  Onboarding Plan Generator) when documents are available.
- The document management area is a shared resource — the
  same uploaded documents are available across all modules
  within the session.
- File size limit of 10 MB per file and 5 files per session
  keeps processing lightweight for a demo/hackathon context.
- Dependencies: 003-app-shell-layout (sidebar/panel
  placement), 001-employee-auth (access gate). Compatible
  with all AI output modules.
- CSV files are treated as text — rows and columns are
  extracted as-is. No special tabular analysis is performed.
