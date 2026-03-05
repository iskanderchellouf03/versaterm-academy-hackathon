import os
import base64
from functools import lru_cache

import streamlit as st
from src.config import (
    KOMUTEL_RESOURCES,
    BRAND_LOGO_WHITE_PATH, BRAND_LOGO_PATH,
    BRAND_PRIMARY_COLOR,
)

KOMUTEL_PRODUCTS = {
    "Kore": {"icon": "\U0001f4de", "desc": "Core telephony platform"},
    "Komlog": {"icon": "\U0001f4cb", "desc": "Logging & call recording"},
    "SIT911": {"icon": "\U0001f6a8", "desc": "911 call processing"},
    "Kontact": {"icon": "\U0001f4ac", "desc": "Contact center platform"},
    "Komuync": {"icon": "\U0001f310", "desc": "Unified communications"},
}

CATEGORY_ICONS = {
    "Documentation": "\U0001f4c4",
    "Knowledge Base": "\U0001f4da",
    "Project Management": "\U0001f4cb",
    "Communication": "\U0001f4ac",
    "HR & Onboarding": "\U0001f465",
    "Presentations": "\U0001f4ca",
    "Testing": "\U0001f9ea",
}

CATEGORY_COLORS = {
    "Documentation": "#00505D",
    "Knowledge Base": "#2E86C1",
    "Project Management": "#8E44AD",
    "Communication": "#27AE60",
    "HR & Onboarding": "#E67E22",
    "Presentations": "#C0392B",
    "Testing": "#16A085",
}


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


def _render_resource_card(resource):
    cat = resource.get("category", "")
    title = resource["title"]
    desc = resource.get("description", "")
    url = resource.get("url", "#")
    accent = CATEGORY_COLORS.get(cat, "#00505D")
    icon = CATEGORY_ICONS.get(cat, "\U0001f517")

    st.markdown(
        f"""<a href="{url}" target="_blank" style="text-decoration: none; display: block;">
            <div style="
                background: #FFFFFF;
                border: 1px solid #E0E4E8;
                border-radius: 10px;
                padding: 1.1rem 1.25rem;
                margin-bottom: 0.6rem;
                box-shadow: 0 1px 6px rgba(0,0,0,0.03);
                transition: box-shadow 0.2s ease, transform 0.15s ease;
                cursor: pointer;
                position: relative;
                overflow: hidden;
            " onmouseover="this.style.boxShadow='0 4px 16px rgba(0,0,0,0.08)';this.style.transform='translateY(-1px)'"
               onmouseout="this.style.boxShadow='0 1px 6px rgba(0,0,0,0.03)';this.style.transform='none'">
                <div style="position: absolute; top: 0; left: 0; width: 4px; height: 100%;
                    background: {accent}; border-radius: 10px 0 0 10px;"></div>
                <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding-left: 0.5rem;">
                    <div style="font-size: 1.3rem; margin-top: 0.1rem;">{icon}</div>
                    <div style="flex: 1; min-width: 0;">
                        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                            <span style="font-size: 0.92rem; color: #111111; font-weight: 600;">{title}</span>
                            <span style="font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.08em;
                                color: {accent}; font-weight: 700; background: {accent}14;
                                padding: 0.1rem 0.45rem; border-radius: 4px; white-space: nowrap;">{cat}</span>
                        </div>
                        <p style="font-size: 0.8rem; color: #5D6D7E; margin: 0; line-height: 1.45;">
                            {desc}
                        </p>
                    </div>
                    <div style="color: #BDC3C7; font-size: 1rem; margin-top: 0.2rem; flex-shrink: 0;">&#8599;</div>
                </div>
            </div>
        </a>""",
        unsafe_allow_html=True,
    )


