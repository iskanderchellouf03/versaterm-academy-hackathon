"""Convert requirement analysis markdown to JIRA and Confluence formats."""

import re
from datetime import date


def _md_to_jira_markup(md: str) -> str:
    """Convert markdown to JIRA wiki markup."""
    lines = md.split("\n")
    out = []
    for line in lines:
        # Headings
        if line.startswith("## "):
            out.append(f"h3. {line[3:].strip()}")
        elif line.startswith("### "):
            out.append(f"h4. {line[4:].strip()}")
        else:
            # Bold: **text** → *text*
            converted = re.sub(r"\*\*(.+?)\*\*", r"*\1*", line)
            # Bullets: - item → * item
            converted = re.sub(r"^(\s*)- ", r"\1* ", converted)
            # Inline code: `code` → {{code}}
            converted = re.sub(r"`([^`]+)`", r"{{\1}}", converted)
            out.append(converted)
    return "\n".join(out)


def to_jira(markdown: str, metadata: dict | None = None) -> str:
    """Convert requirement analysis markdown to JIRA ticket format."""
    meta = metadata or {}
    header_parts = [f"h2. Requirement Analysis"]
    if meta.get("system_type"):
        header_parts.append(f"*System Type*: {meta['system_type']}")
    if meta.get("nfrs"):
        header_parts.append(f"*NFRs*: {', '.join(meta['nfrs'])}")
    header_parts.append(f"*Generated*: {meta.get('date', date.today().isoformat())}")
    header_parts.append("----")

    header = "\n".join(header_parts)
    body = _md_to_jira_markup(markdown)

    return f"{header}\n\n{body}"


def _md_to_confluence(md: str) -> str:
    """Convert markdown to Confluence wiki markup (storage format)."""
    lines = md.split("\n")
    out = []
    in_list = False

    for line in lines:
        stripped = line.strip()

        # Headings
        if stripped.startswith("## "):
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<h2>{stripped[3:].strip()}</h2>")
        elif stripped.startswith("### "):
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<h3>{stripped[4:].strip()}</h3>")
        elif re.match(r"^\s*- ", stripped):
            # Bullet item
            item = re.sub(r"^\s*- ", "", stripped)
            # Bold
            item = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", item)
            # Inline code
            item = re.sub(r"`([^`]+)`", r"<code>\1</code>", item)
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"  <li>{item}</li>")
        else:
            if in_list:
                out.append("</ul>")
                in_list = False
            if stripped:
                # Bold and code
                converted = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", stripped)
                converted = re.sub(r"`([^`]+)`", r"<code>\1</code>", converted)
                out.append(f"<p>{converted}</p>")
            else:
                out.append("")

    if in_list:
        out.append("</ul>")

    return "\n".join(out)


def to_confluence(markdown: str, metadata: dict | None = None) -> str:
    """Convert requirement analysis markdown to Confluence HTML page."""
    meta = metadata or {}

    # Metadata panel
    meta_items = []
    if meta.get("system_type"):
        meta_items.append(f"<li><strong>System Type:</strong> {meta['system_type']}</li>")
    if meta.get("nfrs"):
        meta_items.append(f"<li><strong>NFRs:</strong> {', '.join(meta['nfrs'])}</li>")
    meta_items.append(f"<li><strong>Generated:</strong> {meta.get('date', date.today().isoformat())}</li>")

    meta_panel = (
        '<div style="background:#f4f5f7;border:1px solid #dfe1e6;border-radius:3px;padding:12px;margin-bottom:16px;">\n'
        f'  <ul style="list-style:none;padding:0;margin:0;">{"".join(meta_items)}</ul>\n'
        '</div>'
    )

    body = _md_to_confluence(markdown)

    return f"<h1>Requirement Analysis</h1>\n{meta_panel}\n{body}"
