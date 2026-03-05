import streamlit as st
from datetime import date


def render_download_button(text, module_slug):
    filename = f"{module_slug}-{date.today().isoformat()}.md"
    st.download_button(
        label="Download",
        data=text,
        file_name=filename,
        mime="text/markdown",
    )
