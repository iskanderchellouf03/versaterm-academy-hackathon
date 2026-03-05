import os
import re
import base64

import streamlit as st
from openai import OpenAIError

from src.ai.client import get_client
from src.ai.prompts.onboarding_planner import SYSTEM_PROMPT, build_focus_context
from src.config import (
    AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT, EXPERIENCE_LEVELS,
    ACCEPTED_TYPES, MAX_FILE_SIZE_MB, CHUNK_SIZE,
    BRAND_LOGO_WHITE_PATH, BRAND_LOGO_PATH,
    COMPANY_PRODUCTS,
)
from src.docs.retriever import retrieve_top_k
from src.components.copy_button import render_copy_button
from src.components.download_button import render_download_button
from src.output.prompt import get_format_prompt
from src.output.normalizer import ensure_sections, normalize_markdown
from src.docs.extractor import extract_text

CV_EXTRACT_PROMPT = """Analyze this CV/resume and extract the following in a structured format. Be concise.

## Candidate Summary
- **Name**: (full name)
- **Current/Target Role**: (most recent or target job title)
- **Experience Level**: (one of: Beginner = 0-2 years, Intermediate = 2-5 years, Advanced = 5+ years)
- **Years of Experience**: (total relevant years)

## Key Skills
- List the top 8-10 technical and domain skills

## Relevant Experience
- Summarize the 2-3 most relevant positions (1 sentence each)

## Suggested Focus Areas
- Based on skill gaps or growth areas visible in the CV, suggest 3-5 onboarding focus topics

CV Text:
"""


# ─── Helpers ───────────────────────────────────────────────

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


def _extract_cv_text(uploaded_file):
    file_type = uploaded_file.name.rsplit(".", 1)[-1].lower()
    chunks = extract_text(uploaded_file.getvalue(), file_type)
    if not chunks:
        return ""
    return "\n".join(c["text"] for c in chunks)


def _analyze_cv(cv_text):
    client = get_client()
    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": "You are an HR assistant that extracts structured information from CVs/resumes. Be concise and factual."},
            {"role": "user", "content": CV_EXTRACT_PROMPT + cv_text},
        ],
    )
    return response.choices[0].message.content


def _infer_experience_level(analysis_text):
    text_lower = analysis_text.lower()
    if "advanced" in text_lower and "experience level" in text_lower:
        return "Advanced"
    if "intermediate" in text_lower and "experience level" in text_lower:
        return "Intermediate"
    return "Beginner"


def _get_product_docs_key(company, product):
    """Session state key for a product's knowledge base."""
    return f"product_kb_{company}_{product}"


def _get_product_docs(company, product):
    """Get uploaded docs for a specific product."""
    key = _get_product_docs_key(company, product)
    return st.session_state.get(key, [])


def _add_product_doc(company, product, filename, file_type, size, chunks):
    """Add a document to a product's knowledge base."""
    key = _get_product_docs_key(company, product)
    docs = st.session_state.get(key, [])
    # Avoid duplicates
    existing = [d["filename"] for d in docs if d.get("active", True)]
    if filename in existing:
        return None
    docs.append({
        "filename": filename,
        "type": file_type,
        "size": size,
        "chunks": chunks,
        "active": True,
    })
    st.session_state[key] = docs
    return None


def _remove_product_doc(company, product, filename):
    """Remove a document from a product's knowledge base."""
    key = _get_product_docs_key(company, product)
    docs = st.session_state.get(key, [])
    for doc in docs:
        if doc["filename"] == filename:
            doc["active"] = False
    st.session_state[key] = docs


def _build_product_context(company, product, role):
    """Retrieve relevant chunks from product docs and format as context."""
    docs = _get_product_docs(company, product)
    active = [d for d in docs if d.get("active", True)]
    if not active:
        return ""

    query = f"{product} {role} onboarding features workflows"
    chunks = retrieve_top_k(query, active, k=5)
    if not chunks:
        return ""

    formatted = []
    for chunk in chunks:
        source = chunk["source"]
        page = chunk.get("page")
        header = f"[{source}, p.{page}]" if page else f"[{source}]"
        formatted.append(f"{header}\n{chunk['text']}")

    refs = "\n\n".join(formatted)
    return (
        f"\n\n--- Product Documentation for {product} ({company}) ---\n"
        f"{refs}\n"
        f"--- End Product Documentation ---\n\n"
        f"Use the product documentation above to make the onboarding plan specific and accurate. "
        f"Reference actual product features, workflows, terminology, and capabilities from the docs. "
        f"Incorporate product-specific tasks and learning activities into the day-by-day schedule."
    )


