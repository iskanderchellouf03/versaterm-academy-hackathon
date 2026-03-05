"""JIRA API client — creates tickets or returns mock preview."""

import random
import string
from datetime import datetime

import requests

from src.config import JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN, JIRA_PROJECT_KEY, JIRA_MOCK_MODE
from src.export.formatters import to_jira


def _generate_mock_key():
    num = random.randint(100, 9999)
    return f"{JIRA_PROJECT_KEY}-{num}"


def create_ticket(
    summary: str,
    markdown_body: str,
    metadata: dict | None = None,
    issue_type: str = "Story",
    labels: list[str] | None = None,
) -> dict:
    """Create a JIRA ticket or return a mock preview.

    Returns dict with: success, key, url, summary, description (preview), mock
    """
    meta = metadata or {}
    jira_body = to_jira(markdown_body, meta)
    ticket_labels = labels or []
    if meta.get("system_type"):
        ticket_labels.append(f"system-{meta['system_type'].lower()}")
    for nfr in meta.get("nfrs", []):
        ticket_labels.append(f"nfr-{nfr.lower().replace(' ', '-')}")
    ticket_labels.append("ai-generated")

    # ── Mock mode ────────────────────────────────────────────
    if JIRA_MOCK_MODE or not JIRA_EMAIL or not JIRA_API_TOKEN:
        mock_key = _generate_mock_key()
        return {
            "success": True,
            "mock": True,
            "key": mock_key,
            "url": f"{JIRA_BASE_URL}/browse/{mock_key}",
            "summary": summary,
            "issue_type": issue_type,
            "project": JIRA_PROJECT_KEY,
            "labels": ticket_labels,
            "description_preview": jira_body[:500],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    # ── Real API call ────────────────────────────────────────
    url = f"{JIRA_BASE_URL}/rest/api/3/issue"
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    payload = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": jira_body}],
                    }
                ],
            },
            "issuetype": {"name": issue_type},
            "labels": ticket_labels,
        }
    }

    try:
        resp = requests.post(url, json=payload, auth=auth, headers=headers, timeout=15)
        if resp.status_code in (200, 201):
            data = resp.json()
            return {
                "success": True,
                "mock": False,
                "key": data["key"],
                "url": f"{JIRA_BASE_URL}/browse/{data['key']}",
                "summary": summary,
                "issue_type": issue_type,
                "project": JIRA_PROJECT_KEY,
                "labels": ticket_labels,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        else:
            return {
                "success": False,
                "mock": False,
                "error": f"JIRA API returned {resp.status_code}: {resp.text[:200]}",
            }
    except Exception as e:
        return {
            "success": False,
            "mock": False,
            "error": str(e),
        }
