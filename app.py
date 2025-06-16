import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from pathlib import Path
from src.sidebar import render_sidebar

st.set_page_config(page_title="Retalp EDA Dashboard", layout="wide")
Path("data").mkdir(exist_ok=True)
Path("output").mkdir(exist_ok=True)

def load_data(file_path):
    # Try CSV with multiple encodings
    if str(file_path).lower().endswith('.csv'):
        encodings = ['utf-8', 'utf-16', 'latin1', 'cp1252']
        for enc in encodings:
            try:
                return pd.read_csv(file_path, encoding=enc)
            except Exception:
                continue
        raise ValueError("Could not read CSV file with common encodings.")
    # Try Excel with all major engines
    elif str(file_path).lower().endswith('.xlsx'):
        try:
            return pd.read_excel(file_path, engine='openpyxl')
        except Exception:
            pass
    elif str(file_path).lower().endswith('.xls'):
        try:
            return pd.read_excel(file_path, engine='xlrd')
        except Exception:
            pass
    elif str(file_path).lower().endswith('.ods'):
        try:
            return pd.read_excel(file_path, engine='odf')
        except Exception:
            pass
    raise ValueError("File format not supported or file is corrupted.")

uploaded_file = render_sidebar()

if 'df' not in st.session_state:
    st.session_state.df = None

if uploaded_file:
    file_path = Path("data") / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    try:
        df = load_data(file_path)
        st.session_state.df = df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()
else:
    df = st.session_state.df

st.sidebar.markdown("## Choose Section")
section = st.sidebar.radio(
    "Go to",
    ("Data Overview", "Data Cleaning", "Outlier Detection", "Visualizations", "Full Report"),
    index=0
)

if df is not None:
    st.title("📊 Retalp EDA Dashboard")

    # --- Data Overview ---
    if section == "Data Overview":
        st.header("🔍 Data Overview")
        st.write("**Shape:**", df.shape)
        st.write("**Columns:**", list(df.columns))
        st.dataframe(df.head(10))
        st.write("**Summary Statistics:**")
        st.dataframe(df.describe(include='all').T)
        st.write("**Missing Values:**")
        st.dataframe(df.isnull().sum().to_frame("Missing Count"))

    # --- Data Cleaning ---
    elif section == "Data Cleaning":
        st.header("🧹 Data Cleaning")
        st.write("Remove columns, fill missing values, and preview changes.")
        cols = st.multiselect("Select columns to drop", df.columns)
        if cols:
            df = df.drop(columns=cols)
            st.success(f"Dropped columns: {', '.join(cols)}")
        fill_option = st.selectbox("Missing value handling", ["None", "Fill with mean", "Fill with median", "Fill with mode", "Drop rows with NA"])
        if fill_option != "None":
            for col in df.select_dtypes(include=np.number).columns:
                if fill_option == "Fill with mean":
                    df[col].fillna(df[col].mean(), inplace=True)
                elif fill_option == "Fill with median":
                    df[col].fillna(df[col].median(), inplace=True)
                elif fill_option == "Fill with mode":
                    df[col].fillna(df[col].mode(), inplace=True)
            if fill_option == "Drop rows with NA":
                df.dropna(inplace=True)
            st.success(f"Missing values handled: {fill_option}")
        st.dataframe(df.head(10))
        st.session_state.df = df

    # --- Outlier Detection ---
    elif section == "Outlier Detection":
        st.header("🔎 Outlier Detection & Handling")
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        if num_cols:
            col = st.selectbox("Numeric column for outlier detection", num_cols)
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            outliers = df[(df[col] < lower) | (df[col] > upper)]
            st.write(f"**Number of outliers:** {len(outliers)}")
            st.dataframe(outliers)
            action = st.radio("Handle outliers", ["Do nothing", "Cap values", "Remove outliers"])
            if action == "Cap values":
                df[col] = np.where(df[col] < lower, lower, np.where(df[col] > upper, upper, df[col]))
                st.success("Outliers capped to IQR bounds.")
            elif action == "Remove outliers":
                df = df[(df[col] >= lower) & (df[col] <= upper)]
                st.success("Outliers removed.")
            st.session_state.df = df
        else:
            st.info("No numeric columns for outlier detection.")

    # --- Visualizations ---
    elif section == "Visualizations":
        st.header("📈 Visualizations")
        plot_type = st.selectbox("Choose plot type", ["Bar Plot", "Histogram", "Box Plot", "Scatter Plot", "Correlation Heatmap"])
        if plot_type == "Bar Plot":
            cat_cols = df.select_dtypes(include=['object', 'category']).columns
            if len(cat_cols):
                col = st.selectbox("Column", cat_cols)
                fig, ax = plt.subplots()
                df[col].value_counts().plot(kind='bar', ax=ax, color='#1f77b4')
                st.pyplot(fig)
            else:
                st.info("No categorical columns for bar plot.")
        elif plot_type == "Histogram":
            num_cols = df.select_dtypes(include=np.number).columns
            if len(num_cols):
                col = st.selectbox("Column", num_cols)
                bins = st.slider("Bins", 5, 100, 20)
                fig, ax = plt.subplots()
                df[col].plot(kind='hist', bins=bins, ax=ax, color='#ff7f0e', edgecolor='black')
                st.pyplot(fig)
            else:
                st.info("No numeric columns for histogram.")
        elif plot_type == "Box Plot":
            num_cols = df.select_dtypes(include=np.number).columns
            if len(num_cols):
                col = st.selectbox("Column", num_cols)
                fig, ax = plt.subplots()
                sns.boxplot(x=df[col], ax=ax, color='#2ca02c')
                st.pyplot(fig)
            else:
                st.info("No numeric columns for box plot.")
        elif plot_type == "Scatter Plot":
            num_cols = df.select_dtypes(include=np.number).columns
            if len(num_cols) >= 2:
                x = st.selectbox("X axis", num_cols)
                y = st.selectbox("Y axis", num_cols, index=1 if len(num_cols) > 1 else 0)
                fig, ax = plt.subplots()
                sns.scatterplot(x=df[x], y=df[y], ax=ax, color='#d62728')
                st.pyplot(fig)
            else:
                st.info("Need at least two numeric columns for scatter plot.")
        elif plot_type == "Correlation Heatmap":
            num_cols = df.select_dtypes(include=np.number).columns
            if len(num_cols) >= 2:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(df[num_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
                st.pyplot(fig)
            else:
                st.info("Need at least two numeric columns for heatmap.")

    # --- Full Report ---
    elif section == "Full Report":
        st.header("🤖 Automated EDA Report")
        if st.button("Generate and Show Report"):
            with st.spinner("Generating report..."):
                profile = ProfileReport(df, title="Full EDA Report", explorative=True)
                st_profile_report(profile)
else:
    st.info("👈 Upload a file from the sidebar to start.")



