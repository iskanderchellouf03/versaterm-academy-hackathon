# Versaterm Academy

AI-powered training and development platform for Versaterm / Komutel employees. Built with Streamlit and Azure OpenAI.

## Modules

| Module | Audience | Description |
|--------|----------|-------------|
| **Company Resources** | Everyone | Centralized links to Confluence, JIRA, TestLink, SharePoint, and training materials — filtered by product |
| **Smart Writer** | Everyone | Transform rough notes, emails, or ideas into polished articles with audience and tone control |
| **Onboarding Planner** | HR & Team Leads | Generate personalized 2-week onboarding plans based on role, product, experience, and CV analysis |
| **Requirement Analyzer** | PMs & QA | Analyze requirements for completeness, ambiguity, and testability — export to JIRA with one click |
| **QA Test Lab** | QA & Developers | Generate comprehensive test suites from requirements with iterative chat refinement |

## Architecture

- **Frontend**: Streamlit with custom branded theme (CSS injection)
- **AI Backend**: Azure OpenAI (GPT-4o) via the `openai` Python package
- **Auth**: Email-based OTP with SQLite session storage
- **State**: Streamlit session state (no persistent data storage)
- **Export**: JIRA ticket creation (mock + real), Markdown/Confluence formatting, clipboard copy

## Quick Start

### Prerequisites

- Python 3.11+
- An OpenAI-compatible API key (Azure OpenAI or standard OpenAI)

### Setup

```bash
# Clone the repository
git clone https://github.com/your-org/versaterm-academy-hackathon.git
cd versaterm-academy-hackathon

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API key and SMTP settings
```

### Run

```bash
streamlit run src/app.py
```

The app opens at `http://localhost:8501`.

## Configuration

All settings are in `.env` (see `.env.example`):

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | API key for Azure OpenAI or OpenAI |
| `OPENAI_BASE_URL` | No | Custom endpoint URL (for Azure OpenAI) |
| `OPENAI_MODEL` | No | Model deployment name (default: `gpt-4o`) |
| `ALLOWED_DOMAIN` | No | Email domain restriction (default: `versaterm.com`) |
| `SMTP_HOST` | No | SMTP server for sending OTP codes |
| `SMTP_PORT` | No | SMTP port (default: `587`) |
| `SMTP_USER` | No | SMTP username |
| `SMTP_PASSWORD` | No | SMTP password |
| `JIRA_BASE_URL` | No | JIRA instance URL for ticket creation |
| `JIRA_EMAIL` | No | JIRA API email |
| `JIRA_API_TOKEN` | No | JIRA API token |
| `JIRA_MOCK_MODE` | No | Set to `false` for real JIRA integration (default: `true`) |

> **Dev mode**: If SMTP is not configured, OTP codes are displayed in the UI for local development.

## Project Structure

```
src/
  app.py                    # Entry point, auth flow, sidebar navigation, module dispatch
  config.py                 # Environment config, brand settings, resource data
  assets/                   # Logo files (PNG + SVG)
  auth/                     # Email OTP authentication + SQLite sessions
  ai/
    client.py               # Azure OpenAI client (lazy singleton)
    prompts/                # System prompts per module
  modules/
    __init__.py             # Lazy-loaded module registry
    home.py                 # Dashboard with module cards
    requirement_analyzer.py # Requirement analysis + JIRA export
    qa_test_lab.py          # Test suite generation + chat refinement
    kb_article_generator.py # Article writer with audience/tone
    onboarding_planner.py   # Onboarding plans with CV analysis
    company_resources.py    # Product-specific resource links
  export/                   # JIRA/Confluence formatters
  output/                   # Output schemas + normalizers
  components/               # Reusable UI components (branding, banner, copy/download)
  theme/                    # CSS injection (branded theme, login styles)
.streamlit/config.toml      # Streamlit theme configuration
specs/                      # Feature specifications (001-027)
```

## Key Workflows

### Requirement Analyzer to QA Test Lab

1. Paste a requirement in the **Requirement Analyzer**
2. AI scores it for completeness, ambiguity, and testability
3. Optionally create a JIRA ticket
4. Click **Send to QA Lab** — ticket appears in the QA Test Lab queue
5. In **QA Test Lab**, generate a full test suite (7 sections) from the refined analysis
6. Use the chat to iteratively refine tests
7. Copy or download the final test suite

### Onboarding Planner

1. Select company, product, role, and experience level
2. Optionally upload a CV for AI-powered skill analysis
3. Generate a personalized 2-week onboarding plan with focus notes
4. Copy or download the plan

## Tech Stack

- **Python 3.11+**
- **Streamlit** — UI framework
- **openai** — Azure OpenAI / OpenAI API client
- **PyPDF2** — PDF text extraction (CV upload)
- **python-docx** — DOCX text extraction
- **python-dotenv** — Environment variable management
- **SQLite** — Authentication database (auto-created)

## License

Copyright 2026 Versaterm Inc. All rights reserved.