def _find_section(sections, keywords):
    """Find a section by fuzzy keyword matching."""
    for key, content in sections.items():
        key_lower = key.lower()
        if any(kw in key_lower for kw in keywords):
            return content
    return ""


def _parse_cv_structured(analysis_text):
    """Parse CV analysis into structured sections."""
    data = {
        "metrics": {},
        "skills": [],
        "experience": [],
        "focus_areas": [],
    }

    # Split into sections by ## headings
    sections = {}
    current_key = None
    current_lines = []
    for line in analysis_text.split("\n"):
        heading_match = re.match(r"^#{1,3}\s+(.+)$", line.strip())
        if heading_match:
            if current_key:
                sections[current_key] = "\n".join(current_lines).strip()
            current_key = heading_match.group(1).strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_key:
        sections[current_key] = "\n".join(current_lines).strip()

    # Parse metrics from candidate summary (also scan full text as fallback)
    summary = _find_section(sections, ["summary", "candidate", "profile", "overview"])
    # If no summary section found, scan entire text for metric lines
    scan_text = summary if summary else analysis_text
    for line in scan_text.split("\n"):
        line_lower = line.lower().strip()
        if ":" not in line:
            continue
        val = line.split(":", 1)[-1].strip().strip("*- ")
        if not val:
            continue
        if ("name" in line_lower) and ("**" in line) and "name" not in data["metrics"]:
            data["metrics"]["name"] = val
        elif ("role" in line_lower or "title" in line_lower or "position" in line_lower) and "**" in line and "role" not in data["metrics"]:
            data["metrics"]["role"] = val
        elif ("experience level" in line_lower or "level" in line_lower) and "**" in line and "level" not in data["metrics"]:
            # Avoid matching lines that are just listing items
            if any(lvl in val.lower() for lvl in ["beginner", "intermediate", "advanced", "junior", "senior", "mid"]):
                data["metrics"]["level"] = val
        elif ("years" in line_lower) and "**" in line and "years" not in data["metrics"]:
            data["metrics"]["years"] = val

    # Parse skills
    skills_text = _find_section(sections, ["skill", "competenc", "technolog", "expertise"])
    for line in skills_text.split("\n"):
        line = line.strip().lstrip("-*").strip()
        # Remove numbered prefixes like "1. "
        line = re.sub(r"^\d+\.\s*", "", line).strip()
        if line and len(line) > 1:
            data["skills"].append(line)

    # Parse experience
    exp_text = _find_section(sections, ["experience", "work history", "employment", "position"])
    for line in exp_text.split("\n"):
        line = line.strip().lstrip("-*").strip()
        line = re.sub(r"^\d+\.\s*", "", line).strip()
        if line and len(line) > 1:
            data["experience"].append(line)

    # Parse focus areas
    focus_text = _find_section(sections, ["focus", "recommend", "gap", "development", "improvement", "suggestion"])
    for line in focus_text.split("\n"):
        line = line.strip().lstrip("-*").strip()
        line = re.sub(r"^\d+\.\s*", "", line).strip()
        if line and len(line) > 1:
            data["focus_areas"].append(line)

    return data


