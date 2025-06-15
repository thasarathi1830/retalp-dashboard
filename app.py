import streamlit as st
import pandas as pd
from pathlib import Path
import pdfkit
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

from src.sidebar import render_sidebar

# Set up Streamlit page configuration
st.set_page_config(page_title="Retalp Intern DashBoard", layout="wide")

# Ensure output directory exists
Path("output").mkdir(exist_ok=True)
Path("data").mkdir(exist_ok=True)

def save_uploaded_file(uploaded_file):
    file_path = Path("data") / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def load_data(file_path):
    try:
        if file_path.suffix.lower() == ".csv":
            # Try UTF-8 first, fallback to Latin-1 if needed
            try:
                return pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                return pd.read_csv(file_path, encoding='latin1')
        elif file_path.suffix.lower() in [".xlsx", ".xls"]:
            return pd.read_excel(file_path, engine="openpyxl")
        elif file_path.suffix.lower() == ".ods":
            return pd.read_excel(file_path, engine="odf")
        else:
            st.error("Unsupported file format!")
            return None
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

def generate_profile_report(df):
    return ProfileReport(df, title="Retalp EDA Report", explorative=True)

def export_report_to_pdf(report, html_path, pdf_path):
    report.to_file(html_path)
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    pdfkit.from_file(str(html_path), str(pdf_path), configuration=config)

def main():
    st.title("Retalp EDA Dashboard")

    uploaded_file = render_sidebar()

    if uploaded_file:
        file_path = save_uploaded_file(uploaded_file)
        st.success(f"File `{uploaded_file.name}` uploaded successfully!")

        df = load_data(file_path)
        if df is not None:
            st.subheader("Data Preview")
            st.dataframe(df.head())

            with st.spinner("Generating EDA report..."):
                profile = generate_profile_report(df)
                st.subheader("📈 Retalp EDA Report")
                st_profile_report(profile)

                # Export to PDF
                html_path = Path("output") / "eda_report.html"
                pdf_path = Path("output") / "eda_report.pdf"
                export_report_to_pdf(profile, html_path, pdf_path)

                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📥 Download EDA Report as PDF",
                        data=f,
                        file_name="eda_report.pdf",
                        mime="application/pdf"
                    )
    else:
        st.info("👈 Upload a file from the sidebar to start your analysis.")

if __name__ == "__main__":
    main()