def render():
    # --- Hero Header ---
    logo_white = _get_logo_html(white=True, width=140)
    st.markdown(
        f"""<div style="
            background: linear-gradient(135deg, #111111 0%, #073350 100%);
            border-radius: 10px;
            padding: 1.75rem 2rem;
            margin-bottom: 1.25rem;
            text-align: center;
        ">
            {f'<div style="margin-bottom: 0.75rem;">{logo_white}</div>' if logo_white else ''}
            <div class="hero-title" style="margin: 0; font-size: 1.75rem; font-weight: 700; line-height: 1.2;">
                Company Resources
            </div>
            <style>.hero-title, .hero-title * {{ color: #FFFFFF !important; }}</style>
            <p style="color: rgba(255,255,255,0.75); font-size: 0.95rem; margin: 0.4rem 0 0 0; line-height: 1.5;">
                Find documentation, tools, and training materials for your team. Select your product to see relevant links.
            </p>
        </div>""",
        unsafe_allow_html=True,
    )

    # --- General Resources (always visible) ---
    global_resources = KOMUTEL_RESOURCES.get("_global", [])
    if global_resources:
        st.markdown(
            '<div style="border-left: 4px solid #00505D; padding: 0.5rem 1rem; margin: 0.5rem 0 0.75rem 0; '
            'background: #F4F6F7; border-radius: 0 8px 8px 0;">'
            '<span style="font-size: 1rem; color: #111111; font-weight: 600;">'
            '\U0001f3e2  Company-Wide Tools</span>'
            '<span style="font-size: 0.78rem; color: #5D6D7E; margin-left: 0.5rem;">'
            'Available to all employees</span></div>',
            unsafe_allow_html=True,
        )
        cols = st.columns(2)
        for i, res in enumerate(global_resources):
            with cols[i % 2]:
                _render_resource_card(res)

    # --- Product Selection ---
    st.markdown("")
    st.markdown(
        '<div style="border-left: 4px solid #2E86C1; padding: 0.5rem 1rem; margin: 0.75rem 0 0.75rem 0; '
        'background: #F4F6F7; border-radius: 0 8px 8px 0;">'
        '<span style="font-size: 1rem; color: #111111; font-weight: 600;">'
        '\U0001f4e6  Product Resources</span>'
        '<span style="font-size: 0.78rem; color: #5D6D7E; margin-left: 0.5rem;">'
        'Select your product to see team-specific links</span></div>',
        unsafe_allow_html=True,
    )

    # Product selector as clickable cards
    selected_product = st.session_state.get("res_selected_product", None)

    product_names = list(KOMUTEL_PRODUCTS.keys())
    card_cols = st.columns(len(product_names))

    for col, name in zip(card_cols, product_names):
        meta = KOMUTEL_PRODUCTS[name]
        is_active = selected_product == name
        bg = f"{BRAND_PRIMARY_COLOR}" if is_active else "#FFFFFF"
        text_color = "#FFFFFF" if is_active else "#111111"
        desc_color = "rgba(255,255,255,0.75)" if is_active else "#5D6D7E"
        border = f"2px solid {BRAND_PRIMARY_COLOR}" if is_active else "1px solid #E0E4E8"
        shadow = "0 4px 16px rgba(0,80,93,0.2)" if is_active else "0 1px 6px rgba(0,0,0,0.04)"
        resource_count = len(KOMUTEL_RESOURCES.get(name, []))

        with col:
            st.markdown(
                f"""<div style="
                    background: {bg};
                    border: {border};
                    border-radius: 10px;
                    padding: 1rem 0.75rem;
                    text-align: center;
                    cursor: pointer;
                    transition: all 0.15s ease;
                    box-shadow: {shadow};
                    min-height: 110px;
                    display: flex; flex-direction: column; align-items: center; justify-content: center;
                ">
                    <div style="font-size: 1.6rem; margin-bottom: 0.3rem;">{meta['icon']}</div>
                    <div style="font-size: 0.92rem; font-weight: 700; color: {text_color}; margin-bottom: 0.15rem;">
                        {name}
                    </div>
                    <div style="font-size: 0.7rem; color: {desc_color}; line-height: 1.3;">
                        {meta['desc']}
                    </div>
                    <div style="font-size: 0.6rem; color: {desc_color}; margin-top: 0.35rem;
                        font-weight: 600; letter-spacing: 0.04em;">
                        {resource_count} resource{'s' if resource_count != 1 else ''}
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )
            if st.button(
                f"{'Selected' if is_active else 'Select'}",
                key=f"prod_{name}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                if is_active:
                    st.session_state["res_selected_product"] = None
                else:
                    st.session_state["res_selected_product"] = name
                st.rerun()

    # --- Selected Product Resources ---
    if selected_product and selected_product in KOMUTEL_PRODUCTS:
        product_resources = KOMUTEL_RESOURCES.get(selected_product, [])
        meta = KOMUTEL_PRODUCTS[selected_product]

        st.markdown("")
        st.markdown(
            f'<div style="border-left: 4px solid {BRAND_PRIMARY_COLOR}; padding: 0.5rem 1rem; '
            f'margin: 0.5rem 0 0.75rem 0; background: #F4F6F7; border-radius: 0 8px 8px 0;">'
            f'<span style="font-size: 1.3rem; margin-right: 0.4rem;">{meta["icon"]}</span>'
            f'<span style="font-size: 1rem; color: #111111; font-weight: 600;">'
            f'{selected_product} Resources</span>'
            f'<span style="font-size: 0.78rem; color: #5D6D7E; margin-left: 0.5rem;">'
            f'{meta["desc"]}</span></div>',
            unsafe_allow_html=True,
        )

        if product_resources:
            cols = st.columns(2)
            for i, res in enumerate(product_resources):
                with cols[i % 2]:
                    _render_resource_card(res)
        else:
            st.info(f"No specific resources configured for {selected_product} yet.")

    elif not selected_product:
        # Hint when nothing selected
        st.markdown("")
        st.markdown(
            '<div style="text-align: center; padding: 1.5rem 1rem; color: #5D6D7E; '
            'font-size: 0.85rem; background: #F9FAFB; border: 1px dashed #D5DBDB; '
            'border-radius: 10px; margin-top: 0.5rem;">'
            '\U0001f446  Select a product above to see team-specific documentation, '
            'Confluence spaces, and Jira boards.'
            '</div>',
            unsafe_allow_html=True,
        )

