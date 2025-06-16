import streamlit as st
from pathlib import Path

def render_sidebar():
    st.sidebar.title("📁 Upload File")

    # Safely try to load logo
    logo_path = Path("static/logo.png")
    if logo_path.exists():
        st.sidebar.image(str(logo_path), use_container_width=True)
    else:
        st.sidebar.warning("Logo not found in 'static/logo.png'.")

    uploaded_file = st.sidebar.file_uploader("Choose a data file", type=["csv", "xlsx", "xls", "ods"])
    return uploaded_file

