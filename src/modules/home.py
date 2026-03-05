import os
import base64
from functools import lru_cache

import streamlit as st
from src.config import BRAND_LOGO_WHITE_PATH, BRAND_LOGO_PATH


MODULE_CARDS = [
    {
        "icon": "\U0001f4da",
        "title": "Company Resources",
        "description": "Find Confluence, Jira, SharePoint, and training materials for all Komutel products in one place.",
        "key": "\U0001f4da  Company Resources",
        "audience": "Everyone",
    },
    {
        "icon": "\U0001f680",
        "title": "Onboarding Planner",
        "description": "Generate personalized 2-week onboarding plans based on role, product, experience, and CV analysis.",
        "key": "\U0001f680  Onboarding Planner",
        "audience": "HR & Team Leads",
    },
    {
        "icon": "\U0001f4dd",
        "title": "Smart Writer",
        "description": "Transform rough notes, emails, or ideas into polished, structured content with audience and tone control.",
        "key": "\U0001f4dd  Smart Writer",
        "audience": "Everyone",
    },
    {
        "icon": "\U0001f50d",
        "title": "Requirement Analyzer",
        "description": "Analyze requirements for completeness, ambiguity, and testability. Export to JIRA with one click.",
        "key": "\U0001f50d  Requirement Analyzer",
        "audience": "Product Managers & QA",
    },
    {
        "icon": "\U0001f9ea",
        "title": "QA Test Lab",
        "description": "Generate comprehensive test suites from requirements. Pick tickets from the queue or paste directly.",
        "key": "\U0001f9ea  QA Test Lab",
        "audience": "QA & Developers",
    },
]

STEPS = [
    {
        "num": "1",
        "title": "Choose a Module",
        "desc": "Select one of the AI-powered tools from the sidebar or the cards below.",
    },
    {
        "num": "2",
        "title": "Provide Context",
        "desc": "Enter your requirements, notes, or upload documents to give the AI relevant context.",
    },
    {
        "num": "3",
        "title": "Generate & Export",
        "desc": "Review AI-generated output, iterate as needed, then copy or download the results.",
    },
]


@lru_cache(maxsize=4)
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