def _render_cv_analysis(cv_analysis):
    """Render a modern, card-based CV analysis view."""
    data = _parse_cv_structured(cv_analysis)
    metrics = data["metrics"]
    skills = data["skills"]
    experience = data["experience"]
    focus_areas = data["focus_areas"]

    has_structured = metrics or skills or experience or focus_areas

    # ── Header ──
    st.markdown(
        '<div style="border-left: 4px solid #00505D; padding: 0.5rem 1rem; margin: 0.75rem 0; '
        'background: #F4F6F7; border-radius: 0 8px 8px 0;">'
        '<span style="font-size: 1rem; color: #111111; font-weight: 600;">CV Analysis Results</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    # If parsing failed, show the raw analysis in a nice card and return
    if not has_structured:
        st.markdown(
            """<div style="
                background: #FFFFFF;
                border: 1px solid #E0E4E8;
                border-radius: 10px;
                padding: 1.25rem 1.5rem;
                box-shadow: 0 1px 6px rgba(0,0,0,0.03);
            ">""",
            unsafe_allow_html=True,
        )
        st.markdown(cv_analysis)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    if metrics:
        metric_cols = st.columns(len(metrics))
        labels_map = {"name": "Candidate", "role": "Current Role", "level": "Level", "years": "Experience"}
        colors = {"name": "#073350", "role": "#00505D", "level": "#2E86C1", "years": "#148F77"}
        for col, (key, value) in zip(metric_cols, metrics.items()):
            accent = colors.get(key, "#00505D")
            with col:
                st.markdown(
                    f"""<div style="
                        background: #FFFFFF;
                        border: 1px solid #E0E4E8;
                        border-left: 4px solid {accent};
                        border-radius: 8px;
                        padding: 0.85rem 1rem;
                        box-shadow: 0 1px 6px rgba(0,0,0,0.03);
                    ">
                        <p style="font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.1em; color: #5D6D7E; margin: 0 0 0.3rem 0; font-weight: 600;">
                            {labels_map.get(key, key)}
                        </p>
                        <p style="font-size: 1rem; color: #111111; margin: 0; font-weight: 700; line-height: 1.3;">
                            {value}
                        </p>
                    </div>""",
                    unsafe_allow_html=True,
                )

    st.markdown('<div style="height: 0.75rem;"></div>', unsafe_allow_html=True)

    # ── Skills + Focus Areas side by side ──
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(
            '<p style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; '
            'color: #5D6D7E; font-weight: 600; margin: 0 0 0.5rem 0;">Key Skills</p>',
            unsafe_allow_html=True,
        )
        if skills:
            pills_html = " ".join(
                f'<span style="display:inline-block; background:#E8F6F3; color:#00505D; '
                f'font-size:0.78rem; font-weight:500; padding:0.3rem 0.7rem; border-radius:20px; '
                f'margin:0.2rem 0.15rem; border:1px solid rgba(0,80,93,0.15);">{s}</span>'
                for s in skills
            )
            st.markdown(
                f'<div style="background:#FFFFFF; border:1px solid #E0E4E8; border-radius:10px; '
                f'padding:1rem 1.25rem; box-shadow:0 1px 6px rgba(0,0,0,0.03); min-height:120px;">'
                f'{pills_html}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.caption("No skills extracted.")

    with col_right:
        st.markdown(
            '<p style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; '
            'color: #5D6D7E; font-weight: 600; margin: 0 0 0.5rem 0;">Suggested Focus Areas</p>',
            unsafe_allow_html=True,
        )
        if focus_areas:
            focus_items = ""
            for fa in focus_areas:
                focus_items += (
                    f'<div style="display:flex; align-items:flex-start; gap:0.5rem; margin-bottom:0.5rem;">'
                    f'<div style="min-width:6px; width:6px; height:6px; border-radius:50%; background:#00505D; margin-top:0.45rem;"></div>'
                    f'<span style="font-size:0.85rem; color:#111111; line-height:1.45;">{fa}</span>'
                    f'</div>'
                )
            st.markdown(
                f'<div style="background:#FFFFFF; border:1px solid #E0E4E8; border-radius:10px; '
                f'padding:1rem 1.25rem; box-shadow:0 1px 6px rgba(0,0,0,0.03); min-height:120px;">'
                f'{focus_items}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.caption("No focus areas extracted.")

    st.markdown('<div style="height: 0.75rem;"></div>', unsafe_allow_html=True)

    # ── Experience timeline ──
    if experience:
        st.markdown(
            '<p style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; '
            'color: #5D6D7E; font-weight: 600; margin: 0 0 0.5rem 0;">Relevant Experience</p>',
            unsafe_allow_html=True,
        )
        exp_cards = ""
        for i, exp in enumerate(experience):
            border_style = "border-left: 3px solid #00505D;" if i == 0 else "border-left: 3px solid #E0E4E8;"
            exp_cards += (
                f'<div style="background:#FFFFFF; border:1px solid #E0E4E8; {border_style} '
                f'border-radius:8px; padding:0.85rem 1.15rem; margin-bottom:0.5rem; '
                f'box-shadow:0 1px 4px rgba(0,0,0,0.02);">'
                f'<p style="font-size:0.85rem; color:#111111; margin:0; line-height:1.5;">{exp}</p>'
                f'</div>'
            )
        st.markdown(exp_cards, unsafe_allow_html=True)

    # ── Raw analysis toggle ──
    with st.expander("View raw analysis", expanded=False):
        st.markdown(cv_analysis)


def _split_plan_sections(result_text):
    """Split the generated plan into named sections based on ## headings."""
    sections = {}
    current_key = None
    current_lines = []

    for line in result_text.split("\n"):
        heading_match = re.match(r"^##\s+(.+)$", line.strip())
        if heading_match:
            if current_key:
                sections[current_key] = "\n".join(current_lines).strip()
            current_key = heading_match.group(1).strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_key:
        sections[current_key] = "\n".join(current_lines).strip()

    return sections


def _step_indicator(steps, current_step):
    """Render a horizontal step progress bar."""
    items = []
    for i, (label, _) in enumerate(steps):
        step_num = i + 1
        if step_num < current_step:
            # Completed
            items.append(
                f'<div style="display:flex; align-items:center; gap:0.4rem;">'
                f'<div style="width:28px; height:28px; border-radius:50%; background:#00505D; color:#fff; '
                f'display:flex; align-items:center; justify-content:center; font-size:0.8rem; font-weight:700;">&#10003;</div>'
                f'<span style="font-size:0.82rem; color:#00505D; font-weight:600;">{label}</span>'
                f'</div>'
            )
        elif step_num == current_step:
            # Active
            items.append(
                f'<div style="display:flex; align-items:center; gap:0.4rem;">'
                f'<div style="width:28px; height:28px; border-radius:50%; background:#00505D; color:#fff; '
                f'display:flex; align-items:center; justify-content:center; font-size:0.8rem; font-weight:700;">{step_num}</div>'
                f'<span style="font-size:0.82rem; color:#00505D; font-weight:600;">{label}</span>'
                f'</div>'
            )
        else:
            # Upcoming
            items.append(
                f'<div style="display:flex; align-items:center; gap:0.4rem;">'
                f'<div style="width:28px; height:28px; border-radius:50%; background:#E0E4E8; color:#5D6D7E; '
                f'display:flex; align-items:center; justify-content:center; font-size:0.8rem; font-weight:600;">{step_num}</div>'
                f'<span style="font-size:0.82rem; color:#5D6D7E;">{label}</span>'
                f'</div>'
            )

    # Connector lines between steps
    html_items = []
    for i, item in enumerate(items):
        html_items.append(item)
        if i < len(items) - 1:
            html_items.append(
                '<div style="flex:1; height:2px; background:#E0E4E8; margin:0 0.25rem;"></div>'
            )

    st.markdown(
        f"""<div style="
            display: flex;
            align-items: center;
            padding: 0.75rem 1.25rem;
            background: #FFFFFF;
            border: 1px solid #E0E4E8;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 6px rgba(0,0,0,0.03);
        ">{''.join(html_items)}</div>""",
        unsafe_allow_html=True,
    )


# ─── Main render ───────────────────────────────────────────

def render():
    # --- Page Header ---
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
            <div class="hero-title" style="margin: 0; font-size: 1.75rem; font-weight: 700;">
                Onboarding Plan Generator
            </div>
            <style>.hero-title, .hero-title * {{ color: #FFFFFF !important; }}</style>
            <p style="color: rgba(255,255,255,0.75); font-size: 0.95rem; margin: 0.4rem 0 0 0; line-height: 1.5;">
                Create customized 2-week onboarding plans for new team members.
                Upload a CV to personalize the plan based on the candidate's actual skills and experience.
            </p>
        </div>""",
        unsafe_allow_html=True,
    )

    if not AZURE_OPENAI_API_KEY:
        st.warning("AI features require an API key. Set AZURE_OPENAI_API_KEY in your .env file.")
        return

    # Determine current step
    has_cv = bool(st.session_state.get("onb_cv_analysis"))
    has_result = bool(st.session_state.get("onb_plan_result"))
    if has_result:
        current_step = 3
    elif has_cv:
        current_step = 2
    else:
        current_step = 1

    steps = [
        ("Upload CV", "Upload a candidate resume"),
        ("Configure", "Set role, product, and level"),
        ("Generate", "View the onboarding plan"),
    ]
    _step_indicator(steps, current_step)

    # =============================================
    # STEP 1: CV Upload
    # =============================================
    with st.container(border=True):
        st.markdown(
            '<p style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; '
            'color: #5D6D7E; font-weight: 600; margin: 0 0 0.25rem 0;">Step 1</p>',
            unsafe_allow_html=True,
        )
        st.markdown("**Candidate CV** (optional)")
        st.caption("Upload a resume to auto-extract role, skills, and experience.")

        cv_file = st.file_uploader(
            "Upload CV",
            type=ACCEPTED_TYPES,
            key="onb_cv_upload",
            label_visibility="collapsed",
        )

        # Reset analysis flag if a different file was uploaded
        prev_cv_name = st.session_state.get("onb_cv_filename")
        if cv_file and cv_file.name != prev_cv_name:
            st.session_state["onb_cv_analyzed"] = False
            st.session_state["onb_cv_filename"] = cv_file.name
        elif not cv_file and prev_cv_name:
            # File was removed
            st.session_state.pop("onb_cv_analyzed", None)
            st.session_state.pop("onb_cv_filename", None)
            st.session_state.pop("onb_cv_analysis", None)
            st.session_state.pop("onb_cv_text", None)
            st.session_state.pop("onb_cv_level", None)

        if cv_file and not st.session_state.get("onb_cv_analyzed"):
            if cv_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
                st.error(f"File exceeds {MAX_FILE_SIZE_MB} MB limit.")
            else:
                with st.spinner("Reading and analyzing CV..."):
                    try:
                        cv_text = _extract_cv_text(cv_file)
                        if not cv_text:
                            st.warning("Could not extract text from file.")
                        else:
                            analysis = _analyze_cv(cv_text)
                            st.session_state["onb_cv_analyzed"] = True
                            st.session_state["onb_cv_analysis"] = analysis
                            st.session_state["onb_cv_text"] = cv_text
                            st.session_state["onb_cv_level"] = _infer_experience_level(analysis)
                            st.rerun()
                    except OpenAIError as e:
                        st.error(f"CV analysis failed: {e}")
                    except Exception as e:
                        st.error(f"Failed to process CV: {e}")

    # CV Analysis results
    cv_analysis = st.session_state.get("onb_cv_analysis")
    if cv_analysis:
        _render_cv_analysis(cv_analysis)

        inferred_level = st.session_state.get("onb_cv_level", "Beginner")
        level_idx = EXPERIENCE_LEVELS.index(inferred_level) if inferred_level in EXPERIENCE_LEVELS else 0
    else:
        level_idx = 0

    # =============================================
    # STEP 2: Plan Configuration
    # =============================================
    with st.container(border=True):
        st.markdown(
            '<p style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; '
            'color: #5D6D7E; font-weight: 600; margin: 0 0 0.25rem 0;">Step 2</p>',
            unsafe_allow_html=True,
        )
        st.markdown("**Plan Configuration**")
        st.caption("Select the company and product the new hire will be working on.")

        # Company → Product dynamic selection
        company_names = list(COMPANY_PRODUCTS.keys())
        col_co, col_pr = st.columns(2)
        with col_co:
            company = st.selectbox("Company", company_names, key="onb_company")
        with col_pr:
            products = COMPANY_PRODUCTS.get(company, [])
            if products:
                product = st.selectbox("Product", products, key="onb_product_select")
            else:
                product = st.text_input("Product", key="onb_product", placeholder="e.g., Main Platform")

        # Product Knowledge Base upload
        product_name = product if isinstance(product, str) and product.strip() else ""
        if product_name:
            existing_docs = [d for d in _get_product_docs(company, product_name) if d.get("active", True)]
            total_chunks = sum(len(d.get("chunks", [])) for d in existing_docs)

            st.markdown(
                f'<div style="border-left: 3px solid #00505D; padding: 0.4rem 0.75rem; margin: 0.75rem 0 0.5rem 0; '
                f'background: #F4F6F7; border-radius: 0 6px 6px 0;">'
                f'<span style="font-size: 0.85rem; color: #111111; font-weight: 600;">Product Documentation</span>'
                f'<span style="font-size: 0.78rem; color: #5D6D7E; margin-left: 0.5rem;">'
                f'Upload technical docs about <strong>{product_name}</strong> to improve plan accuracy</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

            product_files = st.file_uploader(
                f"Upload {product_name} docs",
                type=ACCEPTED_TYPES,
                accept_multiple_files=True,
                key=f"onb_product_docs_{company}_{product_name}",
                label_visibility="collapsed",
            )

            if product_files:
                for f in product_files:
                    existing_names = [d["filename"] for d in existing_docs]
                    if f.name in existing_names:
                        continue
                    if f.size > MAX_FILE_SIZE_MB * 1024 * 1024:
                        st.error(f"{f.name} exceeds {MAX_FILE_SIZE_MB} MB limit.")
                        continue
                    file_type = f.name.rsplit(".", 1)[-1].lower()
                    chunks = extract_text(f.getvalue(), file_type)
                    if not chunks:
                        st.warning(f"Could not extract text from {f.name}.")
                        continue
                    _add_product_doc(company, product_name, f.name, file_type, f.size, chunks)
                    st.rerun()

            # Show loaded docs
            existing_docs = [d for d in _get_product_docs(company, product_name) if d.get("active", True)]
            if existing_docs:
                total_chunks = sum(len(d.get("chunks", [])) for d in existing_docs)
                st.markdown(
                    f'<p style="font-size: 0.78rem; color: #00505D; font-weight: 600; margin: 0.25rem 0 0.5rem 0;">'
                    f'{len(existing_docs)} doc(s) loaded &middot; {total_chunks} chunks &middot; '
                    f'Will be used as context for plan generation</p>',
                    unsafe_allow_html=True,
                )
                for doc in existing_docs:
                    dc1, dc2 = st.columns([0.8, 0.2])
                    with dc1:
                        size = doc["size"]
                        size_str = f"{size / (1024*1024):.1f} MB" if size >= 1024*1024 else f"{size / 1024:.1f} KB"
                        st.caption(f"{doc['filename']} ({size_str}, {len(doc['chunks'])} chunks)")
                    with dc2:
                        if st.button("Remove", key=f"rm_pdoc_{doc['filename']}", type="secondary"):
                            _remove_product_doc(company, product_name, doc["filename"])
                            st.rerun()

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Role", key="onb_role", placeholder="e.g., Support Analyst, QA Engineer")
        with col2:
            st.selectbox("Experience Level", EXPERIENCE_LEVELS, index=level_idx, key="onb_level")

        st.text_area(
            "Focus notes (optional)",
            max_chars=1000,
            key="onb_focus_notes",
            placeholder="e.g., safety-critical workflows, compliance reporting",
            height=100,
        )

    st.markdown('<div style="height: 0.25rem;"></div>', unsafe_allow_html=True)

    if st.button("Generate Onboarding Plan", type="primary", use_container_width=True):
        role = st.session_state.get("onb_role", "").strip()
        company = st.session_state.get("onb_company", "")
        # Get product from either selectbox or text input
        product = st.session_state.get("onb_product_select", "") or st.session_state.get("onb_product", "")
        product = product.strip()
        level = st.session_state.get("onb_level", "Beginner")

        missing = []
        if not role:
            missing.append("Role")
        if not product:
            missing.append("Product")
        if missing:
            st.error(f"Please fill in: {', '.join(missing)}")
            return

        user_message = f"Company: {company}\nProduct: {product}\nRole: {role}\nExperience Level: {level}"
        focus_notes = st.session_state.get("onb_focus_notes", "")
        focus_context = build_focus_context(focus_notes)
        format_rules = get_format_prompt("008")
        full_prompt = SYSTEM_PROMPT + focus_context + format_rules

        cv_context = ""
        cv_text = st.session_state.get("onb_cv_text", "")
        if cv_text:
            cv_analysis_text = st.session_state.get("onb_cv_analysis", "")
            cv_context = (
                "\n\n--- Candidate CV Analysis ---\n"
                f"{cv_analysis_text}\n"
                "--- End CV Analysis ---\n\n"
                "Use the candidate's actual skills, experience, and background above to personalize the onboarding plan. "
                "Identify skill gaps relative to the role and prioritize those in the learning plan. "
                "Leverage their existing strengths to accelerate relevant sections."
            )

        # Build product documentation context
        product_context = _build_product_context(company, product, role)

        with st.status("Generating onboarding plan...", expanded=True):
            try:
                client = get_client()
                from src.ai.client import stream_completion
                raw = stream_completion([
                    {"role": "system", "content": full_prompt},
                    {"role": "user", "content": user_message + cv_context + product_context},
                ])
                result = normalize_markdown(ensure_sections("008", raw))
                st.session_state["onb_plan_result"] = result
                st.rerun()
            except OpenAIError as e:
                st.error(f"Generation failed: {e}")
                return
            except Exception as e:
                st.error(f"Generation timed out. Please try again. ({e})")
                return

    # =============================================
    # STEP 3: Results
    # =============================================
    result = st.session_state.get("onb_plan_result")
    if result:
        st.markdown(
            '<div style="border-left: 4px solid #00505D; padding: 0.75rem 1rem; margin: 1.5rem 0 1rem 0; '
            'background: #F4F6F7; border-radius: 0 8px 8px 0;">'
            '<p style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; '
            'color: #5D6D7E; font-weight: 600; margin: 0 0 0.15rem 0;">Step 3</p>'
            '<span style="font-size: 1.1rem; color: #111111; font-weight: 600;">Generated Onboarding Plan</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        if cv_analysis:
            st.markdown(
                '<p style="display: inline-block; background: #E8F6F3; color: #00505D; '
                'font-size: 0.78rem; font-weight: 600; padding: 0.3rem 0.75rem; border-radius: 20px; '
                'margin: 0 0 0.75rem 0;">'
                'Personalized from candidate CV</p>',
                unsafe_allow_html=True,
            )

        # Check if product docs were used
        res_company = st.session_state.get("onb_company", "")
        res_product = st.session_state.get("onb_product_select", "") or st.session_state.get("onb_product", "")
        if res_product and _get_product_docs(res_company, res_product.strip()):
            active_pdocs = [d for d in _get_product_docs(res_company, res_product.strip()) if d.get("active", True)]
            if active_pdocs:
                st.markdown(
                    f'<p style="display: inline-block; background: #EBF5FB; color: #2E86C1; '
                    f'font-size: 0.78rem; font-weight: 600; padding: 0.3rem 0.75rem; border-radius: 20px; '
                    f'margin: 0 0 0.75rem 0.5rem;">'
                    f'Grounded with {len(active_pdocs)} product doc(s)</p>',
                    unsafe_allow_html=True,
                )

        # Action buttons
        col_a, col_b = st.columns(2)
        with col_a:
            render_copy_button(result)
        with col_b:
            render_download_button(result, "onboarding-plan")

        # Split into sections and render as tabs
        sections = _split_plan_sections(result)

        if len(sections) >= 3:
            # Map sections to tab names
            tab_map = {
                "Overview": [],
                "Learning Plan": [],
                "Checkpoints": [],
            }

            for title, content in sections.items():
                title_lower = title.lower()
                if "learning plan" in title_lower or "week" in title_lower:
                    tab_map["Learning Plan"].append((title, content))
                elif "checkpoint" in title_lower or "assessment" in title_lower:
                    tab_map["Checkpoints"].append((title, content))
                else:
                    tab_map["Overview"].append((title, content))

            tab_names = [k for k in tab_map if tab_map[k]]
            if tab_names:
                tabs = st.tabs(tab_names)
                for tab, name in zip(tabs, tab_names):
                    with tab:
                        for title, content in tab_map[name]:
                            st.markdown(
                                f"""<div style="
                                    background: #FFFFFF;
                                    border: 1px solid #E0E4E8;
                                    border-radius: 10px;
                                    padding: 1.25rem 1.5rem;
                                    margin-bottom: 0.75rem;
                                    box-shadow: 0 1px 6px rgba(0,0,0,0.03);
                                ">
                                    <p style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.08em; color: #00505D; margin: 0 0 0.5rem 0; font-weight: 700;">
                                        {title}
                                    </p>
                                </div>""",
                                unsafe_allow_html=True,
                            )
                            st.markdown(content)
            else:
                # Fallback: render as one block
                st.markdown(result)
        else:
            st.markdown(result)

        # Full plan in expander for quick copy
        with st.expander("View full plan (raw)", expanded=False):
            st.markdown(result)

