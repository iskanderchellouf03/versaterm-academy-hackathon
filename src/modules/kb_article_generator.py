import os
import base64

import streamlit as st
from openai import OpenAIError

from src.ai.client import get_client
from src.ai.prompts.kb_article_generator import SYSTEM_PROMPT, build_kb_context
from src.config import (
    AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT, KB_INPUT_MAX_CHARS,
    AUDIENCES, TONES, BRAND_LOGO_WHITE_PATH, BRAND_LOGO_PATH,
)
from src.components.copy_button import render_copy_button
from src.components.download_button import render_download_button
from src.output.prompt import get_format_prompt
from src.output.normalizer import ensure_sections, normalize_markdown


AUDIENCE_META = {
    "Internal": {"icon": "\U0001f3e2", "color": "#00505D", "hint": "Employees who know the product"},
    "External": {"icon": "\U0001f310", "color": "#2E86C1", "hint": "Customers with no insider knowledge"},
    "Support": {"icon": "\U0001f6e0\ufe0f", "color": "#8E44AD", "hint": "Support agents resolving tickets"},
}

TONE_META = {
    "Formal": {"icon": "\U0001f454", "hint": "Professional, third-person, no contractions"},
    "Conversational": {"icon": "\U0001f4ac", "hint": "Friendly, second-person, approachable"},
    "Concise": {"icon": "\u26a1", "hint": "Bullet-heavy, minimal prose, quick-reference"},
}

