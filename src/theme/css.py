import streamlit as st
from functools import lru_cache
from src.config import (
    BRAND_PRIMARY_COLOR,
    BRAND_PRIMARY_HOVER,
    BRAND_SIDEBAR_BG,
    BRAND_SIDEBAR_TEXT,
    BRAND_TEXT_COLOR,
)


@lru_cache(maxsize=1)
def _build_theme_css():
    return f"""
        <style>
            /* === Main content top padding === */
            .stMainBlockContainer {{
                padding-top: 1rem !important;
            }}

            /* === Sidebar === */
            [data-testid="stSidebar"] {{
                background: linear-gradient(180deg, {BRAND_SIDEBAR_BG} 0%, #0a2540 100%);
                border-right: 1px solid rgba(255,255,255,0.06) !important;
            }}
            [data-testid="stSidebar"] * {{
                color: {BRAND_SIDEBAR_TEXT} !important;
            }}
            [data-testid="stSidebar"] hr {{
                border-color: rgba(236,240,241,0.08) !important;
                margin: 0.4rem 0 !important;
            }}
            /* Kill ALL top spacing inside sidebar */
            [data-testid="stSidebar"] > div {{
                padding-top: 0 !important;
                margin-top: 0 !important;
            }}
            [data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
                padding: 1.25rem 1rem 1rem 1rem !important;
                margin-top: 0 !important;
            }}
            /* Sidebar collapse button positioning */
            [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {{
                position: absolute !important;
                top: 0.75rem !important;
                right: 0.75rem !important;
                z-index: 10 !important;
            }}
            /* Sidebar vertical spacing between elements */
            [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
                gap: 0.75rem !important;
            }}

            /* === Sidebar Nav Buttons (secondary = inactive, primary = active) === */
            [data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-secondary"] {{
                background-color: transparent !important;
                border: none !important;
                border-left: 3px solid transparent !important;
                border-radius: 8px !important;
                color: {BRAND_SIDEBAR_TEXT} !important;
                font-weight: 500 !important;
                font-size: 0.85rem !important;
                transition: all 0.2s ease !important;
                padding: 0.5rem 0.75rem !important;
                letter-spacing: 0.01em !important;
                opacity: 0.75 !important;
                text-transform: none !important;
                display: flex !important;
                justify-content: flex-start !important;
            }}
            [data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-secondary"] * {{
                color: {BRAND_SIDEBAR_TEXT} !important;
            }}
            [data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-secondary"]:hover {{
                background-color: rgba(255,255,255,0.06) !important;
                border-left-color: rgba(243,156,18,0.4) !important;
                opacity: 1 !important;
            }}
            /* Active nav item (primary button) */
            [data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-primary"] {{
                background: linear-gradient(90deg, rgba(0,80,93,0.5) 0%, rgba(0,80,93,0.15) 100%) !important;
                border: none !important;
                border-left: 3px solid #F39C12 !important;
                border-radius: 8px !important;
                font-weight: 700 !important;
                font-size: 0.85rem !important;
                color: #FFFFFF !important;
                opacity: 1 !important;
                padding: 0.5rem 0.75rem !important;
                text-transform: none !important;
                display: flex !important;
                justify-content: flex-start !important;
            }}
            [data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-primary"] * {{
                color: #FFFFFF !important;
            }}
            /* === Sidebar Logout Button — use primary type with override === */

            /* Force left-align everything inside sidebar nav buttons */
            [data-testid="stSidebar"] .stButton {{
                text-align: left !important;
            }}
            [data-testid="stSidebar"] .stButton > button p,
            [data-testid="stSidebar"] .stButton > button div,
            [data-testid="stSidebar"] .stButton > button span {{
                text-align: left !important;
                width: 100% !important;
                justify-content: flex-start !important;
            }}
            /* Reduce gap between nav buttons */
            [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {{
                margin: 0 !important;
                padding: 0 !important;
            }}
            [data-testid="stSidebar"] .stElementContainer {{
                margin: 0 !important;
            }}

            /* === Sidebar Expander === */
            [data-testid="stSidebar"] .stExpander {{
                border: none !important;
                border-radius: 8px !important;
                background-color: rgba(255,255,255,0.95) !important;
                overflow: hidden;
                margin: 0.15rem 0 !important;
            }}
            [data-testid="stSidebar"] .stExpander summary {{
                font-size: 0.82rem !important;
                font-weight: 600 !important;
                color: {BRAND_TEXT_COLOR} !important;
                padding: 0.5rem 0.75rem !important;
            }}
            /* All text inside expander — dark on white */
            [data-testid="stSidebar"] .stExpander * {{
                color: {BRAND_TEXT_COLOR} !important;
            }}
            [data-testid="stSidebar"] .stExpander [data-testid="stExpanderDetails"] {{
                padding: 0.4rem 0.6rem !important;
            }}
            /* File uploader inside expander */
            [data-testid="stSidebar"] .stExpander .stFileUploader section {{
                border: 1px dashed #D5DBDB !important;
                border-radius: 6px !important;
            }}
            [data-testid="stSidebar"] .stExpander .stFileUploader small,
            [data-testid="stSidebar"] .stExpander .stFileUploader span {{
                color: #5D6D7E !important;
            }}
            /* Browse files button inside expander */
            [data-testid="stSidebar"] .stExpander .stFileUploader button {{
                color: {BRAND_PRIMARY_COLOR} !important;
                border-color: {BRAND_PRIMARY_COLOR} !important;
            }}
            /* Remove button for documents */
            [data-testid="stSidebar"] .stExpander .stButton > button {{
                border-color: rgba(231,76,60,0.4) !important;
                color: #E74C3C !important;
                background-color: transparent !important;
                font-size: 0.72rem !important;
                padding: 0.15rem 0.5rem !important;
            }}
            /* Caption text in expander */
            [data-testid="stSidebar"] .stExpander .stCaption,
            [data-testid="stSidebar"] .stExpander [data-testid="stCaptionContainer"] {{
                color: #5D6D7E !important;
            }}

            /* === Typography (Articulat-inspired) === */
            body, .stApp {{
                font-family: 'Articulat', "Helvetica Neue", Helvetica, Arial, sans-serif;
            }}
            [data-testid="stMarkdownContainer"] > h1 {{
                font-size: 2rem !important;
                font-weight: 700 !important;
                color: {BRAND_TEXT_COLOR} !important;
                letter-spacing: -0.02em !important;
            }}
            [data-testid="stMarkdownContainer"] > h2 {{
                font-size: 1.5rem !important;
                font-weight: 700 !important;
                color: {BRAND_TEXT_COLOR} !important;
                letter-spacing: -0.01em !important;
            }}
            [data-testid="stMarkdownContainer"] > h3 {{
                font-size: 1.25rem !important;
                font-weight: 600 !important;
                color: {BRAND_TEXT_COLOR} !important;
            }}

            /* === Links === */
            a {{
                color: {BRAND_PRIMARY_COLOR} !important;
            }}

            /* === Form Controls === */
            .stTextArea textarea,
            .stTextInput input {{
                border-radius: 6px !important;
                border-color: #D5DBDB !important;
                transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
            }}
            .stTextArea textarea:focus,
            .stTextInput input:focus {{
                border-color: {BRAND_PRIMARY_COLOR} !important;
                box-shadow: 0 0 0 1px {BRAND_PRIMARY_COLOR} !important;
            }}
            .stSelectbox > div > div {{
                border-radius: 6px !important;
            }}

            /* === Primary Button (Versaterm style: bold, uppercase) === */
            .stButton > button[kind="primary"],
            .stButton > button[data-testid="stBaseButton-primary"] {{
                background-color: {BRAND_PRIMARY_COLOR} !important;
                color: white !important;
                border-radius: 6px !important;
                padding: 0.5rem 1.5rem !important;
                font-weight: 700 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.05em !important;
                font-size: 0.82rem !important;
                border: none !important;
                transition: background-color 0.2s ease !important;
            }}
            .stButton > button[kind="primary"]:hover,
            .stButton > button[data-testid="stBaseButton-primary"]:hover {{
                background-color: {BRAND_PRIMARY_HOVER} !important;
            }}

            /* Secondary buttons */
            .stMainBlockContainer .stButton > button {{
                border-color: {BRAND_PRIMARY_COLOR} !important;
                border-radius: 6px !important;
                font-weight: 600 !important;
            }}

            /* === Layout === */
            .stApp hr {{
                border-color: #E0E4E8 !important;
                margin: 1.5rem 0 !important;
            }}

            .stCaption {{
                margin-top: -0.5rem !important;
                margin-bottom: 1rem !important;
            }}
        </style>
        """


