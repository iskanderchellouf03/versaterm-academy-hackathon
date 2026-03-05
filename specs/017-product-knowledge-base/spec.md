# Feature Specification: Per-Product Knowledge Base

**Feature Branch**: `017-product-knowledge-base`
**Created**: 2026-03-04
**Status**: Implemented
**Input**: User description: "As HR or a team lead, I want to upload product-specific technical documents so the AI can reference real product knowledge when generating onboarding plans, improving accuracy and relevance."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Upload Product Documents (Priority: P1)

In the Onboarding Planner, after selecting a company and
product, the user sees a "Product Knowledge Base" section.
They can upload technical documents (PDF, DOCX, TXT, CSV)
specific to the selected product. Documents are processed,
chunked, and stored per product key in session state.

Each product has its own isolated document store. Uploading
documents for "Komutel / Kore" does not affect "Komutel /
Komlog".

**Why this priority**: Without product-specific documents,
the AI relies on general knowledge which may be inaccurate
for proprietary products.

**Independent Test**: Select "Komutel / Kore", upload a
Kore technical PDF. Switch to "Komutel / Komlog", confirm
the uploaded doc does not appear. Switch back to Kore,
confirm the doc is still listed.

**Acceptance Scenarios**:

1. **Given** a company and product are selected,
   **When** the user uploads a document,
   **Then** the document is processed, chunked, and stored
   under that product's key.

2. **Given** documents are uploaded for Product A,
   **When** the user switches to Product B,
   **Then** Product B's document store is independent
   (empty unless docs were uploaded for it too).

3. **Given** the user uploads multiple documents for one
   product,
   **When** they view the document list,
   **Then** all uploaded documents are listed with filenames
   and chunk counts.

4. **Given** an unsupported file type is uploaded,
   **When** the upload is attempted,
   **Then** the system rejects it with a clear error.

---

### User Story 2 - Product Context in Plan Generation (Priority: P2)

When generating an onboarding plan, the system retrieves
the top-K most relevant chunks from the selected product's
knowledge base and injects them into the AI prompt as
product context. This grounds the plan in real product
documentation.

**Why this priority**: This is the payoff of US1 — making
the uploaded documents actually improve plan quality.

**Independent Test**: Upload a Kore architecture document,
generate a plan for Kore. Confirm the plan references
specific concepts from the uploaded document that would
not appear in a generic plan.

**Acceptance Scenarios**:

1. **Given** product documents have been uploaded,
   **When** the user generates a plan,
   **Then** the top-K relevant chunks are included in
   the AI prompt.

2. **Given** no product documents are uploaded,
   **When** the user generates a plan,
   **Then** the plan is generated without product context
   (no error, standard behavior).

3. **Given** product documents are uploaded for Product A
   but the user generates a plan for Product B,
   **When** the plan is generated,
   **Then** only Product B's documents (if any) are used.

---

### Edge Cases

- What happens if the product key changes mid-session
  (user switches company/product)? Each unique
  company+product combination has its own document store.
- What happens if many large documents are uploaded?
  Only top-K chunks (default: 5) are retrieved per
  generation. The full document set is not sent to the AI.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a document upload area
  scoped to the currently selected product.
- **FR-002**: Documents MUST be chunked and stored in
  session state keyed by company+product combination.
- **FR-003**: Product document stores MUST be isolated —
  uploading for one product does not affect another.
- **FR-004**: When generating a plan, the system MUST
  retrieve the top-K most relevant chunks from the
  selected product's knowledge base.
- **FR-005**: Retrieved product context MUST be injected
  into the AI generation prompt.
- **FR-006**: If no product documents exist for the
  selected product, plan generation MUST proceed without
  product context (no error).
- **FR-007**: Supported file types: PDF, DOCX, TXT, CSV.

### Key Entities

- **Product Document Store**: A per-product collection of
  uploaded documents. Key: company+product string.
  Attributes: list of documents, each with filename and
  text chunks.
- **Product Context**: The top-K relevant chunks retrieved
  for a generation request. Attributes: chunk texts,
  source filenames.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Product document stores are correctly isolated
  in 100% of company/product switches.
- **SC-002**: Plans generated with product documents are
  rated as "more accurate" than plans without in 75% of
  user comparisons.
- **SC-003**: Chunk retrieval completes in under 2 seconds
  for stores with up to 50 chunks.

## Assumptions

- Chunking uses the same pipeline as 012-local-doc-grounding
  (text splitting with configurable chunk size).
- Retrieval uses TF-IDF similarity (retrieve_top_k) from
  the existing grounding module.
- Product documents are stored in session state only — no
  disk persistence.
- The product key format is "Company / Product" to ensure
  uniqueness across subsidiaries.
- Dependencies: 008-onboarding-plan-generator (base module),
  012-local-doc-grounding (chunking and retrieval),
  016-company-product-selection (company/product selectors).
