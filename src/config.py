import os
from dotenv import load_dotenv

load_dotenv()

# SMTP settings
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", "noreply@versaterm.com")

# Domain restriction
ALLOWED_DOMAIN = os.getenv("ALLOWED_DOMAIN", "versaterm.com")

# Auth settings
CODE_EXPIRY_MINUTES = int(os.getenv("CODE_EXPIRY_MINUTES", "10"))
SESSION_TIMEOUT_HOURS = int(os.getenv("SESSION_TIMEOUT_HOURS", "8"))
RATE_LIMIT_MAX = int(os.getenv("RATE_LIMIT_MAX", "5"))
RATE_LIMIT_WINDOW_MINUTES = int(os.getenv("RATE_LIMIT_WINDOW_MINUTES", "15"))

# Database
DB_PATH = os.getenv("DB_PATH", "auth.db")

# LLM / Azure OpenAI
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
OPENAI_TIMEOUT = 30

# Requirement Analyzer
REQ_INPUT_MAX_CHARS = 5000

# QA Test Lab
QA_INPUT_MAX_CHARS = 5000
QA_MAX_QUEUE_SIZE = 10

# System Types (for 005-nfr-platform-context)
SYSTEM_TYPES = {
    "Web": "Browser compatibility, responsive layout, accessibility, SEO, CORS",
    "API": "Request/response validation, authentication, rate limiting, versioning, error codes",
    "Desktop": "OS compatibility, installation, file system access, keyboard shortcuts, memory management",
}

# Non-Functional Requirements
NFR_OPTIONS = {
    "Performance": "Response times, throughput, resource usage, load handling",
    "Security": "Authentication, authorization, data protection, input validation",
    "Accessibility": "Screen reader support, keyboard navigation, color contrast, ARIA labels",
    "Scalability": "Horizontal/vertical scaling, data growth, concurrent users, caching",
    "Reliability": "Uptime, failover, data backup, error recovery, graceful degradation",
    "Usability": "Learnability, task efficiency, error prevention, user satisfaction",
}

# KB Article Generator
KB_INPUT_MAX_CHARS = 10000

# KB Audience & Tone (007)
AUDIENCES = {
    "Internal": "Write for internal employees. Use company jargon, reference internal tools, assume product knowledge.",
    "External": "Write for external customers. Use plain language, avoid internal jargon, provide full context.",
    "Support": "Write for support agents. Use troubleshooting structure, step-by-step resolution, reference ticket workflows and escalation.",
}

TONES = {
    "Formal": "Use professional third-person voice. Passive voice acceptable. No contractions or colloquialisms.",
    "Conversational": "Use friendly second-person voice ('you'). Contractions OK. Approachable and warm.",
    "Concise": "Minimize prose. Use bullet lists, imperative voice, short sentences. Quick-reference style.",
}

# Onboarding Plan Generator (008)
EXPERIENCE_LEVELS = ["Beginner", "Intermediate", "Advanced"]

COMPANY_PRODUCTS = {
    "Komutel": [
        "Kore",
        "Komlog",
        "SIT911",
        "Kontact",
        "Komuync",
    ],
}