def inject_theme_css():
    st.markdown(_build_theme_css(), unsafe_allow_html=True)


@lru_cache(maxsize=1)
def _build_login_css():
    return f"""
        <style>
            /* Hide sidebar */
            [data-testid="stSidebarCollapsedControl"] {{ display: none !important; }}
            [data-testid="stSidebar"] {{ display: none !important; }}

            /* Dark gradient background matching versaterm.com */
            .stApp {{
                background: linear-gradient(135deg, {BRAND_SIDEBAR_BG} 0%, #073350 50%, {BRAND_PRIMARY_COLOR} 100%) !important;
            }}

            /* Center content */
            .stMainBlockContainer {{
                max-width: 520px !important;
                margin: 0 auto !important;
                padding-top: 2vh !important;
            }}

            /* White text for branding on dark bg */
            .stMainBlockContainer h2,
            .stMainBlockContainer p {{
                color: #FFFFFF !important;
            }}

            /* Login card containers — white with shadow */
            .stMainBlockContainer [data-testid="stVerticalBlockBorderWrapper"] {{
                background: #FFFFFF !important;
                border-radius: 12px !important;
                border: none !important;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
                padding: 1rem 1.25rem !important;
                margin-bottom: 1rem !important;
            }}
            /* Text inside cards stays dark */
            .stMainBlockContainer [data-testid="stVerticalBlockBorderWrapper"] p,
            .stMainBlockContainer [data-testid="stVerticalBlockBorderWrapper"] span,
            .stMainBlockContainer [data-testid="stVerticalBlockBorderWrapper"] label,
            .stMainBlockContainer [data-testid="stVerticalBlockBorderWrapper"] div,
            .stMainBlockContainer [data-testid="stVerticalBlockBorderWrapper"] h1,
            .stMainBlockContainer [data-testid="stVerticalBlockBorderWrapper"] h2,
            .stMainBlockContainer [data-testid="stVerticalBlockBorderWrapper"] h3,
            .stMainBlockContainer [data-testid="stVerticalBlockBorderWrapper"] small {{
                color: {BRAND_TEXT_COLOR} !important;
            }}
            /* Primary button text stays white */
            .stMainBlockContainer [data-testid="stVerticalBlockBorderWrapper"] button[kind="primary"],
            .stMainBlockContainer [data-testid="stVerticalBlockBorderWrapper"] button[data-testid="stBaseButton-primary"],
            .stMainBlockContainer [data-testid="stVerticalBlockBorderWrapper"] button[kind="primaryFormSubmit"],
            .stMainBlockContainer [data-testid="stVerticalBlockBorderWrapper"] button[data-testid="stBaseButton-primaryFormSubmit"] {{
                color: #FFFFFF !important;
            }}
            /* Secondary form buttons (Resend Code) inside cards — teal outline */
            .stMainBlockContainer [data-testid="stForm"] .stFormSubmitButton > button:not([kind="primaryFormSubmit"]):not([data-testid="stBaseButton-primaryFormSubmit"]) {{
                color: {BRAND_PRIMARY_COLOR} !important;
                border: 1.5px solid {BRAND_PRIMARY_COLOR} !important;
                background-color: #FFFFFF !important;
                font-weight: 600 !important;
            }}
            .stMainBlockContainer [data-testid="stForm"] .stFormSubmitButton > button:not([kind="primaryFormSubmit"]):not([data-testid="stBaseButton-primaryFormSubmit"]) p,
            .stMainBlockContainer [data-testid="stForm"] .stFormSubmitButton > button:not([kind="primaryFormSubmit"]):not([data-testid="stBaseButton-primaryFormSubmit"]) div,
            .stMainBlockContainer [data-testid="stForm"] .stFormSubmitButton > button:not([kind="primaryFormSubmit"]):not([data-testid="stBaseButton-primaryFormSubmit"]) span {{
                color: {BRAND_PRIMARY_COLOR} !important;
            }}
            .stMainBlockContainer [data-testid="stForm"] .stFormSubmitButton > button:not([kind="primaryFormSubmit"]):not([data-testid="stBaseButton-primaryFormSubmit"]):hover {{
                background-color: rgba(0,80,93,0.08) !important;
            }}

            /* Login form inner spacing — prevent overlap */
            .stMainBlockContainer [data-testid="stForm"] {{
                padding: 0.75rem 0.5rem !important;
            }}
            .stMainBlockContainer [data-testid="stForm"] [data-testid="stVerticalBlock"] {{
                gap: 1rem !important;
            }}
            /* Hide the "Press Enter to submit" helper text */
            [data-testid="stFormSubmitHelper"],
            .stFormSubmitHelper,
            .stMainBlockContainer [data-testid="stForm"] small {{
                display: none !important;
            }}
            /* Ensure text inputs don't overflow */
            .stMainBlockContainer .stTextInput {{
                margin-bottom: 0.5rem !important;
            }}

            /* Footer text light on dark */
            .stMainBlockContainer > div > div:last-child p {{
                color: rgba(255,255,255,0.4) !important;
            }}

            /* Tighten button padding */
            .stMainBlockContainer .stButton > button,
            .stMainBlockContainer .stFormSubmitButton > button {{
                padding: 0.45rem 0.75rem !important;
                font-size: 0.82rem !important;
                white-space: nowrap !important;
                overflow: hidden !important;
                text-overflow: ellipsis !important;
            }}

            /* Form submit primary buttons */
            .stMainBlockContainer .stFormSubmitButton > button[kind="primaryFormSubmit"],
            .stMainBlockContainer .stFormSubmitButton > button[data-testid="stBaseButton-primaryFormSubmit"] {{
                background-color: {BRAND_PRIMARY_COLOR} !important;
                color: #FFFFFF !important;
                border: none !important;
                font-weight: 700 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.05em !important;
            }}
            .stMainBlockContainer .stFormSubmitButton > button[kind="primaryFormSubmit"]:hover,
            .stMainBlockContainer .stFormSubmitButton > button[data-testid="stBaseButton-primaryFormSubmit"]:hover {{
                background-color: {BRAND_PRIMARY_HOVER} !important;
            }}

        </style>
        """


def inject_login_css():
    """Extra CSS for the login page — hides sidebar, centers content."""
    st.markdown(_build_login_css(), unsafe_allow_html=True)
