import smtplib
from email.mime.text import MIMEText

from src.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM


def send_code_email(email, code):
    """Returns True if sent via SMTP, False if in dev mode (no SMTP configured)."""
    if not SMTP_HOST:
        print(f"[DEV] Access code for {email}: {code}")
        return False

    msg = MIMEText(
        f"Your Versaterm Academy access code is: {code}\n\n"
        f"This code expires in 10 minutes."
    )
    msg["Subject"] = "Versaterm Academy Access Code"
    msg["From"] = SMTP_FROM
    msg["To"] = email

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
    return True
