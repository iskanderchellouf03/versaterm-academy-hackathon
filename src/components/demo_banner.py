import streamlit as st
from src.config import DEMO_BANNER_TEXT


def render_demo_banner():
    if st.session_state.get("banner_dismissed", False):
        return

    st.markdown(
        f"""
        <div id="demo-banner" style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #F39C12;
            color: #1A1A1A;
            text-align: center;
            padding: 8px 16px;
            z-index: 999;
            font-size: 14px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        ">
            {DEMO_BANNER_TEXT}
        </div>
        <style>
            .stApp {{
                padding-top: 45px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
