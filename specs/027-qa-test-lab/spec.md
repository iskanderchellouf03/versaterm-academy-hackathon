# 027 — QA Test Lab

## Purpose
Provide QA testers with an AI-powered tool that generates comprehensive test suites from software requirements, supporting both ticket-queue and standalone workflows.

## Flow
```
Requirement Analyzer → "Send to QA Lab" button → Ticket Queue (session state)
QA Test Lab → Pick ticket (or paste manually) → AI generates test suite → Chat to refine → Export
```

## Features

### Ticket Queue
- Receives tickets from Requirement Analyzer via shared `st.session_state["qa_ticket_queue"]`
- Displays ticket cards with title, system type, NFRs, timestamp, and status badge
- Status progression: Pending → In Progress → Tests Generated
- Maximum 10 tickets in queue (FIFO eviction)
- Manual input option for standalone use without tickets
- JIRA link badge (blue `#0052CC`) and quality score badge shown on ticket cards when available
- "Continue Testing" button for In Progress tickets (preserves existing state)

### Test Suite Generation
- AI generates 7 structured sections:
  1. **Test Summary** — scope, approach, assumptions
  2. **Test Scenarios** — happy path, alternate, error flows (TS-XXX format)
  3. **Detailed Test Cases** — TC-XXX format with priority, preconditions, steps, expected result, test data
  4. **Edge Cases & Boundary Tests** — EC-XXX format
  5. **Negative Test Cases** — NT-XXX format
  6. **Exploratory Testing Checklist** — checkbox items
  7. **Regression Checklist** — checkbox items
- Inherits system type and NFR context from source ticket
- Uses **refined analysis** (`result_markdown`) from Requirement Analyzer as primary AI input when available, falling back to raw requirement text
- Context card shows expandable refined analysis, JIRA link, and quality score

### Chat Refinement
- Iterative AI chat to add, modify, or expand tests
- Continues TC numbering from previous generation
- Chat responses shown **only in chat history** (not appended to main result cards)
- Combined base result + chat refinements available at export time
- Full conversation history persisted per ticket (survives ticket switching)

### Export
- Copy All (clipboard) — includes base result + chat refinements
- Download Markdown (.md) — includes base result + chat refinements

## UI Components
- Hero header with gradient background and centered logo
- Color-coded section cards matching Requirement Analyzer pattern:
  - Test Summary: teal (#00505D)
  - Test Scenarios: blue (#2E86C1)
  - Detailed Test Cases: purple (#8E44AD)
  - Edge Cases: orange (#E67E22)
  - Negative Tests: red (#C0392B)
  - Exploratory Checklist: green (#16A085)
  - Regression Checklist: dark (#2C3E50)
- Ticket cards with status badges (orange=Pending, blue=In Progress, green=Generated)
- JIRA badge uses CSS class injection (`.jira-badge`) to override global link color
- Ticket context card in generation view with expandable refined analysis
- Back-to-queue navigation
- All HTML rendered as single-line concatenated strings (avoids Streamlit code block rendering)

## Config
- `QA_INPUT_MAX_CHARS = 5000`
- `QA_MAX_QUEUE_SIZE = 10`

## Files
- `src/ai/prompts/qa_test_lab.py` — SYSTEM_PROMPT, CHAT_FOLLOWUP_PROMPT, build_context_section
- `src/modules/qa_test_lab.py` — Main module
- `src/output/schema.py` — "027" entry with 7 sections
- `src/modules/__init__.py` — Registration
- `src/modules/home.py` — Module card (in 3-2 grid layout, row 2)
- `src/modules/requirement_analyzer.py` — "Send to QA Lab" button with jira_key, jira_url, scores, result_markdown

## Dependencies
- 004 (Requirement Analyzer) — ticket source + refined analysis
- 005 (NFR/Platform Context) — inherited context
- 010 (Copy/Download Export) — export components
- 014 (Structured Output Format) — section normalization
