import streamlit as st
import pandas as pd
from utils.styles import load_custom_css
from utils.data_processor import DataProcessor

st.set_page_config(page_title="Data Upload", page_icon="📁", layout="wide")
load_custom_css()

# Initialize data processor
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()

# Page header
st.markdown("""
<div class="page-header-enhanced">
    <h1>📁 Data Upload</h1>
    <p>Upload and preview your retail transaction dataset</p>
</div>
""", unsafe_allow_html=True)

# Upload section
st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
st.subheader("🚀 Upload Your Dataset")

# File upload options
upload_option = st.radio(
    "Choose data source:",
    ["📄 Upload CSV File", "📊 Use Sample Data"],
    horizontal=True
)

if upload_option == "📄 Upload CSV File":
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload any CSV file containing transaction/retail data"
    )
    
    if uploaded_file:
        try:
            # Try multiple encoding options
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            df = None
            
            for encoding in encodings:
                try:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding=encoding)
                    if len(df) > 0:
                        break
                except:
                    continue
            
            if df is not None:
                st.session_state.data = df
                st.session_state.current_step = 2
                
                st.markdown("""
                <div class="success-box-enhanced">
                    <strong>✅ File uploaded successfully!</strong><br>
                    Your dataset has been loaded and is ready for analysis.
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.error("❌ Could not read the file. Please check the format and encoding.")
                
        except Exception as e:
            st.markdown(f"""
            <div class="error-box-enhanced">
                <strong>❌ Error loading file:</strong><br>
                {str(e)}
            </div>
            """, unsafe_allow_html=True)

else:
    # Sample data option
    if st.button("📊 Load Sample Dataset", type="primary", use_container_width=True):
        sample_data = st.session_state.data_processor.create_sample_data()
        st.session_state.data = sample_data
        st.session_state.current_step = 2
        
        st.markdown("""
        <div class="success-box-enhanced">
            <strong>✅ Sample data loaded successfully!</strong><br>
            You can now proceed with the analysis using our sample retail dataset.
        </div>
        """, unsafe_allow_html=True)

# Display dataset overview if data is loaded
if 'data' in st.session_state and st.session_state.data is not None:
    df = st.session_state.data
    
    # Dataset metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="metric-icon">📊</div>
            <div class="metric-value">{len(df):,}</div>
            <div class="metric-label">Total Rows</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="metric-icon">📋</div>
            <div class="metric-value">{len(df.columns)}</div>
            <div class="metric-label">Columns</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="metric-icon">⚠️</div>
            <div class="metric-value">{missing_pct:.1f}%</div>
            <div class="metric-label">Missing Data</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        file_size = df.memory_usage(deep=True).sum() / 1024 / 1024
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="metric-icon">💾</div>
            <div class="metric-value">{file_size:.1f} MB</div>
            <div class="metric-label">Memory Usage</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Data preview section
if 'data' in st.session_state and st.session_state.data is not None:
    st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
    st.subheader("📋 Data Preview")
    
    # Show first few rows
    st.dataframe(df.head(10), use_container_width=True)
    
    # Column information
    st.subheader("📊 Column Information")
    col_info = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes.astype(str),
        'Non-Null Count': df.count(),
        'Unique Values': df.nunique(),
        'Sample Values': [', '.join(map(str, df[col].dropna().unique()[:3])) for col in df.columns]
    })
    st.dataframe(col_info, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("➡️ Proceed to Column Mapping", type="primary", use_container_width=True):
            st.switch_page("pages/2_⚙️_Column_Mapping.py")

else:
    # Instructions when no data is loaded
    st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
    st.info("👆 Please upload a CSV file or load sample data to begin your market basket analysis")
    
    # Show expected data formats
    st.subheader("📝 Expected Data Format")
    st.write("Your CSV should contain transaction data in one of these formats:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Format 1: Transaction-Product pairs**")
        example1 = pd.DataFrame({
            'OrderID': ['O001', 'O001', 'O002', 'O002'],
            'Product': ['Bread', 'Milk', 'Bread', 'Butter'],
            'Customer': ['John', 'John', 'Alice', 'Alice']
        })
        st.dataframe(example1, hide_index=True)
    
    with col2:
        st.write("**Format 2: Retail sales data**")
        example2 = pd.DataFrame({
            'InvoiceNo': ['INV001', 'INV001', 'INV002'],
            'Description': ['Coffee', 'Sugar', 'Coffee'],
            'Quantity': [1, 2, 1],
            'Price': [5.50, 2.00, 5.50]
        })
        st.dataframe(example2, hide_index=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar info
st.sidebar.markdown("### 📁 Data Upload")
st.sidebar.info("""
**Current Step:** Upload Dataset

**What happens here:**
- Upload your CSV file
- Preview data structure
- Validate data quality
- Check for missing values

**Supported Formats:**
- CSV files only
- Any encoding (UTF-8, Latin-1, etc.)
- Transaction/retail data
- Multiple column structures
""")

# Update session state
st.session_state.current_step = max(st.session_state.get('current_step', 1), 1)
