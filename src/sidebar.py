import streamlit as st

def render_sidebar():
    st.sidebar.title("📊 EDA Dashboard")
    st.sidebar.markdown(
        """
        Welcome!  
        Upload your data file and explore automated EDA.

        **Features:**
        - Upload CSV, Excel, or ODS files
        - Automated profiling & visualizations
        - Download EDA report as PDF
        """
    )

    st.sidebar.markdown("---")
    st.sidebar.header("Upload Data")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a data file",
        type=["csv", "xlsx", "xls", "ods"],
        help="Supported formats: CSV, XLSX, XLS, ODS"
    )
    st.sidebar.markdown("---")

    

    return uploaded_file
