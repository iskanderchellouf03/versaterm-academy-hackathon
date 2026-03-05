import os
import base64
from functools import lru_cache

import streamlit as st
from datetime import datetime

from src.auth.db import init_db
from src.auth.service import (
    validate_email, generate_code, verify_code,
    check_session_timeout, update_activity, logout,
    check_rate_limit, create_session, validate_session,
)
from src.auth.email import send_code_email
from src.modules import MODULES
from src.components.demo_banner import render_demo_banner
from src.components.branding import render_branding
from src.theme.css import inject_theme_css, inject_login_css
from src.config import BRAND_LOGO_WHITE_PATH, BRAND_LOGO_PATH, BRAND_SUBTITLE, BRAND_PRIMARY_COLOR


def main():
    st.set_page_config(
        page_title="Versaterm Academy",
        page_icon="\U0001f393",
        layout="wide",
    )

    init_db()

    # Restore session from query params on refresh
    if not st.session_state.get("authenticated"):
        token = st.query_params.get("session")
        if token:
            email = validate_session(token)
            if email:
                st.session_state["authenticated"] = True
                st.session_state["user_email"] = email
                st.session_state["session_token"] = token
                st.session_state["login_time"] = datetime.utcnow()
                st.session_state["last_activity"] = datetime.utcnow()

    inject_theme_css()
    render_demo_banner()

    if st.session_state.get("authenticated"):
        # Session timeout check
        if check_session_timeout():
            for key in ["authenticated", "user_email", "login_time", "last_activity", "session_token"]:
                st.session_state.pop(key, None)
            st.query_params.clear()
            st.rerun()
        update_activity()

        # Sidebar
        with st.sidebar:
            render_branding(show_subtitle=False, dark_bg=True)

            # Spacer
            st.markdown('<div style="height:0.75rem;"></div>', unsafe_allow_html=True)

            # User identity card with avatar
            user_email = st.session_state.get("user_email", "")
            user_name = user_email.split("@")[0].replace(".", " ").title() if user_email else ""
            initials = "".join(w[0] for w in user_name.split()[:2]).upper() if user_name else "?"
            st.markdown(
                f"""<div style="
                    background: rgba(255,255,255,0.07);
                    border: 1px solid rgba(255,255,255,0.1);
                    border-radius: 10px;
                    padding: 0.7rem 0.9rem;
                    margin: 0 0 0.75rem 0;
                    display: flex;
                    align-items: center;
                    gap: 0.65rem;
                ">
                    <div style="
                        width: 36px; height: 36px; border-radius: 50%;
                        background: linear-gradient(135deg, #00505D, #F39C12);
                        display: flex; align-items: center; justify-content: center;
                        font-size: 0.75rem; font-weight: 700; color: #FFFFFF;
                        flex-shrink: 0;
                    ">{initials}</div>
                    <div style="min-width: 0;">
                        <div style="font-size:0.82rem;font-weight:600;color:#FFFFFF;
                            white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                            {user_name}
                        </div>
                        <div style="font-size:0.68rem;color:rgba(255,255,255,0.45);
                            white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                            {user_email}
                        </div>
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )

        # ── Grouped sidebar navigation ────────────────────────
        NAV_GROUPS = [
            {
                "label": "General",
                "hint": "For everyone",
                "modules": [
                    "\U0001f3e0  Home",
                    "\U0001f4da  Company Resources",
                    "\U0001f4dd  Smart Writer",
                ],
            },
            {
                "label": "Planning",
                "hint": "PMs & Team Leads",
                "modules": [
                    "\U0001f680  Onboarding Planner",
                    "\U0001f50d  Requirement Analyzer",
                ],
            },
            {
                "label": "Quality",
                "hint": "QA & Developers",
                "modules": [
                    "\U0001f9ea  QA Test Lab",
                ],
            },
        ]

        module_keys = list(MODULES.keys())
        nav_target = st.session_state.get("nav_target")
        if nav_target and nav_target in module_keys:
            st.session_state["active_module"] = nav_target
            del st.session_state["nav_target"]

        current = st.session_state.get("active_module", module_keys[0])

        with st.sidebar:
            for group in NAV_GROUPS:
                st.markdown(
                    f'<div style="font-size:0.6rem;opacity:0.35;margin:0.7rem 0 0.1rem 0.25rem;'
                    f'letter-spacing:0.1em;text-transform:uppercase;font-weight:700;">{group["label"]}'
                    f'</div>'
                    f'<div style="font-size:0.62rem;color:rgba(255,255,255,0.3);'
                    f'margin:0 0 0.25rem 0.25rem;">{group["hint"]}</div>',
                    unsafe_allow_html=True,
                )
                for mod in group["modules"]:
                    is_active = mod == current
                    btn_type = "primary" if is_active else "secondary"
                    if st.button(mod, key=f"nav_{mod}", use_container_width=True, type=btn_type):
                        if not is_active:
                            st.session_state["active_module"] = mod
                            st.rerun()

            # Spacer to push logout to bottom
            st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)

            # Divider + version info
            st.markdown(
                '<div style="border-top:1px solid rgba(255,255,255,0.06);margin:0 0 0.6rem 0;"></div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<style>'
                '#sidebar_logout {'
                '  background: transparent !important;'
                '  border: 1.5px solid rgba(231,76,60,0.4) !important;'
                '  color: rgba(231,76,60,0.85) !important;'
                '  display: flex !important;'
                '  justify-content: center !important;'
                '}'
                '#sidebar_logout * { color: rgba(231,76,60,0.85) !important; text-align: center !important; }'
                '#sidebar_logout:hover {'
                '  background: rgba(231,76,60,0.12) !important;'
                '  border-color: rgba(231,76,60,0.6) !important;'
                '}'
                '#sidebar_logout:hover * { color: #E74C3C !important; }'
                '</style>',
                unsafe_allow_html=True,
            )
            st.button("\U0001f6aa  Log out", on_click=logout, use_container_width=True, key="sidebar_logout")

            st.markdown(
                '<div style="text-align:center;font-size:0.58rem;color:rgba(255,255,255,0.2);'
                'margin-top:0.5rem;letter-spacing:0.03em;">Versaterm Academy v1.0</div>',
                unsafe_allow_html=True,
            )

        selected = st.session_state.get("active_module", module_keys[0])

        # Dispatch to selected module
        MODULES[selected]()

        # Page navigation arrows then footer
        _render_page_nav(module_keys, selected)
        _render_footer()
    else:
        _render_login()


def _render_page_nav(module_keys, current):
    """Render Previous / Next arrows at the bottom of the page."""
    idx = module_keys.index(current) if current in module_keys else 0
    has_prev = idx > 0
    has_next = idx < len(module_keys) - 1

    if not has_prev and not has_next:
        return

    prev_label = module_keys[idx - 1] if has_prev else ""
    next_label = module_keys[idx + 1] if has_next else ""

    # Clean labels (remove emoji prefix for display)
    def _clean(label):
        parts = label.split("  ", 1)
        return parts[1] if len(parts) > 1 else label

    st.markdown(
        '<div style="border-top:1px solid #E0E4E8;margin:2.5rem 0 0 0;padding-top:1rem;"></div>',
        unsafe_allow_html=True,
    )

    col_prev, col_spacer, col_next = st.columns([1, 2, 1])

    with col_prev:
        if has_prev:
            if st.button(f"\u2190  {_clean(prev_label)}", key="nav_prev", use_container_width=True):
                st.session_state["active_module"] = prev_label
                st.rerun()

    with col_next:
        if has_next:
            if st.button(f"{_clean(next_label)}  \u2192", key="nav_next", use_container_width=True, type="primary"):
                st.session_state["active_module"] = next_label
                st.rerun()


@lru_cache(maxsize=2)
def _logo_b64(path):
    if not os.path.exists(path):
        return None
    if path.endswith(".svg"):
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
        return base64.b64encode(data.encode("utf-8")).decode("utf-8")
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")


def _render_footer():
    b64 = _logo_b64(BRAND_LOGO_PATH)
    logo_html = ""
    if b64:
        mime = "image/svg+xml" if BRAND_LOGO_PATH.endswith(".svg") else "image/png"
        logo_html = f'<img src="data:{mime};base64,{b64}" width="100" />'
    st.markdown(
        f"""<div style="
            text-align: center;
            margin-top: 3rem;
            padding: 1.5rem 0;
            border-top: 1px solid #E0E4E8;
        ">
            {logo_html}
            <p style="color: #BDC3C7; font-size: 0.75rem; margin: 0.5rem 0 0 0;">
                Versaterm Academy &mdash; AI-Powered Training &amp; Development
            </p>
            <p style="color: #D5DBDB; font-size: 0.7rem; margin: 0.25rem 0 0 0;">
                &copy; 2026 Versaterm Inc. All rights reserved.
            </p>
        </div>""",
        unsafe_allow_html=True,
    )


def _handle_send_code(email):
    """Validate email, check rate limit, generate and send code."""
    if not email:
        st.error("Please enter your email address.")
        return
    valid, error_msg = validate_email(email)
    if not valid:
        st.error(error_msg)
        return
    allowed, _ = check_rate_limit(email)
    if not allowed:
        st.error("Too many code requests. Please try again in a few minutes.")
        return
    code = generate_code(email)
    sent = send_code_email(email, code)
    st.session_state["login_email"] = email
    st.session_state["login_code_sent_via_smtp"] = sent
    if not sent:
        st.session_state["login_dev_code"] = code


def _render_login():
    inject_login_css()

    st.markdown("<div style='height: 5vh'></div>", unsafe_allow_html=True)

    # Branding header (white logo on dark background)
    logo_html = ""
    if os.path.exists(BRAND_LOGO_WHITE_PATH):
        with open(BRAND_LOGO_WHITE_PATH, "r", encoding="utf-8") as f:
            svg_data = f.read()
        b64 = base64.b64encode(svg_data.encode("utf-8")).decode("utf-8")
        logo_html = f'<img src="data:image/svg+xml;base64,{b64}" width="200" style="margin-bottom: 0.5rem;" />'

    st.markdown(
        f"""<div style="text-align: center;">
            {logo_html}
            <p style="color: rgba(255,255,255,0.65); font-size: 0.9rem; margin: 0.2rem 0 0 0;">
                {BRAND_SUBTITLE}
            </p>
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown("")

    code_sent = st.session_state.get("login_email")

    if not code_sent:
        # Step 1: Email entry — form so Enter key triggers Send Code
        with st.form("login_email_form", border=True):
            st.markdown("**Employee Login**")
            st.caption("Enter your company email to receive an access code.")
            email = st.text_input(
                "Work email", key="login_email_input",
                placeholder="you@versaterm.com",
            )
            submitted = st.form_submit_button("Send Code", use_container_width=True, type="primary")
            if submitted:
                _handle_send_code(email)

    # Step 2: Code verification
    if st.session_state.get("login_email"):
        with st.form("login_code_form", border=True):
            st.markdown("**Verify your identity**")
            st.markdown(
                f'<p style="font-size: 0.85rem; color: #5D6D7E !important; margin: -0.5rem 0 0.5rem 0;">'
                f'Code sent to <strong style="color: {BRAND_PRIMARY_COLOR} !important;">{st.session_state["login_email"]}</strong></p>',
                unsafe_allow_html=True,
            )

            dev_code = st.session_state.get("login_dev_code")
            if dev_code:
                st.info(f"**Dev mode** \u2014 Your code is: `{dev_code}`")

            code_input = st.text_input(
                "Access Code", key="login_code_input", max_chars=6,
                placeholder="Enter 6-digit code",
            )

            col1, col2 = st.columns(2)
            with col1:
                verify_clicked = st.form_submit_button("Verify & Sign In", type="primary", use_container_width=True)
            with col2:
                resend_clicked = st.form_submit_button("Resend Code", use_container_width=True)

        if verify_clicked:
            if not code_input:
                st.error("Please enter the access code.")
            else:
                success, error_msg = verify_code(st.session_state["login_email"], code_input)
                if success:
                    email = st.session_state["login_email"]
                    token = create_session(email)
                    st.session_state["authenticated"] = True
                    st.session_state["user_email"] = email
                    st.session_state["session_token"] = token
                    st.session_state["login_time"] = datetime.utcnow()
                    st.session_state["last_activity"] = datetime.utcnow()
                    st.query_params["session"] = token
                    st.rerun()
                else:
                    st.error(error_msg)
        elif resend_clicked:
            _handle_send_code(st.session_state["login_email"])

    st.markdown(
        '<p style="text-align:center; color:#BDC3C7; font-size:0.75rem; margin-top:1.5rem;">'
        '\u00a9 2026 Versaterm Inc.</p>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
