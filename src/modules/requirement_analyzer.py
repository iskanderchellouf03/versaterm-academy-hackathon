import os
import re
import base64
from datetime import datetime

import streamlit as st
from openai import OpenAIError

from src.ai.client import get_client
from src.ai.prompts.requirement_analyzer import SYSTEM_PROMPT, build_context_section
from src.config import (
    AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT, REQ_INPUT_MAX_CHARS,
    SYSTEM_TYPES, NFR_OPTIONS, BRAND_LOGO_WHITE_PATH, BRAND_LOGO_PATH,
    ACCEPTED_TYPES, MAX_FILE_SIZE_MB,
)
from src.components.copy_button import render_copy_button
from src.components.download_button import render_download_button
from src.output.prompt import get_format_prompt
from src.output.normalizer import ensure_sections, normalize_markdown
from src.docs.extractor import extract_text
from src.docs.retriever import retrieve_top_k
from src.export.formatters import to_jira, to_confluence
from src.export.jira_client import create_ticket


# ── Section metadata for result cards ────────────────────────────
SECTION_META = {
    "Rewritten Requirements": {"icon": "\u2728", "color": "#00505D"},
    "Acceptance Criteria": {"icon": "\u2705", "color": "#2E86C1"},
    "Test Cases": {"icon": "\U0001f9ea", "color": "#8E44AD"},
    "Edge Cases": {"icon": "\u26a0\ufe0f", "color": "#E67E22"},
    "Risks": {"icon": "\U0001f6a8", "color": "#C0392B"},
}

SYSTEM_ICONS = {"Web": "\U0001f310", "API": "\U0001f517", "Desktop": "\U0001f5a5\ufe0f"}

