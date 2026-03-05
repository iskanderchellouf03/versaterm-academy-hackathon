<!--
  Sync Impact Report
  ==================
  Sync Impact Report
  ==================
  Version change: 1.0.0 → 1.1.0
  Modified principles: none
  Modified sections:
    - Development Workflow: rewritten for solo developer,
      small atomic commits with descriptive messages
    - Governance: removed team review requirement
  Added sections: none
  Removed sections: none
  Templates requiring updates:
    - .specify/templates/plan-template.md ✅ no changes needed
    - .specify/templates/spec-template.md ✅ no changes needed
    - .specify/templates/tasks-template.md ✅ no changes needed
  Follow-up TODOs: none
-->

# Versaterm Academy Hackathon Constitution

## Core Principles

### I. User-Centric Design

All features MUST map to a concrete employee use case.
No speculative or "nice-to-have" functionality is permitted
unless it directly supports an identified employee workflow.

- Every feature MUST answer: "Which employee task does this
  help with, and how?"
- Features without a clear employee benefit MUST be rejected
  or deferred.
- User-facing outputs (answers, summaries, navigation) MUST
  be validated against real Versaterm product documentation.
- Ambiguous requirements MUST be clarified with stakeholders
  before implementation begins.

### II. Simplicity First

Start with the simplest solution that works. Avoid
premature abstraction, over-engineering, and speculative
generality.

- YAGNI: Do not build functionality until it is needed.
- Prefer inline logic over abstractions until a pattern
  repeats three or more times.
- Every dependency MUST be justified; prefer the standard
  library when feasible.
- Code MUST be readable by any team member without requiring
  deep framework knowledge.
- If a feature can be delivered in fewer lines or fewer
  files, it MUST be.

## Hackathon Constraints

- **MVP-first**: Every task MUST target the minimum viable
  demo. Gold-plating is prohibited until the core demo flow
  works end-to-end.
- **Demo-ready**: The application MUST be runnable and
  demonstrable at any point after Phase 2 (Foundational)
  is complete.
- **No gold-plating**: Cosmetic polish, edge-case hardening,
  and performance optimization are deferred until all P1
  user stories are complete and demonstrable.
- **Tech stack**: Full-stack Python (e.g., Streamlit or
  Gradio for UI). All code MUST remain in the Python
  ecosystem to minimize context-switching overhead.
- **Single-repo**: All code lives in this repository. No
  external service dependencies that cannot be mocked
  locally.

## Development Workflow

This is a solo-developer project.

- **Small atomic commits**: Each commit MUST represent one
  logical change (a single task, a bug fix, a refactor).
  Avoid bundling unrelated changes.
- **Descriptive commit messages**: Every commit message MUST
  clearly convey what changed and why, using conventional
  prefixes (e.g., `feat:`, `fix:`, `refactor:`, `docs:`).
  The message MUST be understandable weeks later without
  reading the diff.
- **No pull requests required**: Commit directly to feature
  branches and merge to `main`. Skip ceremony that adds
  no value for a solo workflow.
- All secrets and credentials MUST be stored in environment
  variables or `.env` files (never committed).

## Governance

This constitution is the authoritative guide for all
development decisions in this project. When in doubt,
refer to the principles above.

- **Amendments**: Amendments MUST be documented with a
  rationale and reflected in a version bump.
- **Versioning**: Constitution versions follow semantic
  versioning (MAJOR.MINOR.PATCH). MAJOR for principle
  removals or redefinitions, MINOR for new principles or
  sections, PATCH for clarifications and wording.
- **Compliance**: All commits SHOULD align with this
  constitution. Violations MUST be corrected before
  moving on.

**Version**: 1.1.0 | **Ratified**: 2026-03-04 | **Last Amended**: 2026-03-04
