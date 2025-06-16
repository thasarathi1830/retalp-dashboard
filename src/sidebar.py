import streamlit as st

def render_sidebar():
    st.sidebar.image(
        "https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", 
        use_container_width=True  # Updated for Streamlit deprecation warning
    )
    st.sidebar.title("Retalp EDA Dashboard")
    st.sidebar.markdown(
        """
        **Navigation**
        - Data Overview
        - Data Cleaning
        - Outlier Detection
        - Visualizations
        - Full Report
        """
    )
    st.sidebar.markdown("---")
    uploaded_file = st.sidebar.file_uploader(
        "Upload your data file",
        type=["csv", "xlsx", "xls", "ods"]
    )
    st.sidebar.markdown("---")
    st.sidebar.info("Tip: Use the navigation menu above to explore different EDA tools.")
    return uploaded_file




