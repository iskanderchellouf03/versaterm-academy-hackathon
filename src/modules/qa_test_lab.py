import os
import base64
import html
from datetime import datetime

import streamlit as st
from openai import OpenAIError

from src.ai.client import get_client
from src.ai.prompts.qa_test_lab import SYSTEM_PROMPT, CHAT_FOLLOWUP_PROMPT, build_context_section
from src.config import (
    AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT,
    QA_INPUT_MAX_CHARS, QA_MAX_QUEUE_SIZE,
    BRAND_LOGO_WHITE_PATH, BRAND_LOGO_PATH,
)
from src.components.copy_button import render_copy_button
from src.components.download_button import render_download_button
from src.output.prompt import get_format_prompt
from src.output.normalizer import ensure_sections, normalize_markdown


# ── Section metadata for result cards ────────────────────────────
SECTION_META = {
    "Test Summary": {"icon": "\U0001f4cb", "color": "#00505D"},
    "Test Scenarios": {"icon": "\U0001f3af", "color": "#2E86C1"},
    "Detailed Test Cases": {"icon": "\U0001f9ea", "color": "#8E44AD"},
    "Edge Cases & Boundary Tests": {"icon": "\u26a0\ufe0f", "color": "#E67E22"},
    "Negative Test Cases": {"icon": "\u274c", "color": "#C0392B"},
    "Exploratory Testing Checklist": {"icon": "\U0001f50e", "color": "#16A085"},
    "Regression Checklist": {"icon": "\U0001f6e1\ufe0f", "color": "#2C3E50"},
}

STATUS_COLORS = {
    "Pending": "#E67E22",
    "In Progress": "#2E86C1",
    "Tests Generated": "#27AE60",
}


# ── Helpers ──────────────────────────────────────────────────────