NFR_ICONS = {
    "Performance": "\u26a1", "Security": "\U0001f512", "Accessibility": "\u267f",
    "Scalability": "\U0001f4c8", "Reliability": "\U0001f6e1\ufe0f", "Usability": "\U0001f91d",
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


def _parse_scores(sections):
    """Extract quality scores from the 'Requirement Quality Score' section."""
    scores = {"overall": 0, "clarity": 0, "completeness": 0, "testability": 0, "summary": ""}
    for title, body in sections:
        if "quality score" in title.lower():
            for line in body.split("\n"):
                m = re.search(r"\*\*Overall\*\*[:\s]*(\d+)\s*/\s*100", line, re.IGNORECASE)
                if m:
                    scores["overall"] = int(m.group(1))
                m = re.search(r"\*\*Clarity\*\*[:\s]*(\d+)\s*/\s*100", line, re.IGNORECASE)
                if m:
                    scores["clarity"] = int(m.group(1))
                m = re.search(r"\*\*Completeness\*\*[:\s]*(\d+)\s*/\s*100", line, re.IGNORECASE)
                if m:
                    scores["completeness"] = int(m.group(1))
                m = re.search(r"\*\*Testability\*\*[:\s]*(\d+)\s*/\s*100", line, re.IGNORECASE)
                if m:
                    scores["testability"] = int(m.group(1))
            # Summary: last non-bullet, non-empty line
            for line in reversed(body.split("\n")):
                line = line.strip()
                if line and not line.startswith("-") and not re.match(r"\*\*\w+\*\*", line):
                    scores["summary"] = line
                    break
            break
    return scores


def _score_color(score):
    if score >= 75:
        return "#27AE60"
    if score >= 40:
        return "#E67E22"
    return "#C0392B"


def _score_label(score):
    if score >= 75:
        return "Excellent"
    if score >= 40:
        return "Good"
    return "Needs Work"


def _render_score_dashboard(scores):
    """Render the quality score as a visual dashboard."""
    overall = scores["overall"]
    color = _score_color(overall)
    label = _score_label(overall)

    # Overall score circle + sub-scores
    st.markdown(
        f"""<div style="
            background:#FFFFFF;border:1px solid #E0E4E8;border-radius:10px;
            padding:1.25rem 1.5rem;margin-bottom:1rem;
            box-shadow:0 2px 12px rgba(0,0,0,0.04);
        ">
            <div style="display:flex;align-items:center;gap:2rem;flex-wrap:wrap;">
                <div style="text-align:center;min-width:100px;">
                    <div style="
                        width:90px;height:90px;border-radius:50%;
                        border:5px solid {color};
                        display:flex;align-items:center;justify-content:center;
                        margin:0 auto 0.4rem auto;
                    ">
                        <span style="font-size:1.6rem;font-weight:800;color:{color};">{overall}</span>
                    </div>
                    <div style="font-size:0.75rem;font-weight:700;color:{color};text-transform:uppercase;letter-spacing:0.05em;">
                        {label}
                    </div>
                </div>
                <div style="flex:1;min-width:200px;">
                    {_score_bar("Clarity", scores["clarity"])}
                    {_score_bar("Completeness", scores["completeness"])}
                    {_score_bar("Testability", scores["testability"])}
                </div>
            </div>
            {f'<p style="font-size:0.82rem;color:#5D6D7E;margin:0.75rem 0 0 0;border-top:1px solid #E0E4E8;padding-top:0.75rem;">{scores["summary"]}</p>' if scores["summary"] else ''}
        </div>""",
        unsafe_allow_html=True,
    )


def _score_bar(label, score):
    color = _score_color(score)
    return (
        f'<div style="margin-bottom:0.5rem;">'
        f'  <div style="display:flex;justify-content:space-between;font-size:0.78rem;margin-bottom:0.2rem;">'
        f'    <span style="color:#111111;font-weight:600;">{label}</span>'
        f'    <span style="color:{color};font-weight:700;">{score}/100</span>'
        f'  </div>'
        f'  <div style="background:#E0E4E8;border-radius:4px;height:8px;overflow:hidden;">'
        f'    <div style="background:{color};width:{score}%;height:100%;border-radius:4px;'
        f'         transition:width 0.5s ease;"></div>'
        f'  </div>'
        f'</div>'
    )


# ── Product Context (Enhancement 4) ─────────────────────────────

def _get_product_docs():
    return st.session_state.get("req_product_docs", [])


def _add_product_doc(filename, file_type, size, chunks):
    docs = _get_product_docs()
    if any(d["filename"] == filename for d in docs):
        return
    docs.append({"filename": filename, "size": size, "chunks": [{"text": c} for c in chunks], "active": True})
    st.session_state["req_product_docs"] = docs


def _remove_product_doc(filename):
    docs = _get_product_docs()
    st.session_state["req_product_docs"] = [d for d in docs if d["filename"] != filename]


def _build_product_context(query):
    docs = _get_product_docs()
    if not docs:
        return "", []
    results = retrieve_top_k(query, docs, k=5)
    if not results:
        return "", []
    sources = list({r["source"] for r in results})
    context_block = "\n\n---\nProduct Documentation Context:\n"
    for r in results:
        context_block += f"\n[From: {r['source']}]\n{r['text']}\n"
    return context_block, sources


# ── Compare Versions (Enhancement 3) ────────────────────────────

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
                Requirement Analyzer
            </div>
            <style>.hero-title, .hero-title * {{ color: #FFFFFF !important; }}</style>
            <p style="color:rgba(255,255,255,0.75);font-size:0.95rem;margin:0.4rem 0 0 0;line-height:1.5;">
                Analyze software requirements for completeness, ambiguity, and testability.
                Get acceptance criteria, test cases, edge cases, and risks.
            </p>
        </div>""",
        unsafe_allow_html=True,
    )

    if not AZURE_OPENAI_API_KEY:
        st.warning("AI features require an API key. Set AZURE_OPENAI_API_KEY in your .env file.")
        return

    # ── Step 1: Context Configuration ────────────────────────
    _section_label("Step 1 \u2014 Context", "Select system type and non-functional requirements")

    # System type pills
    st.markdown(
        '<p style="font-size:0.82rem;font-weight:600;color:#111111;margin:0 0 0.4rem 0;">System Type</p>',
        unsafe_allow_html=True,
    )
    sys_types = list(SYSTEM_TYPES.keys())
    sys_cols = st.columns(len(sys_types))
    current_sys = st.session_state.get("system_type", sys_types[0])

    for col, st_name in zip(sys_cols, sys_types):
        with col:
            icon = SYSTEM_ICONS.get(st_name, "")
            is_active = current_sys == st_name
            if st.button(
                f"{icon} {st_name}",
                key=f"sys_{st_name}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state["system_type"] = st_name
                st.rerun()

    if current_sys in SYSTEM_TYPES:
        st.markdown(
            f'<div style="background:#F4F6F7;border-radius:6px;padding:0.6rem 1rem;margin:0.5rem 0 1rem 0;'
            f'font-size:0.82rem;color:#5D6D7E;border-left:3px solid #00505D;">'
            f'<strong>{current_sys}</strong>: {SYSTEM_TYPES[current_sys]}</div>',
            unsafe_allow_html=True,
        )

    # NFR toggles
    st.markdown(
        '<p style="font-size:0.82rem;font-weight:600;color:#111111;margin:0.5rem 0 0.4rem 0;">Non-Functional Requirements</p>',
        unsafe_allow_html=True,
    )
    nfr_keys = list(NFR_OPTIONS.keys())
    selected_nfrs = st.session_state.get("selected_nfrs", [])
    nfr_cols = st.columns(3)

    for i, nfr in enumerate(nfr_keys):
        with nfr_cols[i % 3]:
            icon = NFR_ICONS.get(nfr, "")
            is_selected = nfr in selected_nfrs
            if st.button(
                f"{icon} {nfr}",
                key=f"nfr_{nfr}",
                use_container_width=True,
                type="primary" if is_selected else "secondary",
            ):
                if is_selected:
                    selected_nfrs.remove(nfr)
                else:
                    selected_nfrs.append(nfr)
                st.session_state["selected_nfrs"] = selected_nfrs
                st.rerun()

    if selected_nfrs:
        nfr_html = ""
        for nfr in selected_nfrs:
            if nfr in NFR_OPTIONS:
                nfr_html += (
                    f'<div style="display:inline-block;background:#00505D;color:#FFFFFF;'
                    f'border-radius:20px;padding:0.25rem 0.75rem;margin:0.2rem 0.3rem 0.2rem 0;'
                    f'font-size:0.75rem;font-weight:600;">{NFR_ICONS.get(nfr, "")} {nfr}</div>'
                )
        st.markdown(
            f'<div style="margin:0.5rem 0 0.75rem 0;">{nfr_html}</div>',
            unsafe_allow_html=True,
        )

    # ── Product Documentation (Enhancement 4) ────────────────
    _section_label("Product Documentation", "Optional \u2014 upload product docs for context-aware analysis")

    product_docs = _get_product_docs()
    uploaded = st.file_uploader(
        "Upload product documents",
        type=ACCEPTED_TYPES,
        accept_multiple_files=True,
        key="req_doc_upload",
        label_visibility="collapsed",
    )
    if uploaded:
        for f in uploaded:
            existing = [d["filename"] for d in product_docs]
            if f.name in existing:
                continue
            if f.size > MAX_FILE_SIZE_MB * 1024 * 1024:
                st.error(f"{f.name} exceeds {MAX_FILE_SIZE_MB} MB limit.")
                continue
            file_type = f.name.rsplit(".", 1)[-1].lower()
            chunks = extract_text(f.getvalue(), file_type)
            if not chunks:
                st.warning(f"Could not extract text from {f.name}.")
                continue
            _add_product_doc(f.name, file_type, f.size, chunks)
            st.success(f"Loaded {f.name} ({len(chunks)} chunks)")

    product_docs = _get_product_docs()
    if product_docs:
        total_chunks = sum(len(d["chunks"]) for d in product_docs)
        st.markdown(
            f'<div style="background:#EAFAF1;border-left:3px solid #27AE60;border-radius:0 6px 6px 0;'
            f'padding:0.5rem 0.75rem;font-size:0.8rem;color:#1E8449;margin:0.5rem 0;">'
            f'{len(product_docs)} doc(s) loaded ({total_chunks} chunks) \u2014 will be used as AI context</div>',
            unsafe_allow_html=True,
        )
        for doc in product_docs:
            dc1, dc2 = st.columns([0.8, 0.2])
            with dc1:
                size = doc["size"]
                size_str = f"{size / (1024*1024):.1f} MB" if size >= 1024 * 1024 else f"{size / 1024:.1f} KB"
                st.caption(f"{doc['filename']} ({size_str}, {len(doc['chunks'])} chunks)")
            with dc2:
                if st.button("\u2715", key=f"req_rm_{doc['filename']}", help="Remove"):
                    _remove_product_doc(doc["filename"])
                    st.rerun()

    # ── Step 2: Requirement Input ────────────────────────────
    _section_label("Step 2 \u2014 Requirement", "Paste the requirement to analyze")

    st.text_area(
        "Paste your requirement",
        max_chars=REQ_INPUT_MAX_CHARS,
        key="req_input_text",
        height=200,
        placeholder="e.g., Users should be able to reset their password via email...",
        label_visibility="collapsed",
    )

    current_text = st.session_state.get("req_input_text", "")
    char_count = len(current_text)
    cc_color = "#C0392B" if char_count > REQ_INPUT_MAX_CHARS * 0.9 else "#5D6D7E"
    st.markdown(
        f'<p style="text-align:right;font-size:0.75rem;color:{cc_color};margin:-0.5rem 0 0.5rem 0;">'
        f'{char_count:,} / {REQ_INPUT_MAX_CHARS:,} characters</p>',
        unsafe_allow_html=True,
    )

    analyze_col, _ = st.columns([1, 3])
    with analyze_col:
        analyze_clicked = st.button("Analyze Requirement", type="primary", use_container_width=True)

    if analyze_clicked:
        user_input = current_text.strip()
        if not user_input:
            st.error("Please paste a requirement to analyze.")
            return

        with st.spinner("Analyzing requirement..."):
            try:
                client = get_client()
                context = build_context_section(
                    st.session_state.get("system_type"),
                    st.session_state.get("selected_nfrs"),
                )
                product_ctx, product_sources = _build_product_context(user_input)
                format_rules = get_format_prompt("004")
                full_prompt = SYSTEM_PROMPT + context + format_rules
                response = client.chat.completions.create(
                    model=AZURE_OPENAI_DEPLOYMENT,
                    messages=[
                        {"role": "system", "content": full_prompt},
                        {"role": "user", "content": user_input + product_ctx},
                    ],
                )
                raw = response.choices[0].message.content
                result = normalize_markdown(ensure_sections("004", raw))

                # Parse scores
                sections = _parse_sections(result)
                scores = _parse_scores(sections)

                st.session_state["req_analysis_result"] = result
                st.session_state["req_analysis_scores"] = scores
                st.session_state["req_analysis_context"] = {
                    "system_type": st.session_state.get("system_type", ""),
                    "nfrs": list(selected_nfrs),
                    "product_sources": product_sources,
                }
                if product_sources:
                    st.info(f"Using {len(product_sources)} reference(s) from: {', '.join(product_sources)}")
            except OpenAIError as e:
                st.error(f"Analysis failed: {e}")
                return
            except Exception as e:
                st.error(f"Analysis timed out or failed. Please try again. ({e})")
                return

    # ── Step 3: Results ──────────────────────────────────────
    result = st.session_state.get("req_analysis_result")
    if result:
        _section_label("Step 3 \u2014 Analysis Results", "AI-generated analysis")

        # ── Quality Score Dashboard ──────────────────────────
        scores = st.session_state.get("req_analysis_scores", {})
        if scores and scores.get("overall", 0) > 0:
            _render_score_dashboard(scores)

        # Context badges
        ctx = st.session_state.get("req_analysis_context", {})
        badges_html = ""
        if ctx.get("system_type"):
            icon = SYSTEM_ICONS.get(ctx["system_type"], "")
            badges_html += (
                f'<span style="display:inline-block;background:#073350;color:#FFFFFF;'
                f'border-radius:20px;padding:0.25rem 0.75rem;margin:0 0.4rem 0.4rem 0;'
                f'font-size:0.75rem;font-weight:600;">{icon} {ctx["system_type"]}</span>'
            )
        for nfr in ctx.get("nfrs", []):
            icon = NFR_ICONS.get(nfr, "")
            badges_html += (
                f'<span style="display:inline-block;background:#00505D;color:#FFFFFF;'
                f'border-radius:20px;padding:0.25rem 0.75rem;margin:0 0.4rem 0.4rem 0;'
                f'font-size:0.75rem;font-weight:600;">{icon} {nfr}</span>'
            )
        if ctx.get("product_sources"):
            badges_html += (
                f'<span style="display:inline-block;background:#8E44AD;color:#FFFFFF;'
                f'border-radius:20px;padding:0.25rem 0.75rem;margin:0 0.4rem 0.4rem 0;'
                f'font-size:0.75rem;font-weight:600;">Product Context</span>'
            )
        if badges_html:
            st.markdown(
                f'<div style="margin-bottom:0.75rem;">{badges_html}</div>',
                unsafe_allow_html=True,
            )

        # ── Export Row ────────────────────────────────────────
        meta = {
            "system_type": ctx.get("system_type", ""),
            "nfrs": ctx.get("nfrs", []),
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        ec1, ec2, ec3, ec4, ec5 = st.columns(5)
        with ec1:
            render_copy_button(result)
        with ec2:
            render_download_button(result, "requirement-analysis")
        with ec3:
            conf_html = to_confluence(result, meta)
            st.download_button(
                label="Confluence",
                data=conf_html,
                file_name=f"requirement-analysis-{meta['date']}.confluence.html",
                mime="text/html",
                key="dl_confluence",
            )
        with ec4:
            jira_clicked = st.button("Create JIRA Ticket", key="btn_jira_create", use_container_width=True)
        with ec5:
            qa_lab_clicked = st.button("\U0001f9ea Send to QA Lab", key="btn_send_qa", use_container_width=True)

        # JIRA ticket creation flow
        if jira_clicked:
            # Build summary from first rewritten requirement
            sections = _parse_sections(result)
            summary = "Requirement Analysis"
            for t, b in sections:
                if "rewritten" in t.lower():
                    first_line = b.split("\n")[0].strip().lstrip("- ")
                    if first_line:
                        summary = first_line[:120]
                    break

            ticket = create_ticket(
                summary=summary,
                markdown_body=result,
                metadata=meta,
            )
            st.session_state["req_jira_ticket"] = ticket

        # Send to QA Lab flow
        if qa_lab_clicked:
            sections = _parse_sections(result)
            summary = "Requirement Analysis"
            for t, b in sections:
                if "rewritten" in t.lower():
                    first_line = b.split("\n")[0].strip().lstrip("- ")
                    if first_line:
                        summary = first_line[:120]
                    break

            jira = st.session_state.get("req_jira_ticket")
            qa_ticket = {
                "id": f"REQ-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                "title": summary,
                "requirement_text": st.session_state.get("req_input_text", ""),
                "system_type": ctx.get("system_type", ""),
                "nfrs": ctx.get("nfrs", []),
                "scores": scores,
                "result_markdown": result,
                "jira_key": jira.get("key") if jira and jira.get("success") else "",
                "jira_url": jira.get("url") if jira and jira.get("success") else "",
                "sender_email": st.session_state.get("user_email", "unknown"),
                "timestamp": datetime.now(),
                "status": "Pending",
            }
            from src.modules.qa_test_lab import _add_to_queue
            _add_to_queue(qa_ticket)
            st.session_state["nav_target"] = "\U0001f9ea  QA Test Lab"
            st.success("Sent to QA Test Lab!")
            st.rerun()

        # Show JIRA ticket result card
        ticket = st.session_state.get("req_jira_ticket")
        if ticket:
            if ticket["success"]:
                mock_badge = (
                    '<span style="display:inline-block;background:#E67E22;color:#FFF;'
                    'border-radius:12px;padding:0.15rem 0.6rem;font-size:0.7rem;font-weight:700;'
                    'margin-left:0.5rem;">DEMO MODE</span>'
                ) if ticket.get("mock") else ""

                labels_html = ""
                for lbl in ticket.get("labels", []):
                    labels_html += (
                        f'<span style="display:inline-block;background:#EAECEE;color:#5D6D7E;'
                        f'border-radius:4px;padding:0.1rem 0.5rem;font-size:0.7rem;margin:0.15rem 0.3rem 0.15rem 0;">'
                        f'{lbl}</span>'
                    )

                st.markdown(
                    f"""<div style="
                        background:#FFFFFF;border:1px solid #E0E4E8;border-left:4px solid #2E86C1;
                        border-radius:8px;padding:1rem 1.25rem;margin:0.75rem 0;
                        box-shadow:0 2px 8px rgba(0,0,0,0.05);
                    ">
                        <div style="display:flex;align-items:center;margin-bottom:0.5rem;">
                            <span style="font-size:1.1rem;margin-right:0.5rem;">\U0001f3ab</span>
                            <span style="font-size:0.95rem;font-weight:700;color:#2E86C1;">
                                JIRA Ticket Created
                            </span>
                            {mock_badge}
                        </div>
                        <div style="display:flex;gap:1.5rem;flex-wrap:wrap;margin-bottom:0.5rem;">
                            <div>
                                <span style="font-size:0.72rem;text-transform:uppercase;color:#5D6D7E;font-weight:600;">Key</span><br/>
                                <span style="font-size:0.95rem;font-weight:700;color:#111111;">{ticket["key"]}</span>
                            </div>
                            <div>
                                <span style="font-size:0.72rem;text-transform:uppercase;color:#5D6D7E;font-weight:600;">Project</span><br/>
                                <span style="font-size:0.95rem;color:#111111;">{ticket.get("project", "")}</span>
                            </div>
                            <div>
                                <span style="font-size:0.72rem;text-transform:uppercase;color:#5D6D7E;font-weight:600;">Type</span><br/>
                                <span style="font-size:0.95rem;color:#111111;">{ticket.get("issue_type", "Story")}</span>
                            </div>
                            <div>
                                <span style="font-size:0.72rem;text-transform:uppercase;color:#5D6D7E;font-weight:600;">Created</span><br/>
                                <span style="font-size:0.95rem;color:#111111;">{ticket.get("created_at", "")}</span>
                            </div>
                        </div>
                        <div style="font-size:0.85rem;color:#111111;margin-bottom:0.4rem;">
                            <strong>Summary:</strong> {ticket.get("summary", "")[:150]}
                        </div>
                        <div style="margin-bottom:0.4rem;">{labels_html}</div>
                        <a href="{ticket.get("url", "#")}" target="_blank" style="
                            font-size:0.82rem;color:#2E86C1 !important;font-weight:600;text-decoration:none;
                        ">
                            Open in JIRA &#8599;
                        </a>
                    </div>""",
                    unsafe_allow_html=True,
                )
            else:
                st.error(f"Failed to create JIRA ticket: {ticket.get('error', 'Unknown error')}")

        # ── Section Cards ────────────────────────────────────
        sections = _parse_sections(result)

        for title, body in sections:
            if "quality score" in title.lower():
                continue  # already rendered as dashboard

            sec_meta = SECTION_META.get(title, {"icon": "\U0001f4cb", "color": "#00505D"})
            accent = sec_meta["color"]
            icon = sec_meta["icon"]

            st.markdown(
                f"""<div style="
                    background:#FFFFFF;
                    border:1px solid #E0E4E8;
                    border-left:4px solid {accent};
                    border-radius:8px;
                    padding:1rem 1.25rem;
                    margin-bottom:0.75rem;
                    box-shadow:0 1px 6px rgba(0,0,0,0.03);
                ">
                    <div style="display:flex;align-items:center;margin-bottom:0.5rem;">
                        <span style="font-size:1.2rem;margin-right:0.5rem;">{icon}</span>
                        <span style="font-size:1rem;font-weight:700;color:{accent};">{title}</span>
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )
            st.markdown(body)
            render_copy_button(f"## {title}\n{body}", label="Copy section")

