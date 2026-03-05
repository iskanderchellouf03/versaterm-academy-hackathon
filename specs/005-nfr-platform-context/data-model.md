# Data Model: NFR & Platform Context for Requirement Analysis

This feature extends the session state from
004-requirement-analyzer. No persistent storage.

## Session State: Analysis Context (extends 004)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| system_type | string | "Web" | Selected platform (Web, Mobile, API, Desktop) |
| selected_nfrs | list of string | [] | Selected NFRs (subset of fixed list) |

## Constants: System Types

| Value | Key Concerns (injected into prompt) |
|-------|-------------------------------------|
| Web | Browser compatibility, responsive layout, accessibility, SEO, CORS |
| Mobile | Offline handling, battery, touch interactions, device permissions, network variability |
| API | Request/response validation, authentication, rate limiting, versioning, error codes |
| Desktop | OS compatibility, installation, file system access, keyboard shortcuts, memory management |

## Constants: NFR Options

| Value | Brief Description (injected into prompt) |
|-------|------------------------------------------|
| Performance | Response times, throughput, resource usage, load handling |
| Security | Authentication, authorization, data protection, input validation |
| Accessibility | Screen readers, keyboard navigation, color contrast, ARIA |
| Scalability | Concurrent users, data volume growth, horizontal/vertical scaling |
| Reliability | Uptime, error recovery, data integrity, failover |
| Usability | Learnability, task efficiency, error prevention, user satisfaction |

## Relationships

- Extends 004's session state (adds `system_type` and
  `selected_nfrs` alongside existing `req_input_text`)
- Both values passed to the prompt builder in
  `src/ai/prompts/requirement_analyzer.py`
- No new entities, no database changes