def _get_logo_html(white=True, width=120):
    path = BRAND_LOGO_WHITE_PATH if white else BRAND_LOGO_PATH
    if not os.path.exists(path):
        return ""
    if path.endswith(".svg"):
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
        b64 = base64.b64encode(data.encode("utf-8")).decode("utf-8")
        return f'<img src="data:image/svg+xml;base64,{b64}" width="{width}" />'
    else:
        with open(path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode("utf-8")
        return f'<img src="data:image/png;base64,{b64}" width="{width}" />'


def _section_label(title, subtitle="", accent="#00505D"):
    sub = f'<span style="font-size:0.8rem;color:#5D6D7E;margin-left:0.5rem;">{subtitle}</span>' if subtitle else ""
    st.markdown(
        f'<div style="border-left:4px solid {accent};padding:0.5rem 1rem;margin:1.25rem 0 0.75rem 0;'
        f'background:#F4F6F7;border-radius:0 8px 8px 0;">'
        f'<span style="font-size:1rem;color:#111111;font-weight:600;">{title}</span>'
        f'{sub}</div>',
        unsafe_allow_html=True,
    )


def _get_ticket_queue():
    if "qa_ticket_queue" not in st.session_state:
        st.session_state["qa_ticket_queue"] = []
    return st.session_state["qa_ticket_queue"]


def _add_to_queue(ticket):
    queue = _get_ticket_queue()
    if len(queue) >= QA_MAX_QUEUE_SIZE:
        queue.pop(0)
    ticket["status"] = "Pending"
    queue.append(ticket)
    st.session_state["qa_ticket_queue"] = queue


def _parse_sections(markdown_text):
    """Split markdown into (title, body) sections."""
    if not markdown_text:
        return []
    parts = markdown_text.split("\n## ")
    sections = []
    for i, part in enumerate(parts):
        if i == 0:
            text = part[3:] if part.startswith("## ") else part
            if not text.strip():
                continue
        else:
            text = part
        lines = text.split("\n", 1)
        title = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""
        sections.append((title, body))
    return sections


# ── Views ────────────────────────────────────────────────────────

def _render_ticket_queue():
    """Render the ticket queue with status badges."""
    queue = _get_ticket_queue()

    if not queue:
        st.markdown(
            '<div style="background:#F4F6F7;border-radius:8px;padding:2rem;text-align:center;'
            'color:#5D6D7E;font-size:0.9rem;margin:0.5rem 0;">'
            '<div style="font-size:2rem;margin-bottom:0.5rem;">\U0001f4ed</div>'
            'No tickets in the queue yet.<br/>'
            '<span style="font-size:0.8rem;">Use the Requirement Analyzer to send tickets here, '
            'or paste a requirement below.</span></div>',
            unsafe_allow_html=True,
        )
        return

    for i, ticket in enumerate(reversed(queue)):
        idx = len(queue) - 1 - i
        status = ticket.get("status", "Pending")
        s_color = STATUS_COLORS.get(status, "#5D6D7E")
        ts = ticket.get("timestamp", "")
        if isinstance(ts, datetime):
            ts = ts.strftime("%b %d, %H:%M")

        safe_title = html.escape(ticket.get('title', 'Untitled Ticket')[:80])
        safe_sys = html.escape(ticket.get('system_type', ''))
        safe_nfrs = ', '.join(html.escape(n) for n in ticket.get('nfrs', []))

        meta_parts = []
        if safe_sys:
            meta_parts.append(safe_sys)
        if safe_nfrs:
            meta_parts.append(safe_nfrs)
        if ts:
            meta_parts.append(ts)
        meta_line = " · ".join(meta_parts)

        # Inline badges for JIRA + score
        inline_badges = ""
        if ticket.get("jira_key"):
            jira_url = html.escape(ticket.get("jira_url", "#"))
            inline_badges += (
                f'<a class="jira-badge" href="{jira_url}" target="_blank" style="'
                f'display:inline-block;background:#0052CC;border-radius:12px;'
                f'padding:0.15rem 0.55rem;margin:0.2rem 0.3rem 0 0;font-size:0.68rem;'
                f'font-weight:700;text-decoration:none;">'
                f'\U0001f3ab {html.escape(ticket["jira_key"])}</a>'
            )
        t_overall = ticket.get("scores", {}).get("overall", 0)
        if t_overall > 0:
            sc = "#27AE60" if t_overall >= 75 else ("#E67E22" if t_overall >= 40 else "#C0392B")
            inline_badges += (
                f'<span style="display:inline-block;background:{sc};color:#FFF;border-radius:12px;'
                f'padding:0.15rem 0.55rem;margin:0.2rem 0.3rem 0 0;font-size:0.68rem;'
                f'font-weight:700;">Score: {t_overall}/100</span>'
            )

        card_html = (
            f'<div style="background:#FFFFFF;border:1px solid #E0E4E8;border-left:4px solid {s_color};'
            f'border-radius:8px;padding:1rem 1.25rem;margin-bottom:0.6rem;'
            f'box-shadow:0 1px 6px rgba(0,0,0,0.03);">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;">'
            f'<div style="flex:1;min-width:200px;">'
            f'<div style="font-size:0.95rem;font-weight:700;color:#111111;margin-bottom:0.25rem;">{safe_title}</div>'
            f'<div style="font-size:0.78rem;color:#5D6D7E;">{meta_line}</div>'
            f'{f"<div>{inline_badges}</div>" if inline_badges else ""}'
            f'</div>'
            f'<div><span style="display:inline-block;background:{s_color};color:#FFFFFF;'
            f'border-radius:12px;padding:0.2rem 0.7rem;font-size:0.72rem;font-weight:700;'
            f'letter-spacing:0.02em;">{status}</span></div>'
            f'</div></div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)

        if status in ("Pending", "In Progress"):
            label = "Continue Testing" if status == "In Progress" else "Start Testing"
            if st.button(label, key=f"qa_start_{idx}", type="primary"):
                ticket["status"] = "In Progress"
                st.session_state["qa_selected_ticket"] = ticket
                st.session_state["qa_view"] = "generation"
                if status == "Pending":
                    st.session_state["qa_test_result"] = None
                    st.session_state["qa_chat_history"] = []
                st.rerun()
        elif status == "Tests Generated":
            if st.button("View Results", key=f"qa_view_{idx}"):
                st.session_state["qa_selected_ticket"] = ticket
                st.session_state["qa_test_result"] = ticket.get("generated_result")
                st.session_state["qa_chat_history"] = ticket.get("chat_history", [])
                st.session_state["qa_view"] = "generation"
                st.rerun()


def _render_manual_input():
    """Standalone text area for manual requirement input."""
    _section_label("Manual Input", "Paste a requirement directly without a ticket")

    st.text_area(
        "Paste requirement to test",
        max_chars=QA_INPUT_MAX_CHARS,
        key="qa_manual_input",
        height=180,
        placeholder="e.g., Users should be able to reset their password via email verification...",
        label_visibility="collapsed",
    )

    current_text = st.session_state.get("qa_manual_input", "")
    char_count = len(current_text)
    cc_color = "#C0392B" if char_count > QA_INPUT_MAX_CHARS * 0.9 else "#5D6D7E"
    st.markdown(
        f'<p style="text-align:right;font-size:0.75rem;color:{cc_color};margin:-0.5rem 0 0.5rem 0;">'
        f'{char_count:,} / {QA_INPUT_MAX_CHARS:,} characters</p>',
        unsafe_allow_html=True,
    )

    btn_col, _ = st.columns([1, 3])
    with btn_col:
        if st.button("Generate Test Suite", key="qa_manual_generate", type="primary", use_container_width=True):
            text = current_text.strip()
            if not text:
                st.error("Please paste a requirement to generate tests for.")
                return
            # Create a synthetic ticket
            ticket = {
                "id": f"MANUAL-{datetime.now().strftime('%H%M%S')}",
                "title": text[:80] + ("..." if len(text) > 80 else ""),
                "requirement_text": text,
                "system_type": "",
                "nfrs": [],
                "sender_email": st.session_state.get("user_email", "manual"),
                "timestamp": datetime.now(),
                "status": "In Progress",
            }
            st.session_state["qa_selected_ticket"] = ticket
            st.session_state["qa_view"] = "generation"
            st.session_state["qa_test_result"] = None
            st.session_state["qa_chat_history"] = []
            st.rerun()


def _run_generation(ticket):
    """Call AI to generate test suite from ticket context."""
    client = get_client()

    context = build_context_section(
        ticket.get("system_type"),
        ticket.get("nfrs"),
    )
    format_rules = get_format_prompt("027")

    full_prompt = SYSTEM_PROMPT + context + format_rules

    # Use the refined analysis as primary input if available
    if ticket.get("result_markdown"):
        user_content = ticket["result_markdown"]
    else:
        user_content = ticket.get("requirement_text", "")

    from src.ai.client import stream_completion
    raw = stream_completion([
        {"role": "system", "content": full_prompt},
        {"role": "user", "content": user_content},
    ])
    return normalize_markdown(ensure_sections("027", raw))


def _run_chat_followup(ticket, message, existing_result, chat_history):
    """Call AI for iterative refinement of the test suite."""
    client = get_client()

    context = build_context_section(
        ticket.get("system_type"),
        ticket.get("nfrs"),
    )

    messages = [
        {"role": "system", "content": CHAT_FOLLOWUP_PROMPT + context},
        {"role": "user", "content": f"Original requirement:\n{ticket.get('requirement_text', '')[:2000]}"},
        {"role": "assistant", "content": existing_result},
    ]

    for entry in chat_history:
        messages.append({"role": "user", "content": entry["user"]})
        if entry.get("assistant"):
            messages.append({"role": "assistant", "content": entry["assistant"]})

    messages.append({"role": "user", "content": message})

    from src.ai.client import stream_completion
    return stream_completion(messages)


def _render_results(result, ticket):
    """Render the 7-section test suite as color-coded cards."""
    sections = _parse_sections(result)

    for title, body in sections:
        sec_meta = SECTION_META.get(title, {"icon": "\U0001f4cb", "color": "#00505D"})
        accent = sec_meta["color"]
        icon = sec_meta["icon"]

        section_html = (
            f'<div style="background:#FFFFFF;border:1px solid #E0E4E8;border-left:4px solid {accent};'
            f'border-radius:8px;padding:1rem 1.25rem;margin-bottom:0.75rem;'
            f'box-shadow:0 1px 6px rgba(0,0,0,0.03);">'
            f'<div style="display:flex;align-items:center;margin-bottom:0.5rem;">'
            f'<span style="font-size:1.2rem;margin-right:0.5rem;">{icon}</span>'
            f'<span style="font-size:1rem;font-weight:700;color:{accent};">{html.escape(title)}</span>'
            f'</div></div>'
        )
        st.markdown(section_html, unsafe_allow_html=True)
        st.markdown(body)
        render_copy_button(f"## {title}\n{body}", label="Copy section")


def _get_full_result():
    """Combine the base result with all chat refinements for export."""
    base = st.session_state.get("qa_test_result", "")
    chat_history = st.session_state.get("qa_chat_history", [])
    parts = [base]
    for entry in chat_history:
        if entry.get("assistant"):
            parts.append(entry["assistant"])
    return "\n\n".join(parts)


def _render_export_row(result):
    """Render the export buttons for the test suite."""
    full = _get_full_result()
    ec1, ec2 = st.columns(2)
    with ec1:
        render_copy_button(full, label="Copy All")
    with ec2:
        render_download_button(full, "qa-test-suite")


def _render_chat_refinement(ticket):
    """Render the chat interface for iterative refinement."""
    _section_label("Refine Test Suite", "Ask the AI to add, modify, or expand tests")

    chat_history = st.session_state.get("qa_chat_history", [])

    # Show chat history
    for entry in chat_history:
        st.markdown(
            f'<div style="background:#F4F6F7;border-radius:8px;padding:0.6rem 1rem;'
            f'margin-bottom:0.4rem;font-size:0.85rem;">'
            f'<strong style="color:#00505D;">You:</strong> {html.escape(entry["user"])}</div>',
            unsafe_allow_html=True,
        )
        if entry.get("assistant"):
            st.markdown(entry["assistant"])

    # Chat input
    chat_input = st.text_input(
        "Refine tests",
        key="qa_chat_input",
        placeholder="e.g., Add accessibility tests, Add more edge cases for empty inputs...",
        label_visibility="collapsed",
    )

    send_col, _ = st.columns([1, 3])
    with send_col:
        if st.button("Send", key="qa_chat_send", type="primary", use_container_width=True):
            if not chat_input.strip():
                return

            existing_result = st.session_state.get("qa_test_result", "")

            with st.status("Refining test suite...", expanded=True):
                try:
                    response = _run_chat_followup(
                        ticket, chat_input.strip(), existing_result, chat_history
                    )
                    chat_history.append({
                        "user": chat_input.strip(),
                        "assistant": response,
                    })
                    st.session_state["qa_chat_history"] = chat_history

                    # Persist chat history on ticket (don't append to main result to avoid duplication)
                    ticket = st.session_state.get("qa_selected_ticket")
                    if ticket:
                        ticket["chat_history"] = chat_history
                        queue = _get_ticket_queue()
                        for t in queue:
                            if t.get("id") == ticket.get("id"):
                                t["chat_history"] = chat_history

                    st.rerun()
                except OpenAIError as e:
                    st.error(f"Refinement failed: {e}")
                except Exception as e:
                    st.error(f"Request failed. Please try again. ({e})")


def _render_generation_view():
    """Render the generation/results view for a selected ticket."""
    ticket = st.session_state.get("qa_selected_ticket")
    if not ticket:
        st.session_state["qa_view"] = "queue"
        st.rerun()
        return

    # Back button
    if st.button("\u2190 Back to Queue", key="qa_back"):
        st.session_state["qa_view"] = "queue"
        st.rerun()

    # Ticket context card
    ts = ticket.get("timestamp", "")
    if isinstance(ts, datetime):
        ts = ts.strftime("%b %d, %H:%M")

    # Build badges
    badge_parts = []
    if ticket.get("system_type"):
        badge_parts.append(
            f'<span style="display:inline-block;background:#073350;color:#FFF;'
            f'border-radius:20px;padding:0.2rem 0.65rem;margin:0 0.3rem 0.3rem 0;'
            f'font-size:0.72rem;font-weight:600;">{html.escape(ticket["system_type"])}</span>'
        )
    for nfr in ticket.get("nfrs", []):
        badge_parts.append(
            f'<span style="display:inline-block;background:#00505D;color:#FFF;'
            f'border-radius:20px;padding:0.2rem 0.65rem;margin:0 0.3rem 0.3rem 0;'
            f'font-size:0.72rem;font-weight:600;">{html.escape(nfr)}</span>'
        )
    badges_html = "".join(badge_parts)

    safe_title = html.escape(ticket.get('title', 'Untitled')[:100])
    safe_id = html.escape(ticket.get('id', ''))

    # JIRA link
    jira_html = ""
    if ticket.get("jira_key") and ticket.get("jira_url"):
        jira_html = (
            f'<a class="jira-badge" href="{html.escape(ticket["jira_url"])}" target="_blank" style="'
            f'display:inline-block;background:#0052CC;border-radius:20px;'
            f'padding:0.2rem 0.65rem;margin:0 0.3rem 0.3rem 0;font-size:0.72rem;'
            f'font-weight:600;text-decoration:none;">'
            f'\U0001f3ab {html.escape(ticket["jira_key"])}</a>'
        )

    # Score badge
    score_html = ""
    overall = ticket.get("scores", {}).get("overall", 0)
    if overall > 0:
        s_color = "#27AE60" if overall >= 75 else ("#E67E22" if overall >= 40 else "#C0392B")
        score_html = (
            f'<span style="display:inline-block;background:{s_color};color:#FFF;'
            f'border-radius:20px;padding:0.2rem 0.65rem;margin:0 0.3rem 0.3rem 0;'
            f'font-size:0.72rem;font-weight:600;">Score: {overall}/100</span>'
        )

    badges_row = f'<div style="margin-bottom:0.5rem;">{badges_html}{jira_html}{score_html}</div>' if (badges_html or jira_html or score_html) else ''

    # Summary card (collapsed)
    ctx_html = (
        '<div style="background:#FFFFFF;border:1px solid #E0E4E8;border-radius:10px;'
        'padding:1.25rem 1.5rem;margin-bottom:1rem;'
        'box-shadow:0 2px 12px rgba(0,0,0,0.04);border-top:3px solid #00505D;">'
        '<div style="font-size:0.72rem;color:#5D6D7E;text-transform:uppercase;font-weight:600;margin-bottom:0.3rem;">Ticket Context</div>'
        f'<div style="font-size:1.05rem;font-weight:700;color:#111111;margin-bottom:0.4rem;">{safe_title}</div>'
        f'{badges_row}'
        f'<div style="font-size:0.72rem;color:#5D6D7E;margin-top:0.3rem;">{safe_id} · {ts}</div>'
        '</div>'
    )
    st.markdown(ctx_html, unsafe_allow_html=True)

    # Expandable refined analysis
    if ticket.get("result_markdown"):
        with st.expander("View Refined Analysis from Requirement Analyzer", expanded=False):
            st.markdown(ticket["result_markdown"])

    # Generate button (if no result yet)
    result = st.session_state.get("qa_test_result")

    if not result:
        gen_col, _ = st.columns([1, 3])
        with gen_col:
            if st.button("Generate Test Suite", key="qa_generate", type="primary", use_container_width=True):
                with st.status("Generating comprehensive test suite...", expanded=True):
                    try:
                        result = _run_generation(ticket)
                        st.session_state["qa_test_result"] = result

                        # Store result on the ticket for later retrieval
                        ticket["generated_result"] = result
                        ticket["chat_history"] = []

                        # Update ticket status in queue
                        queue = _get_ticket_queue()
                        for t in queue:
                            if t.get("id") == ticket.get("id"):
                                t["status"] = "Tests Generated"
                                t["generated_result"] = result
                                t["chat_history"] = []
                        ticket["status"] = "Tests Generated"
                        st.session_state["qa_selected_ticket"] = ticket
                        st.rerun()
                    except OpenAIError as e:
                        st.error(f"Generation failed: {e}")
                    except Exception as e:
                        st.error(f"Request failed. Please try again. ({e})")
        return

    # ── Results ──────────────────────────────────────────────
    _section_label("Test Suite Results", "AI-generated test cases")

    # Export row
    _render_export_row(result)

    # Section cards
    _render_results(result, ticket)

    # Chat refinement
    _render_chat_refinement(ticket)


# ── Main render ──────────────────────────────────────────────────

def render():
    # ── Hero Header ──────────────────────────────────────────
    logo_white = _get_logo_html(white=True, width=140)
    st.markdown(
        f"""<div style="
            background: linear-gradient(135deg, #111111 0%, #073350 100%);
            border-radius: 10px;
            padding: 1.75rem 2rem;
            margin-bottom: 1.25rem;
            text-align: center;
        ">
            {f'<div style="margin-bottom:0.75rem;">{logo_white}</div>' if logo_white else ''}
            <div class="hero-title" style="margin:0;font-size:1.75rem;font-weight:700;line-height:1.2;">
                QA Test Lab
            </div>
            <style>
                .hero-title, .hero-title * {{ color: #FFFFFF !important; }}
                a.jira-badge, a.jira-badge *, a.jira-badge span {{ color: #FFFFFF !important; }}
            </style>
            <p style="color:rgba(255,255,255,0.75);font-size:0.95rem;margin:0.4rem 0 0 0;line-height:1.5;">
                Generate comprehensive test suites from requirements.
                Pick a ticket from the queue or paste a requirement directly.
            </p>
        </div>""",
        unsafe_allow_html=True,
    )

    if not AZURE_OPENAI_API_KEY:
        st.warning("AI features require an API key. Set AZURE_OPENAI_API_KEY in your .env file.")
        return

    # ── View Router ──────────────────────────────────────────
    view = st.session_state.get("qa_view", "queue")

    if view == "generation":
        _render_generation_view()
    else:
        # Queue view
        _section_label("Ticket Queue", "Tickets sent from the Requirement Analyzer")
        _render_ticket_queue()
        _render_manual_input()
