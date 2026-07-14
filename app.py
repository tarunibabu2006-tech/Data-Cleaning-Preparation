import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io

# ----------------------------------------------------
# 1. Page Configuration & Theme
# ----------------------------------------------------
st.set_page_config(
    page_title="RefineData | Interactive Cleaning & EDA Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Injection for Dark Theme, Glassmorphism, and Fonts
def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Custom Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(31, 41, 55, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* Glowing Title Headers */
    .glowing-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #a78bfa 0%, #3b82f6 50%, #14b8a6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        letter-spacing: -0.05em;
    }
    
    .glowing-subheader {
        font-size: 1.5rem;
        font-weight: 600;
        color: #e9d5ff;
        border-bottom: 1px solid #4c1d95;
        padding-bottom: 8px;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    
    /* KPI Metrics Styling */
    div[data-testid="metric-container"] {
        background: rgba(17, 24, 39, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Custom Alert Styling */
    div.stAlert {
        border-radius: 12px;
        background: rgba(31, 41, 55, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Custom buttons */
    .stButton>button {
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5);
        border: none;
        color: white;
    }
    
    /* Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0e1117;
        color: #9ca3af;
        text-align: center;
        padding: 10px;
        font-size: 0.85rem;
        border-top: 1px solid #1f2937;
        z-index: 100;
    }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ----------------------------------------------------
# 2. Session State & Data Initialization
# ----------------------------------------------------
if 'df_raw' not in st.session_state:
    st.session_state.df_raw = None
if 'df_clean' not in st.session_state:
    st.session_state.df_clean = None
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Home"

def generate_sample_data():
    data = {
        'ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2],
        'Name': ['alice ', 'bob', 'charlie', 'David', 'Eve', 'frank', 'Grace', 'heidi', 'Ivan', 'Judy', 'alice ', 'bob'],
        'Age': [24.0, 30.0, np.nan, 28.0, 35.0, 40.0, 22.0, np.nan, 31.0, 29.0, 24.0, 30.0],
        'City': ['New York', 'London', 'Paris', 'Tokyo', 'Berlin', 'Rome', 'Madrid', 'London', 'Paris', 'New York', 'New York', 'London'],
        'Score': [85.5, 78.0, 92.1, 70.3, np.nan, 88.9, 95.0, 65.2, 81.7, 74.4, 85.5, 78.0],
        'Date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08', '2023-01-09', '2023-01-10', '2023-01-01', '2023-01-02']
    }
    return pd.DataFrame(data)

def load_local_data():
    try:
        return pd.read_csv('dataset.csv')
    except Exception:
        try:
            return pd.read_csv('cleaned_dataset.csv')
        except Exception:
            return generate_sample_data()

# ----------------------------------------------------
# 3. Sidebar Configuration
# ----------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #a78bfa;'>✨ RefineData</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.9rem; color: #9ca3af;'>Interactive Data Cleaning & EDA Dashboard</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Navigation
    st.markdown("### 🗺️ Navigation")
    choice = st.radio("Go to", ["🏠 Dashboard Home", "🧼 Cleaning Studio", "📊 EDA Playground", "💾 Export & Deploy"])
    
    st.markdown("---")
    
    # Data Input Settings
    st.markdown("### 📥 Data Source")
    data_source = st.radio("Choose Source", ["📁 Upload CSV File", "💡 Use Default Sample Dataset"])
    
    uploaded_file = None
    if data_source == "📁 Upload CSV File":
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"], help="Limit 200MB. Only CSV format is supported currently.")
    
    # Reset State Button
    st.markdown("---")
    if st.button("🔄 Reset to Original Data", use_container_width=True):
        st.session_state.df_raw = None
        st.session_state.df_clean = None
        st.success("App data reset successfully!")
        st.rerun()

# ----------------------------------------------------
# 4. Data Loading Handler
# ----------------------------------------------------
# Check if file uploaded or default selected
if data_source == "📁 Upload CSV File" and uploaded_file is not None:
    try:
        df_loaded = pd.read_csv(uploaded_file)
        if st.session_state.df_raw is None or not st.session_state.df_raw.equals(df_loaded):
            st.session_state.df_raw = df_loaded
            st.session_state.df_clean = df_loaded.copy()
    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    # Use Default Sample Dataset
    if st.session_state.df_raw is None:
        df_local = load_local_data()
        st.session_state.df_raw = df_local
        st.session_state.df_clean = df_local.copy()

df_raw = st.session_state.df_raw
df_clean = st.session_state.df_clean

# ----------------------------------------------------
# 5. Core Views Implementation
# ----------------------------------------------------

# PAGE 1: DASHBOARD HOME
if "🏠 Dashboard Home" in choice:
    st.markdown("<h1 class='glowing-header'>Data Quality Overview</h1>", unsafe_allow_html=True)
    st.markdown("Assess the cleanliness and statistics of your raw dataset. Head over to the **🧼 Cleaning Studio** tab to fix issues.")
    
    # KPI Grid
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Records", value=f"{df_clean.shape[0]}")
    with col2:
        st.metric(label="Total Columns", value=f"{df_clean.shape[1]}")
    with col3:
        missing_count = df_clean.isnull().sum().sum()
        st.metric(label="Missing Cells", value=f"{missing_count}", delta=f"{-missing_count if missing_count == 0 else missing_count} cells", delta_color="inverse")
    with col4:
        duplicate_count = df_clean.duplicated().sum()
        st.metric(label="Duplicate Rows", value=f"{duplicate_count}", delta=f"{-duplicate_count if duplicate_count == 0 else duplicate_count} rows", delta_color="inverse")
        
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3 class='glowing-subheader' style='margin-top: 0;'>🔍 Dataset Explorer</h3>", unsafe_allow_html=True)
    
    # Grid details
    st.markdown("**Data Preview (Showing first 10 rows):**")
    st.dataframe(df_clean.head(10), use_container_width=True)
    
    # Schema Analysis
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("**Column Schema details:**")
        schema_df = pd.DataFrame({
            "Data Type": df_clean.dtypes.astype(str),
            "Missing Values": df_clean.isnull().sum(),
            "Unique Values": df_clean.nunique()
        })
        st.dataframe(schema_df, use_container_width=True)
        
    with col_right:
        st.markdown("**Missing Data Heatmap / Matrix Representation:**")
        # Visual representation of missing values
        null_mask = df_clean.isnull().astype(int)
        fig_null = px.imshow(
            null_mask.T,
            labels=dict(x="Row Index", y="Column Name", color="Is Null"),
            x=df_clean.index,
            y=df_clean.columns,
            color_continuous_scale=[[0, "#111827"], [1, "#f43f5e"]],
            aspect="auto"
        )
        fig_null.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#fafafa',
            coloraxis_showscale=False,
            height=250,
            margin=dict(l=20, r=20, t=10, b=10)
        )
        st.plotly_chart(fig_null, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# PAGE 2: CLEANING STUDIO
elif "🧼 Cleaning Studio" in choice:
    st.markdown("<h1 class='glowing-header'>Data Cleaning Studio</h1>", unsafe_allow_html=True)
    st.markdown("Interactively clean your dataset step-by-step. All changes will be saved to your session workspace.")
    
    # Compare raw vs cleaned shape
    st.info(f"💡 Current Session Status: Raw Rows = **{df_raw.shape[0]}** | Cleaned Rows = **{df_clean.shape[0]}**")
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    
    # Step 1: Duplicate handling
    st.markdown("<h3 class='glowing-subheader' style='margin-top:0;'>1. Duplicate Rows Detection & Clean</h3>", unsafe_allow_html=True)
    current_duplicates = df_clean.duplicated().sum()
    st.write(f"Found **{current_duplicates}** duplicate row(s) in the current dataset.")
    
    if current_duplicates > 0:
        if st.button("🗑️ Remove All Duplicates", key="btn_remove_duplicates"):
            df_clean = df_clean.drop_duplicates()
            st.session_state.df_clean = df_clean
            st.success("Removed all duplicate rows successfully!")
            st.rerun()
    else:
        st.write("✅ Dataset does not contain duplicate rows.")
        
    st.markdown("---")
    
    # Step 2: Missing values imputation
    st.markdown("<h3 class='glowing-subheader'>2. Missing Value Imputation</h3>", unsafe_allow_html=True)
    missing_stats = df_clean.isnull().sum()
    cols_with_missing = missing_stats[missing_stats > 0].index.tolist()
    
    if cols_with_missing:
        st.write(f"The following columns contain missing values: **{', '.join(cols_with_missing)}**")
        
        sel_col_missing = st.selectbox("Select column to impute", cols_with_missing)
        col_missing_type = df_clean[sel_col_missing].dtype
        st.write(f"Column **{sel_col_missing}** is of type **{col_missing_type}** and has **{missing_stats[sel_col_missing]}** nulls.")
        
        # Give imputation choices
        impute_strategy = None
        if np.issubdtype(col_missing_type, np.number):
            impute_strategy = st.radio(
                "Imputation Strategy for numerical column",
                ["Fill with Median (Recommended)", "Fill with Mean", "Fill with Mode", "Fill with Constant (0)", "Drop Rows with Missing Values"]
            )
        else:
            impute_strategy = st.radio(
                "Imputation Strategy for categorical/text column",
                ["Fill with Mode (Most Frequent) (Recommended)", "Fill with Constant Label ('Unknown')", "Drop Rows with Missing Values"]
            )
            
        if st.button(f"Apply Imputation on '{sel_col_missing}'", key="btn_impute"):
            if "Median" in impute_strategy:
                val = df_clean[sel_col_missing].median()
                df_clean[sel_col_missing] = df_clean[sel_col_missing].fillna(val)
            elif "Mean" in impute_strategy:
                val = df_clean[sel_col_missing].mean()
                df_clean[sel_col_missing] = df_clean[sel_col_missing].fillna(val)
            elif "Mode" in impute_strategy:
                val = df_clean[sel_col_missing].mode()[0]
                df_clean[sel_col_missing] = df_clean[sel_col_missing].fillna(val)
            elif "Constant (0)" in impute_strategy:
                df_clean[sel_col_missing] = df_clean[sel_col_missing].fillna(0)
            elif "Constant Label" in impute_strategy:
                df_clean[sel_col_missing] = df_clean[sel_col_missing].fillna("Unknown")
            elif "Drop" in impute_strategy:
                df_clean = df_clean.dropna(subset=[sel_col_missing])
            
            st.session_state.df_clean = df_clean
            st.success(f"Applied strategy successfully on {sel_col_missing}!")
            st.rerun()
    else:
        st.write("✅ Dataset has no missing values.")
        
    st.markdown("---")
    
    # Step 3: Text columns format standardization
    st.markdown("<h3 class='glowing-subheader'>3. Standardize Text Formatting</h3>", unsafe_allow_html=True)
    text_cols = df_clean.select_dtypes(include=['object']).columns.tolist()
    if text_cols:
        st.write("Select string/text columns to clean formatting (remove extra spaces, standardize capitalization).")
        sel_text_col = st.selectbox("Select Text Column", text_cols, key="sel_text_col")
        text_case_strategy = st.radio("Capitalization Strategy", ["Title Case (e.g. 'New York')", "LOWER CASE (e.g. 'new york')", "UPPER CASE (e.g. 'NEW YORK')", "Only strip leading/trailing spaces"])
        
        if st.button(f"Standardize '{sel_text_col}' Format"):
            # Strip spaces
            df_clean[sel_text_col] = df_clean[sel_text_col].astype(str).str.strip()
            # Modify case
            if "Title" in text_case_strategy:
                df_clean[sel_text_col] = df_clean[sel_text_col].str.title()
            elif "Lower" in text_case_strategy:
                df_clean[sel_text_col] = df_clean[sel_text_col].str.lower()
            elif "Upper" in text_case_strategy:
                df_clean[sel_text_col] = df_clean[sel_text_col].str.upper()
                
            st.session_state.df_clean = df_clean
            st.success(f"Formatting standardized for column: {sel_text_col}!")
            st.rerun()
    else:
        st.write("No text columns found in dataset.")
        
    st.markdown("---")
    
    # Step 4: Parse Date formatting
    st.markdown("<h3 class='glowing-subheader'>4. Standardize Date / Time Formats</h3>", unsafe_allow_html=True)
    all_cols = df_clean.columns.tolist()
    sel_date_col = st.selectbox("Select Date Column", all_cols, index=all_cols.index('Date') if 'Date' in all_cols else 0)
    
    if st.button(f"Convert '{sel_date_col}' to Datetime"):
        try:
            df_clean[sel_date_col] = pd.to_datetime(df_clean[sel_date_col], errors='coerce')
            st.session_state.df_clean = df_clean
            st.success(f"Successfully formatted column '{sel_date_col}' to Datetime format!")
            st.rerun()
        except Exception as e:
            st.error(f"Could not convert column {sel_date_col} to datetime: {e}")
            
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Show comparison
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3 class='glowing-subheader' style='margin-top: 0;'>👁️ Raw vs. Cleaned Dataset Comparison</h3>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Raw Dataset Preview (Original)", "Cleaned Dataset Preview (Current)"])
    with tab1:
        st.dataframe(df_raw.head(10), use_container_width=True)
    with tab2:
        st.dataframe(df_clean.head(10), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# PAGE 3: EDA PLAYGROUND
elif "📊 EDA Playground" in choice:
    st.markdown("<h1 class='glowing-header'>Exploratory Data Analysis Playground</h1>", unsafe_allow_html=True)
    st.markdown("Visualize features and investigate correlation parameters using modern interactive charts.")
    
    # Quick statistics
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3 class='glowing-subheader' style='margin-top:0;'>📊 Describe Statistics</h3>", unsafe_allow_html=True)
    st.dataframe(df_clean.describe(include='all').astype(str), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Interactive Plots
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3 class='glowing-subheader' style='margin-top:0;'>📈 Custom Interactive Visualizer</h3>", unsafe_allow_html=True)
    
    plot_type = st.selectbox(
        "Choose Visualization Type",
        ["Histogram (Numerical Distributions)", "Scatter Plot (Relationship analysis)", "Bar Plot (Categorical Aggregate)", "Line Plot (Trends over Date)"]
    )
    
    cols = df_clean.columns.tolist()
    
    if plot_type == "Histogram (Numerical Distributions)":
        num_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            sel_num_col = st.selectbox("Select numerical column", num_cols)
            bins = st.slider("Number of bins", 5, 50, 20)
            
            fig = px.histogram(
                df_clean,
                x=sel_num_col,
                nbins=bins,
                title=f"Distribution of {sel_num_col}",
                color_discrete_sequence=['#8b5cf6'],
                marginal="box",
                template="plotly_dark"
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_family="Outfit"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No numerical columns found in your dataset to plot a histogram.")
            
    elif plot_type == "Scatter Plot (Relationship analysis)":
        num_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
        if len(num_cols) >= 2:
            col_x = st.selectbox("Select X-axis column", num_cols, index=0)
            col_y = st.selectbox("Select Y-axis column", num_cols, index=1 if len(num_cols) > 1 else 0)
            
            cat_cols = [None] + df_clean.select_dtypes(include=['object']).columns.tolist()
            col_color = st.selectbox("Select Color legend column (Optional)", cat_cols, index=0)
            
            fig = px.scatter(
                df_clean,
                x=col_x,
                y=col_y,
                color=col_color,
                title=f"{col_y} vs {col_x}",
                template="plotly_dark",
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_family="Outfit"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Scatter plot requires at least 2 numerical columns.")
            
    elif plot_type == "Bar Plot (Categorical Aggregate)":
        cat_cols = df_clean.select_dtypes(include=['object']).columns.tolist()
        num_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
        
        if cat_cols and num_cols:
            col_cat = st.selectbox("Select Categorical Feature (Group by)", cat_cols)
            col_num = st.selectbox("Select Numerical Metric Value", num_cols)
            agg_func = st.selectbox("Aggregation Method", ["Mean", "Sum", "Count", "Min", "Max"])
            
            # Aggregate data
            if agg_func == "Mean":
                df_agg = df_clean.groupby(col_cat)[col_num].mean().reset_index()
            elif agg_func == "Sum":
                df_agg = df_clean.groupby(col_cat)[col_num].sum().reset_index()
            elif agg_func == "Count":
                df_agg = df_clean.groupby(col_cat)[col_num].count().reset_index()
            elif agg_func == "Min":
                df_agg = df_clean.groupby(col_cat)[col_num].min().reset_index()
            elif agg_func == "Max":
                df_agg = df_clean.groupby(col_cat)[col_num].max().reset_index()
                
            fig = px.bar(
                df_agg,
                x=col_cat,
                y=col_num,
                color=col_cat,
                title=f"{agg_func} of {col_num} grouped by {col_cat}",
                template="plotly_dark"
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_family="Outfit"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Bar plot requires at least 1 categorical column and 1 numerical column.")
            
    elif plot_type == "Line Plot (Trends over Date)":
        # Check if we have date columns
        date_cols = []
        for col in df_clean.columns:
            if pd.api.types.is_datetime64_any_dtype(df_clean[col]):
                date_cols.append(col)
        
        if date_cols:
            sel_date = st.selectbox("Select date/time column", date_cols)
            num_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
            
            if num_cols:
                sel_num = st.selectbox("Select numerical value trend line", num_cols)
                df_sorted = df_clean.sort_values(by=sel_date)
                
                fig = px.line(
                    df_sorted,
                    x=sel_date,
                    y=sel_num,
                    title=f"Trend of {sel_num} over time",
                    color_discrete_sequence=['#14b8a6'],
                    template="plotly_dark"
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_family="Outfit"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No numerical columns found to plot trend lines.")
        else:
            st.warning("Please convert a column to Datetime format in the '🧼 Cleaning Studio' tab first.")
            
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Correlation Heatmap
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3 class='glowing-subheader' style='margin-top:0;'>🔥 Correlation Matrix Heatmap</h3>", unsafe_allow_html=True)
    
    num_df = df_clean.select_dtypes(include=[np.number])
    if num_df.shape[1] >= 2:
        corr_matrix = num_df.corr()
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=".2f",
            color_continuous_scale='RdBu_r',
            zmin=-1, zmax=1,
            title="Pearson Correlation Coefficient Matrix"
        )
        fig_corr.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family="Outfit"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.warning("Heatmap requires at least 2 numerical columns in the dataset.")
    st.markdown("</div>", unsafe_allow_html=True)

# PAGE 4: EXPORT & DEPLOY
elif "💾 Export & Deploy" in choice:
    st.markdown("<h1 class='glowing-header'>Export Cleaned Data & Deploy Info</h1>", unsafe_allow_html=True)
    st.markdown("Export your cleaned dataset or get ready to deploy this app online.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='glass-card' style='height: 100%;'>", unsafe_allow_html=True)
        st.markdown("<h3 class='glowing-subheader' style='margin-top:0;'>📥 Download Cleaned Dataset</h3>", unsafe_allow_html=True)
        st.write("Click below to download the cleaned, formatted dataset directly as a CSV file to your local computer.")
        
        # Buffer to save CSV
        csv_buffer = io.StringIO()
        df_clean.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="💾 Download Cleaned CSV",
            data=csv_data,
            file_name="cleaned_dataset_export.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.write("")
        st.write("**Dataset Summary for Export:**")
        st.write(f"- Total rows: **{df_clean.shape[0]}**")
        st.write(f"- Total columns: **{df_clean.shape[1]}**")
        st.write(f"- Formatted Columns: `{', '.join(df_clean.columns.tolist())}`")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='glass-card' style='height: 100%;'>", unsafe_allow_html=True)
        st.markdown("<h3 class='glowing-subheader' style='margin-top:0;'>☁️ Host & Deploy Instructions</h3>", unsafe_allow_html=True)
        st.write("You can deploy this Streamlit Web Application for free using a few different methods:")
        
        st.markdown("""
        1. **Streamlit Community Cloud (Recommended & Free):**
           - Push your changes to your GitHub Repository.
           - Visit [share.streamlit.io](https://share.streamlit.io) and log in using GitHub.
           - Click 'New App', choose your repository `tarunibabu2006-tech/Data-Cleaning-Preparation`, branch `main`, and enter `app.py` as the entrypoint.
           - Click 'Deploy' and your app will be live in 2 minutes!
           
        2. **Deploy on Railway / Render (Dockerized):**
           - We have included a `Dockerfile` in the repository project workspace.
           - Connect your Github to [Railway.app](https://railway.app) or [Render.com](https://render.com).
           - Choose this repository and the server will build automatically using the Dockerfile.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class='footer'>
    RefineData Studio | Developed for Data Analytics Intern & Portfolio Projects | © 2026 Taruni Babu
</div>
""", unsafe_allow_html=True)
