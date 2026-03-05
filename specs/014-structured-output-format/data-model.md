# Data Model: Structured Output Formatting

This feature has no persistent data entities. All data
structures are in-memory configuration objects.

## Configuration Entity: ModuleSectionSchema

Defines the required output sections for each AI module.

| Field | Type | Description |
|-------|------|-------------|
| module_id | string | Module identifier (e.g., "004", "006", "008") |
| module_name | string | Human-readable name (e.g., "Requirement Analyzer") |
| sections | ordered list of string | Section headings in required order |
| empty_note | string | Default placeholder text for empty sections (e.g., "None identified.") |

### Module Definitions

**004 — Requirement Analyzer**:
- Rewritten Requirements
- Acceptance Criteria
- Test Cases
- Edge Cases
- Risks

**006 — KB Article Generator**:
- Title
- Summary
- Body
- Tags

**008 — Onboarding Plan Generator**:
- What It Is
- Why It Matters
- Key Terms
- Learning Plan
- Checkpoints

## Configuration Entity: FormattingRules

Shared tone and Markdown rules applied to all modules.

| Field | Type | Description |
|-------|------|-------------|
| heading_level | int | Top-level section heading level (2 = `##`) |
| subheading_level | int | Subsection heading level (3 = `###`) |
| list_marker | string | Unordered list marker (`-`) |
| ordered_list_format | string | Ordered list format (`1.`) |
| bold_syntax | string | Bold syntax (`**`) |
| no_preamble | bool | Suppress introductory filler |
| no_signoff | bool | Suppress closing filler |
| direct_voice | bool | Enforce active/imperative voice |
| bullet_first | bool | Prefer bullets over paragraphs for enumerables |

## Relationships

- Each AI module (004, 006, 008) references exactly one
  ModuleSectionSchema.
- All modules share the same FormattingRules instance.
- No database tables, no migrations, no persistence layer.
