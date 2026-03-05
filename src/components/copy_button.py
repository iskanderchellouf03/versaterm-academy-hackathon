import streamlit as st
import streamlit.components.v1 as components
import html


def render_copy_button(text, label="Copy"):
    escaped = html.escape(text).replace("`", "\\`").replace("${", "\\${")
    html_content = f"""
    <button id="copyBtn" style="
        background-color: #00505D;
        color: white;
        border: none;
        padding: 6px 16px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
    " onclick="copyToClipboard()">
        {label}
    </button>
    <script>
    function copyToClipboard() {{
        const text = `{escaped}`;
        try {{
            navigator.clipboard.writeText(text).then(() => {{
                document.getElementById('copyBtn').innerText = 'Copied!';
                setTimeout(() => {{
                    document.getElementById('copyBtn').innerText = '{label}';
                }}, 2000);
            }});
        }} catch (e) {{
            document.getElementById('copyBtn').innerText = 'Unable to copy. Please select the text and copy manually (Ctrl+C).';
            setTimeout(() => {{
                document.getElementById('copyBtn').innerText = '{label}';
            }}, 3000);
        }}
    }}
    </script>
    """
    components.html(html_content, height=40)


def render_sections_with_copy(markdown_text):
    if not markdown_text:
        return []

    # Split on \n## to extract sections
    parts = markdown_text.split("\n## ")
    sections = []

    for i, part in enumerate(parts):
        if i == 0:
            # First part may or may not have a ## prefix
            if part.startswith("## "):
                section = part[3:]
            else:
                section = part
            if section.strip():
                sections.append("## " + section if not part.startswith("## ") else part)
        else:
            sections.append("## " + part)

    for section in sections:
        st.markdown(section)
        render_copy_button(section, label="Copy section")

    return sections
