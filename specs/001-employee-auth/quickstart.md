# Quickstart: Employee Authentication

## Prerequisites

- Python 3.11+
- (Optional) SMTP credentials for email delivery

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment (optional — for real email delivery)
cp .env.example .env
# Edit .env with SMTP credentials
```

## Run

```bash
streamlit run src/app.py
```

## Demo Flow

1. Open the app in your browser (default: http://localhost:8501)
2. Enter a `@versaterm.com` email address
3. Check the terminal for the access code (if SMTP not
   configured, the code is printed to console)
4. Enter the 6-digit code
5. You are now authenticated and can access the app
6. Click "Log out" to end your session

## Environment Variables

| Variable       | Required | Description                     |
|----------------|----------|---------------------------------|
| SMTP_HOST      | No       | SMTP server hostname            |
| SMTP_PORT      | No       | SMTP server port (default: 587) |
| SMTP_USER      | No       | SMTP username/email             |
| SMTP_PASSWORD  | No       | SMTP password or app password   |
| SMTP_FROM      | No       | Sender email address            |
| ALLOWED_DOMAIN | No       | Allowed email domain (default: versaterm.com) |

When SMTP variables are not set, access codes are printed to
the terminal/console for development and demo purposes.
