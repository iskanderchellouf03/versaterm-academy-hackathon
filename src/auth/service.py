import secrets
from datetime import datetime, timedelta

from src.auth.db import get_connection
import streamlit as st

from src.config import (
    ALLOWED_DOMAIN, CODE_EXPIRY_MINUTES, SESSION_TIMEOUT_HOURS,
    RATE_LIMIT_MAX, RATE_LIMIT_WINDOW_MINUTES,
)


def validate_email(email):
    email = email.strip().lower()
    if not email:
        return False, "Email is required."
    if "@" not in email:
        return False, "Invalid email format."
    domain = email.split("@", 1)[1]
    if domain != ALLOWED_DOMAIN:
        return False, f"Only @{ALLOWED_DOMAIN} email addresses are allowed."
    return True, ""


def generate_code(email):
    email = email.strip().lower()
    code = str(secrets.randbelow(1000000)).zfill(6)
    now = datetime.utcnow()
    expires_at = now + timedelta(minutes=CODE_EXPIRY_MINUTES)

    conn = get_connection()
    # Invalidate prior unused codes for this email
    conn.execute(
        "UPDATE access_codes SET used = 1 WHERE email = ? AND used = 0",
        (email,),
    )
    # Insert new code
    conn.execute(
        "INSERT INTO access_codes (email, code, created_at, expires_at, used) VALUES (?, ?, ?, ?, 0)",
        (email, code, now.isoformat(), expires_at.isoformat()),
    )
    conn.commit()
    conn.close()
    return code


def verify_code(email, code):
    email = email.strip().lower()
    code = code.strip()
    now = datetime.utcnow().isoformat()

    conn = get_connection()
    row = conn.execute(
        "SELECT id, expires_at FROM access_codes WHERE email = ? AND code = ? AND used = 0 ORDER BY created_at DESC LIMIT 1",
        (email, code),
    ).fetchone()

    if row is None:
        # Check if code exists but is expired
        expired_row = conn.execute(
            "SELECT id FROM access_codes WHERE email = ? AND code = ? AND used = 0 AND expires_at <= ?",
            (email, code, now),
        ).fetchone()
        conn.close()
        if expired_row:
            return False, "Code expired. Please request a new one."
        return False, "Invalid code. Please check and try again."

    code_id, expires_at = row
    if expires_at <= now:
        conn.close()
        return False, "Code expired. Please request a new one."

    # Mark as used
    conn.execute("UPDATE access_codes SET used = 1 WHERE id = ?", (code_id,))
    conn.commit()
    conn.close()
    return True, ""


def check_rate_limit(email):
    email = email.strip().lower()
    window_start = (datetime.utcnow() - timedelta(minutes=RATE_LIMIT_WINDOW_MINUTES)).isoformat()

    conn = get_connection()
    count = conn.execute(
        "SELECT COUNT(*) FROM access_codes WHERE email = ? AND created_at > ?",
        (email, window_start),
    ).fetchone()[0]
    conn.close()

    if count >= RATE_LIMIT_MAX:
        return False, 0
    return True, RATE_LIMIT_MAX - count


def create_session(email):
    """Create a persistent session token, return it."""
    token = secrets.token_urlsafe(32)
    now = datetime.utcnow()
    expires_at = now + timedelta(hours=SESSION_TIMEOUT_HOURS)
    conn = get_connection()
    conn.execute(
        "INSERT INTO sessions (token, email, created_at, expires_at) VALUES (?, ?, ?, ?)",
        (token, email.strip().lower(), now.isoformat(), expires_at.isoformat()),
    )
    conn.commit()
    conn.close()
    return token


def validate_session(token):
    """Check if a session token is valid. Returns email or None."""
    if not token:
        return None
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    row = conn.execute(
        "SELECT email FROM sessions WHERE token = ? AND expires_at > ?",
        (token, now),
    ).fetchone()
    conn.close()
    return row[0] if row else None


def delete_session(token):
    """Remove a session token from the DB."""
    if not token:
        return
    conn = get_connection()
    conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
    conn.commit()
    conn.close()


def check_session_timeout():
    last_activity = st.session_state.get("last_activity")
    if last_activity is None:
        return True
    delta = datetime.utcnow() - last_activity
    return delta > timedelta(hours=SESSION_TIMEOUT_HOURS)


def update_activity():
    st.session_state["last_activity"] = datetime.utcnow()


def logout():
    token = st.session_state.pop("session_token", None)
    delete_session(token)
    for key in ["authenticated", "user_email", "login_time", "last_activity"]:
        st.session_state.pop(key, None)
    st.query_params.clear()
    st.rerun()
