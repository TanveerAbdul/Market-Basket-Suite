import streamlit as st
from utils.styles import load_custom_css
from utils.data_processor import DataProcessor

st.set_page_config(page_title="Column Mapping", page_icon="⚙️", layout="wide")
load_custom_css()

# Check if data exists
if 'data' not in st.session_state or st.session_state.data is None:
    st.error("❌ No data found. Please upload a dataset first.")
    if st.button("🔙 Go to Data Upload"):
        st.switch_page("pages/1_📁_Data_Upload.py")
    st.stop()

df = st.session_state.data

# Initialize data processor
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()

# Page header
st.markdown("""
<div class="page-header-enhanced">
    <h1>⚙️ Column Mapping</h1>
    <p>Map your dataset columns to analysis requirements</p>
</div>
""", unsafe_allow_html=True)

# Auto-detect column types
potential_mappings = st.session_state.data_processor.detect_column_types(df)

# Column mapping interface
st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
st.subheader("🎯 Configure Column Mapping")

# Show auto-detection results
st.markdown("#### 🤖 Auto-Detection Results")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**📋 Detected Patterns:**")
    for col_type, suggestions in potential_mappings.items():
        if suggestions:
            st.write(f"- **{col_type.replace('_', ' ').title()}**: {', '.join(suggestions[:2])}")

with col2:
    st.markdown("**📊 Data Quality Check:**")
    quality_info = []
    for col in df.columns:
        missing_pct = (df[col].isnull().sum() / len(df)) * 100
        if missing_pct < 10:
            quality_info.append(f"✅ {col}: {missing_pct:.1f}% missing")
        else:
            quality_info.append(f"⚠️ {col}: {missing_pct:.1f}% missing")
    
    for info in quality_info[:5]:  # Show first 5
        st.write(info)

st.markdown("---")

# Manual column selection
st.markdown("#### ⚙️ Manual Column Selection")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔴 Required Columns")
    
    # Transaction ID
    transaction_col = st.selectbox(
        "Transaction/Order ID Column *",
        ['None'] + list(df.columns),
        index=1 if potential_mappings['transaction_id'] and potential_mappings['transaction_id'][0] in df.columns 
        else 0,
        help="Column that groups items into transactions"
    )
    
    # Product/Item
    product_col = st.selectbox(
        "Product/Item Column *",
        ['None'] + list(df.columns),
        index=1 if potential_mappings['product_item'] and potential_mappings['product_item'][0] in df.columns 
        else 0,
        help="Column containing product/item names"
    )

with col2:
    st.markdown("### 🟡 Optional Columns")
    
    # Customer ID
    customer_col = st.selectbox(
        "Customer ID Column",
        ['None'] + list(df.columns),
        index=df.columns.get_loc(potential_mappings['customer_id'][0]) + 1 
        if potential_mappings['customer_id'] and potential_mappings['customer_id'][0] in df.columns 
        else 0,
        help="Customer identifier (optional)"
    )
    
    # Price/Sales
    price_col = st.selectbox(
        "Price/Sales Column",
        ['None'] + list(df.columns),
        index=df.columns.get_loc(potential_mappings['price_sales'][0]) + 1 
        if potential_mappings['price_sales'] and potential_mappings['price_sales'][0] in df.columns 
        else 0,
        help="Price or sales amount (optional)"
    )
    
    # Quantity
    quantity_col = st.selectbox(
        "Quantity Column",
        ['None'] + list(df.columns),
        index=df.columns.get_loc(potential_mappings['quantity'][0]) + 1 
        if potential_mappings['quantity'] and potential_mappings['quantity'][0] in df.columns 
        else 0,
        help="Quantity of items (optional)"
    )
    
    # Category
    category_col = st.selectbox(
        "Category Column",
        ['None'] + list(df.columns),
        index=df.columns.get_loc(potential_mappings['category'][0]) + 1 
        if potential_mappings['category'] and potential_mappings['category'][0] in df.columns 
        else 0,
        help="Product category (optional)"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Validation and preview
if transaction_col != 'None' and product_col != 'None':
    
    # Store mapping
    column_mapping = {
        'transaction_id': transaction_col,
        'product_item': product_col,
        'customer_id': customer_col if customer_col != 'None' else None,
        'price_sales': price_col if price_col != 'None' else None,
        'quantity': quantity_col if quantity_col != 'None' else None,
        'category': category_col if category_col != 'None' else None
    }
    
    st.session_state.column_mapping = column_mapping
    st.session_state.current_step = 3
    
    st.markdown("""
    <div class="success-box-enhanced">
        <strong>✅ Column mapping configured successfully!</strong><br>
        Your columns have been mapped and validated.
    </div>
    """, unsafe_allow_html=True)
    
    # Data quality validation
    quality_report = st.session_state.data_processor.validate_data_quality(
        df, transaction_col, product_col
    )
    
    # Preview mapped data
    st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
    st.subheader("📋 Mapped Data Preview")
    
    preview_cols = [col for col in [transaction_col, product_col, customer_col, price_col, quantity_col, category_col] if col != 'None']
    preview_df = df[preview_cols].head(10)
    st.dataframe(preview_df, use_container_width=True)
    
    # Data quality metrics
    st.subheader("📊 Data Quality Assessment")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="metric-icon">🛒</div>
            <div class="metric-value">{quality_report['unique_transactions']:,}</div>
            <div class="metric-label">Unique Transactions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="metric-icon">📦</div>
            <div class="metric-value">{quality_report['unique_products']:,}</div>
            <div class="metric-label">Unique Products</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="metric-icon">📊</div>
            <div class="metric-value">{quality_report['avg_items_per_transaction']:.1f}</div>
            <div class="metric-label">Avg Items/Transaction</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        quality_color = "🟢" if quality_report['quality_score'] > 80 else "🟡" if quality_report['quality_score'] > 60 else "🔴"
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="metric-icon">{quality_color}</div>
            <div class="metric-value">{quality_report['quality_score']:.0f}%</div>
            <div class="metric-label">Quality Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quality recommendations
    if quality_report['quality_score'] < 70:
        st.markdown("""
        <div class="warning-box-enhanced">
            <strong>⚠️ Data Quality Warning:</strong><br>
            Your data quality score is below 70%. Consider reviewing missing values and data consistency.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔙 Back to Upload", use_container_width=True):
            st.switch_page("pages/1_📁_Data_Upload.py")
    
    with col3:
        if st.button("➡️ Proceed to Data Processing", type="primary", use_container_width=True):
            st.switch_page("pages/3_🔄_Data_Processing.py")

else:
    st.markdown("""
    <div class="warning-box-enhanced">
        <strong>⚠️ Required columns missing!</strong><br>
        Please select both Transaction ID and Product columns to proceed.
    </div>
    """, unsafe_allow_html=True)

# Sidebar info
st.sidebar.markdown("### ⚙️ Column Mapping")
st.sidebar.info("""
**Current Step:** Configure Mapping

**Required Fields:**
- Transaction/Order ID
- Product/Item name

**Optional Fields:**
- Customer ID
- Price/Sales amount
- Quantity
- Category

**Auto-Detection:**
- Smart column detection
- Quality assessment
- Data validation
""")

if 'column_mapping' in st.session_state:
    st.sidebar.markdown("### ✅ Current Mapping")
    for key, value in st.session_state.column_mapping.items():
        if value:
            st.sidebar.write(f"**{key.replace('_', ' ').title()}:** {value}")