def render():
    # ── Hero Banner ──────────────────────────────────────────────
    logo_white = _get_logo_html(white=True, width=160)
    st.markdown(
        f"""<div style="
            background: linear-gradient(135deg, #111111 0%, #073350 100%);
            border-radius: 12px;
            padding: 2.5rem 2rem 2rem 2rem;
            text-align: center;
            margin-bottom: 1.5rem;
        ">
            {f'<div style="margin-bottom: 1rem;">{logo_white}</div>' if logo_white else ''}
            <div class="hero-title" style="margin: 0; font-size: 2rem; font-weight: 700; line-height: 1.2;">
                Welcome to <span style="color: #F39C12 !important;">Versaterm</span> Academy
            </div>
            <style>.hero-title, .hero-title * {{ color: #FFFFFF !important; }}</style>
            <p style="color: rgba(255,255,255,0.85); font-size: 1.1rem; max-width: 640px;
                margin: 1rem auto 0 auto; line-height: 1.7; font-weight: 500;">
                Your AI-powered command center for onboarding, documentation, and requirements.
            </p>
            <p style="color: rgba(255,255,255,0.55); font-size: 0.88rem; max-width: 580px;
                margin: 0.5rem auto 0 auto; line-height: 1.6;">
                Write better requirements. Create knowledge articles in seconds.
                Onboard new teammates with personalized plans. All in one place.
            </p>
        </div>""",
        unsafe_allow_html=True,
    )

    # ── How It Works ─────────────────────────────────────────────
    st.markdown(
        '<div style="border-left: 4px solid #00505D; padding: 0.5rem 1rem; margin: 0.5rem 0 1rem 0; '
        'background: #F4F6F7; border-radius: 0 8px 8px 0;">'
        '<span style="font-size: 1.05rem; color: #111111; font-weight: 600;">How It Works</span></div>',
        unsafe_allow_html=True,
    )

    step_cols = st.columns(3, gap="large")
    for col, step in zip(step_cols, STEPS):
        with col:
            st.markdown(
                f"""<div style="
                    text-align: center;
                    padding: 1.25rem 1rem;
                ">
                    <div style="
                        display: inline-flex; align-items: center; justify-content: center;
                        width: 44px; height: 44px; border-radius: 50%;
                        background: #00505D; color: #FFFFFF;
                        font-size: 1.1rem; font-weight: 700; margin-bottom: 0.6rem;
                    ">{step['num']}</div>
                    <div style="font-size: 0.95rem; font-weight: 600; color: #111111; margin-bottom: 0.3rem;">
                        {step['title']}
                    </div>
                    <p style="font-size: 0.83rem; color: #5D6D7E; line-height: 1.5; margin: 0;">
                        {step['desc']}
                    </p>
                </div>""",
                unsafe_allow_html=True,
            )

    # ── Module Cards ─────────────────────────────────────────────
    st.markdown(
        '<div style="border-left: 4px solid #00505D; padding: 0.5rem 1rem; margin: 1.5rem 0 1rem 0; '
        'background: #F4F6F7; border-radius: 0 8px 8px 0;">'
        '<span style="font-size: 1.05rem; color: #111111; font-weight: 600;">Available Modules</span>'
        '<span style="font-size: 0.8rem; color: #5D6D7E; margin-left: 0.5rem;">Click a card to get started</span></div>',
        unsafe_allow_html=True,
    )

    def _render_card(card):
        st.markdown(
            f'<div style="'
            f'background:#FFFFFF;border:1px solid #E0E4E8;border-radius:10px;'
            f'padding:1.5rem 1.25rem;text-align:center;height:230px;'
            f'box-shadow:0 2px 12px rgba(0,0,0,0.04);border-top:3px solid #00505D;'
            f'display:flex;flex-direction:column;align-items:center;justify-content:flex-start;'
            f'">'
            f'<div style="font-size:2.2rem;margin-bottom:0.5rem;flex-shrink:0;">{card["icon"]}</div>'
            f'<div style="margin:0 0 0.3rem 0;font-size:1.05rem;color:#111111;font-weight:600;flex-shrink:0;">{card["title"]}</div>'
            f'<div style="display:inline-block;background:#00505D;color:#FFF;border-radius:12px;'
            f'padding:0.1rem 0.55rem;font-size:0.65rem;font-weight:600;margin-bottom:0.4rem;'
            f'letter-spacing:0.02em;flex-shrink:0;">{card.get("audience", "")}</div>'
            f'<p style="font-size:0.83rem;color:#5D6D7E;line-height:1.5;margin:0;flex:1;">'
            f'{card["description"]}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
        if st.button(f"Open {card['title']}", key=f"go_{card['key']}", use_container_width=True, type="primary"):
            st.session_state["nav_target"] = card["key"]
            st.rerun()

    # Row 1: first 3 cards
    row1 = st.columns(3, gap="large")
    for col, card in zip(row1, MODULE_CARDS[:3]):
        with col:
            _render_card(card)

    # Row 2: last 2 cards, centered with padding columns
    r2_pad_l, r2_c1, r2_c2, r2_pad_r = st.columns([0.5, 1, 1, 0.5], gap="large")
    with r2_c1:
        _render_card(MODULE_CARDS[3])
    with r2_c2:
        _render_card(MODULE_CARDS[4])

    # ── Quick Try Examples ─────────────────────────────────────────
    st.markdown(
        '<div style="border-left: 4px solid #F39C12; padding: 0.5rem 1rem; margin: 1.5rem 0 1rem 0; '
        'background: #F4F6F7; border-radius: 0 8px 8px 0;">'
        '<span style="font-size: 1.05rem; color: #111111; font-weight: 600;">Quick Try</span>'
        '<span style="font-size: 0.8rem; color: #5D6D7E; margin-left: 0.5rem;">'
        'Jump straight into a module with a pre-filled example</span></div>',
        unsafe_allow_html=True,
    )

    QUICK_EXAMPLES = [
        {
            "label": "\U0001f50d  Analyze a 911 Requirement",
            "module": "\U0001f50d  Requirement Analyzer",
            "prefill_key": "req_input_text",
            "prefill_value": "When a 911 call is received, the system shall automatically display the caller's location on the dispatch map within 2 seconds. If the caller is on a VoIP line, the system shall fall back to the registered address and display a confidence indicator.",
        },
        {
            "label": "\U0001f4dd  Write a KB Article",
            "module": "\U0001f4dd  Smart Writer",
            "prefill_key": "kb_input_text",
            "prefill_value": "customer called about password reset, told them to go to settings > security > reset password, they needed to verify email first, took about 5 mins, resolved successfully",
        },
        {
            "label": "\U0001f680  Plan Onboarding for a QA Engineer",
            "module": "\U0001f680  Onboarding Planner",
            "prefill_key": "onb_role",
            "prefill_value": "QA Engineer",
        },
    ]

    ex_cols = st.columns(len(QUICK_EXAMPLES), gap="medium")
    for col, ex in zip(ex_cols, QUICK_EXAMPLES):
        with col:
            if st.button(ex["label"], key=f"quick_{ex['label']}", use_container_width=True):
                st.session_state[ex["prefill_key"]] = ex["prefill_value"]
                st.session_state["nav_target"] = ex["module"]
                st.rerun()

    # ── Tips & Guidelines ────────────────────────────────────────
    st.markdown("")

    tip_left, tip_right = st.columns(2, gap="large")

    with tip_left:
        st.markdown(
            """<div style="
                background: #F4F6F7;
                border: 1px solid #E0E4E8;
                border-radius: 10px;
                padding: 1.25rem 1.5rem;
                min-height: 180px;
            ">
                <div style="font-size: 0.95rem; font-weight: 600; color: #00505D; margin-bottom: 0.6rem;">
                    Tips for Best Results
                </div>
                <ul style="font-size: 0.83rem; color: #5D6D7E; line-height: 1.8; padding-left: 1.2rem; margin: 0;">
                    <li>Upload product documents in the sidebar to give the AI more context about your project.</li>
                    <li>Be specific with your inputs — the more detail you provide, the better the output.</li>
                    <li>Use the Onboarding Planner with a CV upload for personalized training plans.</li>
                    <li>All outputs can be copied or downloaded — nothing is saved on the server.</li>
                </ul>
            </div>""",
            unsafe_allow_html=True,
        )

    with tip_right:
        st.markdown(
            """<div style="
                background: #F4F6F7;
                border: 1px solid #E0E4E8;
                border-radius: 10px;
                padding: 1.25rem 1.5rem;
                min-height: 180px;
            ">
                <div style="font-size: 0.95rem; font-weight: 600; color: #00505D; margin-bottom: 0.6rem;">
                    Who Is This For?
                </div>
                <ul style="font-size: 0.83rem; color: #5D6D7E; line-height: 1.8; padding-left: 1.2rem; margin: 0;">
                    <li><strong>Product Managers</strong> — analyze and refine software requirements.</li>
                    <li><strong>Technical Writers</strong> — generate KB articles from rough notes.</li>
                    <li><strong>Team Leads & HR</strong> — create onboarding plans for new hires.</li>
                    <li><strong>New Employees</strong> — find company resources and get up to speed fast.</li>
                    <li><strong>QA Testers</strong> — generate test suites and edge cases from requirements.</li>
                </ul>
            </div>""",
            unsafe_allow_html=True,
        )

    # ── About Banner ─────────────────────────────────────────────
    st.markdown("")
    st.markdown(
        """<div style="
            background: linear-gradient(135deg, #111111 0%, #073350 100%);
            border-radius: 10px;
            padding: 1.75rem 2rem;
        ">
            <div style="font-size: 1.1rem; font-weight: 600; color: #FFFFFF; margin-bottom: 0.5rem;">
                About Versaterm
            </div>
            <p style="color: rgba(255,255,255,0.75); line-height: 1.7; margin-bottom: 0; font-size: 0.92rem;">
                Versaterm is a leading provider of public safety software solutions,
                serving law enforcement, fire, and EMS agencies across North America.
                The Academy platform uses AI to streamline training, documentation,
                and knowledge management across teams. Upload your own documents for
                context-aware AI responses, or use the tools standalone.
            </p>
        </div>""",
        unsafe_allow_html=True,
    )