# Company Resources — Komutel
KOMUTEL_RESOURCES = {
    "_global": [
        {
            "category": "Knowledge Base",
            "title": "Komutel Confluence",
            "description": "Company-wide wiki, engineering standards, and internal processes.",
            "url": "https://komutel.atlassian.net/wiki",
        },
        {
            "category": "Project Management",
            "title": "Jira Dashboard",
            "description": "Track tasks, sprints, and project progress across all teams.",
            "url": "https://komutel.atlassian.net/jira",
        },
        {
            "category": "Communication",
            "title": "Microsoft Teams",
            "description": "Team channels, meetings, and instant messaging.",
            "url": "https://teams.microsoft.com",
        },
        {
            "category": "HR & Onboarding",
            "title": "HR Portal",
            "description": "Benefits, time off, policies, and onboarding checklists.",
            "url": "https://komutel.sharepoint.com/sites/HR",
        },
        {
            "category": "Documentation",
            "title": "Komutel SharePoint",
            "description": "Technical documentation, design specs, and internal processes.",
            "url": "https://komutel.sharepoint.com/sites/Engineering",
        },
        {
            "category": "Presentations",
            "title": "Komutel Presentations",
            "description": "Product overviews, training materials, and onboarding decks.",
            "url": "https://komutel.sharepoint.com/sites/Presentations",
        },
        {
            "category": "Testing",
            "title": "TestLink",
            "description": "Test plans, test cases, and execution tracking across all products.",
            "url": "https://testlink.komutel.com",
        },
    ],
    "Kore": [
        {
            "category": "Documentation",
            "title": "Kore Technical Docs",
            "description": "Core telephony platform documentation and API references.",
            "url": "https://komutel.sharepoint.com/sites/Kore",
        },
        {
            "category": "Knowledge Base",
            "title": "Kore Confluence Space",
            "description": "Architecture decisions, runbooks, and troubleshooting guides for Kore.",
            "url": "https://komutel.atlassian.net/wiki/spaces/KORE",
        },
        {
            "category": "Project Management",
            "title": "Kore Jira Board",
            "description": "Sprint board, backlog, and issue tracking for the Kore team.",
            "url": "https://komutel.atlassian.net/jira/software/projects/KORE/board",
        },
        {
            "category": "Testing",
            "title": "Kore TestLink",
            "description": "Test plans and test case execution for the Kore telephony platform.",
            "url": "https://testlink.komutel.com/index.php?testproject=Kore",
        },
    ],
    "Komlog": [
        {
            "category": "Documentation",
            "title": "Komlog Technical Docs",
            "description": "Logging and call recording system documentation.",
            "url": "https://komutel.sharepoint.com/sites/Komlog",
        },
        {
            "category": "Knowledge Base",
            "title": "Komlog Confluence Space",
            "description": "System architecture, deployment guides, and FAQs for Komlog.",
            "url": "https://komutel.atlassian.net/wiki/spaces/KOMLOG",
        },
        {
            "category": "Project Management",
            "title": "Komlog Jira Board",
            "description": "Sprint board and issue tracking for the Komlog team.",
            "url": "https://komutel.atlassian.net/jira/software/projects/KOMLOG/board",
        },
        {
            "category": "Testing",
            "title": "Komlog TestLink",
            "description": "Test plans and regression suites for logging and call recording.",
            "url": "https://testlink.komutel.com/index.php?testproject=Komlog",
        },
    ],
    "SIT911": [
        {
            "category": "Documentation",
            "title": "SIT911 Technical Docs",
            "description": "911 call processing system documentation and workflows.",
            "url": "https://komutel.sharepoint.com/sites/SIT911",
        },
        {
            "category": "Knowledge Base",
            "title": "SIT911 Confluence Space",
            "description": "Call flow diagrams, integration specs, and operational procedures.",
            "url": "https://komutel.atlassian.net/wiki/spaces/SIT911",
        },
        {
            "category": "Project Management",
            "title": "SIT911 Jira Board",
            "description": "Sprint board and issue tracking for the SIT911 team.",
            "url": "https://komutel.atlassian.net/jira/software/projects/SIT911/board",
        },
        {
            "category": "Testing",
            "title": "SIT911 TestLink",
            "description": "Test scenarios and execution tracking for 911 call processing.",
            "url": "https://testlink.komutel.com/index.php?testproject=SIT911",
        },
    ],
    "Kontact": [
        {
            "category": "Documentation",
            "title": "Kontact Technical Docs",
            "description": "Contact center platform documentation and configuration guides.",
            "url": "https://komutel.sharepoint.com/sites/Kontact",
        },
        {
            "category": "Knowledge Base",
            "title": "Kontact Confluence Space",
            "description": "Agent routing logic, IVR configuration, and reporting guides.",
            "url": "https://komutel.atlassian.net/wiki/spaces/KONTACT",
        },
        {
            "category": "Project Management",
            "title": "Kontact Jira Board",
            "description": "Sprint board and issue tracking for the Kontact team.",
            "url": "https://komutel.atlassian.net/jira/software/projects/KONTACT/board",
        },
        {
            "category": "Testing",
            "title": "Kontact TestLink",
            "description": "Test plans for contact center routing, IVR, and agent workflows.",
            "url": "https://testlink.komutel.com/index.php?testproject=Kontact",
        },
    ],
    "Komuync": [
        {
            "category": "Documentation",
            "title": "Komuync Technical Docs",
            "description": "Unified communications platform documentation.",
            "url": "https://komutel.sharepoint.com/sites/Komuync",
        },
        {
            "category": "Knowledge Base",
            "title": "Komuync Confluence Space",
            "description": "UC architecture, SIP integration guides, and deployment docs.",
            "url": "https://komutel.atlassian.net/wiki/spaces/KOMUYNC",
        },
        {
            "category": "Project Management",
            "title": "Komuync Jira Board",
            "description": "Sprint board and issue tracking for the Komuync team.",
            "url": "https://komutel.atlassian.net/jira/software/projects/KOMUYNC/board",
        },
        {
            "category": "Testing",
            "title": "Komuync TestLink",
            "description": "Test plans for unified communications, SIP, and integration tests.",
            "url": "https://testlink.komutel.com/index.php?testproject=Komuync",
        },
    ],
}

# JIRA Integration
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "https://komutel.atlassian.net")
JIRA_EMAIL = os.getenv("JIRA_EMAIL", "")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "KORE")
JIRA_MOCK_MODE = os.getenv("JIRA_MOCK_MODE", "true").lower() == "true"

# Demo Banner (011)
DEMO_BANNER_TEXT = "Demo — This is a prototype. No data is persisted. All information is local to your current session."

# Branded Theme (013)
# Local Document Grounding (012)
MAX_FILE_SIZE_MB = 10
MAX_FILES = 5
CHUNK_SIZE = 500
TOP_K = 3
ACCEPTED_TYPES = ["pdf", "docx", "txt", "csv"]
ACCEPTED_MIMES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "text/csv",
]

BRAND_LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
BRAND_LOGO_WHITE_PATH = os.path.join(os.path.dirname(__file__), "assets", "logo-white.svg")
BRAND_TITLE = "Versaterm Academy"
BRAND_SUBTITLE = "AI-Powered Training & Development"
BRAND_PRIMARY_COLOR = "#00505D"
BRAND_PRIMARY_HOVER = "#073350"
BRAND_SIDEBAR_BG = "#111111"
BRAND_SIDEBAR_TEXT = "#ECF0F1"
BRAND_BG_COLOR = "#FFFFFF"
BRAND_SECONDARY_BG = "#F4F6F7"
BRAND_TEXT_COLOR = "#111111"
