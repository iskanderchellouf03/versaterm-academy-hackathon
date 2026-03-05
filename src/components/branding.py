import os
import base64
from functools import lru_cache
import streamlit as st
from src.config import BRAND_LOGO_PATH, BRAND_LOGO_WHITE_PATH, BRAND_TITLE, BRAND_SUBTITLE


@lru_cache(maxsize=4)
def _logo_b64(path):
    if not os.path.exists(path):
        return None
    if path.endswith(".svg"):
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
        return base64.b64encode(data.encode("utf-8")).decode("utf-8")
    else:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("utf-8")


def render_branding(show_subtitle=True, dark_bg=False):
    logo_path = BRAND_LOGO_WHITE_PATH if dark_bg else BRAND_LOGO_PATH
    width = 140 if show_subtitle else 100

    b64 = _logo_b64(logo_path)
    if b64:
        mime = "image/svg+xml" if logo_path.endswith(".svg") else "image/png"
        st.markdown(
            f'<img src="data:{mime};base64,{b64}" width="{width}" />',
            unsafe_allow_html=True,
        )

    if show_subtitle:
        st.caption(BRAND_SUBTITLE)