SECTION_META = {
    "Title": {"icon": "\U0001f3f7\ufe0f", "color": "#00505D"},
    "Summary": {"icon": "\U0001f4cb", "color": "#2E86C1"},
    "Body": {"icon": "\U0001f4dd", "color": "#27AE60"},
    "Tags": {"icon": "\U0001f3f7\ufe0f", "color": "#8E44AD"},
}


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
                Smart Writer
            </div>
            <style>.hero-title, .hero-title * {{ color: #FFFFFF !important; }}</style>
            <p style="color:rgba(255,255,255,0.75);font-size:0.95rem;margin:0.4rem 0 0 0;line-height:1.5;">
                Transform rough notes, emails, or ideas into polished, structured content.
                Articles, documentation, summaries — powered by AI.
            </p>
        </div>""",
        unsafe_allow_html=True,
    )

    if not AZURE_OPENAI_API_KEY:
        st.warning("AI features require an API key. Set AZURE_OPENAI_API_KEY in your .env file.")
        return

    # ── Step 1: Audience & Tone ──────────────────────────────
    _section_label("Step 1 \u2014 Who is reading this?", "Choose the audience and writing style")

    # Audience selector as cards
    st.markdown(
        '<p style="font-size:0.82rem;font-weight:600;color:#111111;margin:0 0 0.4rem 0;">Target Audience</p>',
        unsafe_allow_html=True,
    )
    audience_keys = list(AUDIENCES.keys())
    current_audience = st.session_state.get("kb_audience", audience_keys[0])
    aud_cols = st.columns(len(audience_keys))

    for col, aud in zip(aud_cols, audience_keys):
        with col:
            meta = AUDIENCE_META.get(aud, {})
            is_active = current_audience == aud
            if st.button(
                f"{meta.get('icon', '')} {aud}",
                key=f"aud_{aud}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state["kb_audience"] = aud
                st.rerun()

    # Show audience description
    aud_meta = AUDIENCE_META.get(current_audience, {})
    st.markdown(
        f'<div style="background:#F4F6F7;border-radius:6px;padding:0.6rem 1rem;margin:0.4rem 0 1rem 0;'
        f'font-size:0.82rem;color:#5D6D7E;border-left:3px solid {aud_meta.get("color", "#00505D")};">'
        f'<strong>{current_audience}</strong>: {aud_meta.get("hint", "")}</div>',
        unsafe_allow_html=True,
    )

    # Tone selector
    st.markdown(
        '<p style="font-size:0.82rem;font-weight:600;color:#111111;margin:0.5rem 0 0.4rem 0;">Writing Tone</p>',
        unsafe_allow_html=True,
    )
    tone_keys = list(TONES.keys())
    current_tone = st.session_state.get("kb_tone", tone_keys[0])
    tone_cols = st.columns(len(tone_keys))

    for col, tone in zip(tone_cols, tone_keys):
        with col:
            meta = TONE_META.get(tone, {})
            is_active = current_tone == tone
            if st.button(
                f"{meta.get('icon', '')} {tone}",
                key=f"tone_{tone}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state["kb_tone"] = tone
                st.rerun()

    # Show tone description
    tone_meta = TONE_META.get(current_tone, {})
    st.markdown(
        f'<div style="background:#F4F6F7;border-radius:6px;padding:0.6rem 1rem;margin:0.4rem 0 0.75rem 0;'
        f'font-size:0.82rem;color:#5D6D7E;border-left:3px solid #00505D;">'
        f'<strong>{current_tone}</strong>: {tone_meta.get("hint", "")}</div>',
        unsafe_allow_html=True,
    )

    # ── Step 2: Raw Input ────────────────────────────────────
    _section_label("Step 2 \u2014 Paste your raw content", "Notes, tickets, emails, meeting minutes \u2014 anything goes")

    # Privacy reminder
    st.markdown(
        '<div style="background:#FEF9E7;border-left:3px solid #F1C40F;border-radius:0 6px 6px 0;'
        'padding:0.5rem 0.75rem;font-size:0.78rem;color:#7D6608;margin:0 0 0.75rem 0;">'
        '\U0001f512 Remove sensitive information (names, ticket numbers) before publishing externally.</div>',
        unsafe_allow_html=True,
    )

    st.text_area(
        "Paste your notes or raw text",
        max_chars=KB_INPUT_MAX_CHARS,
        key="kb_input_text",
        height=200,
        placeholder="e.g., customer called about password reset, told them to go to settings > security > reset password, they needed to verify email first...",
        label_visibility="collapsed",
    )

    # Character counter
    current_text = st.session_state.get("kb_input_text", "")
    char_count = len(current_text)
    cc_color = "#C0392B" if char_count > KB_INPUT_MAX_CHARS * 0.9 else "#5D6D7E"
    st.markdown(
        f'<p style="text-align:right;font-size:0.75rem;color:{cc_color};margin:-0.5rem 0 0.5rem 0;">'
        f'{char_count:,} / {KB_INPUT_MAX_CHARS:,} characters</p>',
        unsafe_allow_html=True,
    )

    # Generate button
    gen_col, _ = st.columns([1, 3])
    with gen_col:
        generate_clicked = st.button("Generate Article", type="primary", use_container_width=True)

    if generate_clicked:
        user_input = current_text.strip()
        if not user_input:
            st.error("Please paste some text to generate an article from.")
            return

        with st.status("Writing your article...", expanded=True):
            try:
                client = get_client()
                context = build_kb_context(
                    st.session_state.get("kb_audience"),
                    st.session_state.get("kb_tone"),
                )
                format_rules = get_format_prompt("006")
                full_prompt = SYSTEM_PROMPT + context + format_rules
                from src.ai.client import stream_completion
                raw = stream_completion([
                    {"role": "system", "content": full_prompt},
                    {"role": "user", "content": user_input},
                ])
                result = normalize_markdown(ensure_sections("006", raw))
                st.session_state["kb_article_result"] = result
                st.session_state["kb_article_context"] = {
                    "audience": current_audience,
                    "tone": current_tone,
                }
            except OpenAIError as e:
                st.error(f"Generation failed: {e}")
                return
            except Exception as e:
                st.error(f"Generation timed out. Please try again. ({e})")
                return

    # ── Step 3: Results ──────────────────────────────────────
    result = st.session_state.get("kb_article_result")
    if result:
        _section_label("Step 3 \u2014 Generated Article", "Review, edit, then export")

        # Context badges
        ctx = st.session_state.get("kb_article_context", {})
        badges_html = ""
        if ctx.get("audience"):
            aud_m = AUDIENCE_META.get(ctx["audience"], {})
            badges_html += (
                f'<span style="display:inline-block;background:{aud_m.get("color", "#00505D")};color:#FFFFFF;'
                f'border-radius:20px;padding:0.25rem 0.75rem;margin:0 0.4rem 0.4rem 0;'
                f'font-size:0.75rem;font-weight:600;">{aud_m.get("icon", "")} {ctx["audience"]}</span>'
            )
        if ctx.get("tone"):
            tone_m = TONE_META.get(ctx["tone"], {})
            badges_html += (
                f'<span style="display:inline-block;background:#073350;color:#FFFFFF;'
                f'border-radius:20px;padding:0.25rem 0.75rem;margin:0 0.4rem 0.4rem 0;'
                f'font-size:0.75rem;font-weight:600;">{tone_m.get("icon", "")} {ctx["tone"]}</span>'
            )
        if badges_html:
            st.markdown(f'<div style="margin-bottom:0.75rem;">{badges_html}</div>', unsafe_allow_html=True)

        # Parse sections and render as cards with preview + editable
        sections = _parse_sections(result)

        # Render structured preview
        tab_preview, tab_edit = st.tabs(["Preview", "Edit & Export"])

        with tab_preview:
            for title, body in sections:
                meta = SECTION_META.get(title, {"icon": "\U0001f4cb", "color": "#00505D"})
                accent = meta["color"]
                icon = meta["icon"]

                if title == "Tags" and body:
                    # Render tags as pills
                    tags = [t.strip() for t in body.replace("\n", ",").split(",") if t.strip()]
                    tags_html = ""
                    for tag in tags:
                        tags_html += (
                            f'<span style="display:inline-block;background:#F4F6F7;color:#5D6D7E;'
                            f'border:1px solid #E0E4E8;border-radius:20px;padding:0.2rem 0.7rem;'
                            f'font-size:0.75rem;margin:0.2rem 0.3rem 0.2rem 0;">{tag}</span>'
                        )
                    st.markdown(
                        f"""<div style="
                            background:#FFFFFF;border:1px solid #E0E4E8;border-left:4px solid {accent};
                            border-radius:8px;padding:1rem 1.25rem;margin-bottom:0.75rem;
                            box-shadow:0 1px 6px rgba(0,0,0,0.03);
                        ">
                            <div style="display:flex;align-items:center;margin-bottom:0.5rem;">
                                <span style="font-size:1.1rem;margin-right:0.5rem;">{icon}</span>
                                <span style="font-size:0.9rem;font-weight:700;color:{accent};">{title}</span>
                            </div>
                            <div>{tags_html}</div>
                        </div>""",
                        unsafe_allow_html=True,
                    )
                elif title == "Title" and body:
                    # Render title prominently
                    clean_title = body.strip().lstrip("#").strip()
                    st.markdown(
                        f"""<div style="
                            background:#FFFFFF;border:1px solid #E0E4E8;border-left:4px solid {accent};
                            border-radius:8px;padding:1rem 1.25rem;margin-bottom:0.75rem;
                            box-shadow:0 1px 6px rgba(0,0,0,0.03);
                        ">
                            <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em;
                                color:{accent};font-weight:700;margin-bottom:0.3rem;">{icon} Article Title</div>
                            <div style="font-size:1.2rem;font-weight:700;color:#111111;">{clean_title}</div>
                        </div>""",
                        unsafe_allow_html=True,
                    )
                else:
                    # Standard section card
                    st.markdown(
                        f"""<div style="
                            background:#FFFFFF;border:1px solid #E0E4E8;border-left:4px solid {accent};
                            border-radius:8px;padding:1rem 1.25rem;margin-bottom:0.75rem;
                            box-shadow:0 1px 6px rgba(0,0,0,0.03);
                        ">
                            <div style="display:flex;align-items:center;margin-bottom:0.5rem;">
                                <span style="font-size:1.1rem;margin-right:0.5rem;">{icon}</span>
                                <span style="font-size:0.9rem;font-weight:700;color:{accent};">{title}</span>
                            </div>
                        </div>""",
                        unsafe_allow_html=True,
                    )
                    st.markdown(body)

            # Copy from preview
            render_copy_button(result, label="Copy Article")

        with tab_edit:
            edited = st.text_area(
                "Edit the generated article",
                value=result,
                height=400,
                label_visibility="collapsed",
                key="kb_article_edit_area",
            )

            ec1, ec2 = st.columns(2)
            with ec1:
                render_copy_button(edited)
            with ec2:
                render_download_button(edited, "kb-article")

