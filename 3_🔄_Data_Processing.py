import streamlit as st
import pandas as pd
from utils.styles import load_custom_css
from utils.data_processor import DataProcessor

st.set_page_config(page_title="Data Processing", page_icon="🔄", layout="wide")
load_custom_css()

# Check prerequisites
if 'data' not in st.session_state or 'column_mapping' not in st.session_state:
    st.error("❌ Missing data or column mapping. Please complete previous steps.")
    if st.button("🔙 Go to Column Mapping"):
        st.switch_page("pages/2_⚙️_Column_Mapping.py")
    st.stop()

df = st.session_state.data
column_mapping = st.session_state.column_mapping

# Initialize data processor
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()

# Page header
st.markdown("""
<div class="page-header-enhanced">
    <h1>🔄 Data Processing</h1>
    <p>Clean and prepare your data for market basket analysis</p>
</div>
""", unsafe_allow_html=True)

# Processing interface
st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
st.subheader("🛠️ Data Preprocessing Pipeline")

# Processing configuration
col1, col2 = st.columns(2)

with col1:
    st.markdown("**⚙️ Processing Options:**")
    remove_duplicates = st.checkbox("Remove duplicate transactions", value=True)
    standardize_text = st.checkbox("Standardize product names", value=True)
    handle_quantities = st.checkbox("Expand quantities (if available)", value=True)

with col2:
    st.markdown("**📊 Quality Filters:**")
    min_transaction_size = st.slider("Minimum items per transaction:", 1, 10, 1)
    max_quantity_per_item = st.slider("Maximum quantity per item:", 1, 20, 10)

# Start processing
if st.button("🚀 Start Data Processing", type="primary", use_container_width=True):
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize processor with configuration
        processor = st.session_state.data_processor
        
        # Step 1: Basic processing
        status_text.text("Step 1/5: Extracting and mapping columns...")
        progress_bar.progress(20)
        
        success = processor.process_data(df, column_mapping)
        
        if not success:
            st.error("❌ Processing failed. Check the logs below.")
            st.stop()
        
        # Step 2: Apply user configurations
        status_text.text("Step 2/5: Applying processing options...")
        progress_bar.progress(40)
        
        processed_data = processor.processed_data
        
        # Step 3: Quality filtering
        status_text.text("Step 3/5: Applying quality filters...")
        progress_bar.progress(60)
        
        if min_transaction_size > 1:
            # Filter transactions by size
            transaction_sizes = processed_data['clean_df'].groupby('TransactionID').size()
            valid_transactions = transaction_sizes[transaction_sizes >= min_transaction_size].index
            processed_data['clean_df'] = processed_data['clean_df'][
                processed_data['clean_df']['TransactionID'].isin(valid_transactions)
            ]
            
            # Recreate transactions and basket encoding
            processed_data['transactions'] = processed_data['clean_df'].groupby('TransactionID')['Product'].apply(list).tolist()
            
            # Re-encode
            from mlxtend.preprocessing import TransactionEncoder
            te = TransactionEncoder()
            te_array = te.fit(processed_data['transactions']).transform(processed_data['transactions'])
            processed_data['basket_df'] = pd.DataFrame(te_array, columns=te.columns_)
        
        # Step 4: Final validation
        status_text.text("Step 4/5: Final validation...")
        progress_bar.progress(80)
        
        if len(processed_data['transactions']) == 0:
            st.error("❌ No valid transactions remain after processing. Try relaxing the filters.")
            st.stop()
        
        # Step 5: Store results
        status_text.text("Step 5/5: Finalizing...")
        progress_bar.progress(100)
        
        st.session_state.processed_data = processed_data
        st.session_state.current_step = 4
        
        progress_bar.empty()
        status_text.empty()
        
        st.markdown("""
        <div class="success-box-enhanced">
            <strong>✅ Data processing completed successfully!</strong><br>
            Your data is now ready for market basket analysis.
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.markdown(f"""
        <div class="error-box-enhanced">
            <strong>❌ Processing error:</strong><br>
            {str(e)}
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Show processing results
# Show processing results if available
if 'processed_data' in st.session_state:
    processed = st.session_state.processed_data
    
    # Processing summary
    st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
    st.subheader("📊 Processing Summary")
    
    # Get summary with None check
    summary = st.session_state.data_processor.get_processing_summary()
    
    if summary is not None:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card-enhanced">
                <div class="metric-icon">🛒</div>
                <div class="metric-value">{summary['total_transactions']:,}</div>
                <div class="metric-label">Final Transactions</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card-enhanced">
                <div class="metric-icon">📦</div>
                <div class="metric-value">{summary['unique_products']:,}</div>
                <div class="metric-label">Unique Products</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card-enhanced">
                <div class="metric-icon">📊</div>
                <div class="metric-value">{summary['avg_items_per_transaction']:.1f}</div>
                <div class="metric-label">Avg Items/Transaction</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card-enhanced">
                <div class="metric-icon">🎯</div>
                <div class="metric-value">{summary['sparsity']:.1f}%</div>
                <div class="metric-label">Data Density</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Processing steps log
        st.subheader("📋 Processing Steps")
        for step in summary['processing_steps']:
            st.write(f"- {step}")
    
    else:
        # Fallback when summary is None
        st.warning("⚠️ Processing summary not available. Please ensure data processing completed successfully.")
        
        # Show basic info from processed_data directly
        col1, col2, col3 = st.columns(3)
        
        with col1:
            transactions_count = len(processed.get('transactions', []))
            st.markdown(f"""
            <div class="metric-card-enhanced">
                <div class="metric-icon">🛒</div>
                <div class="metric-value">{transactions_count:,}</div>
                <div class="metric-label">Transactions</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            products_count = len(processed.get('basket_df', pd.DataFrame()).columns)
            st.markdown(f"""
            <div class="metric-card-enhanced">
                <div class="metric-icon">📦</div>
                <div class="metric-value">{products_count:,}</div>
                <div class="metric-label">Unique Products</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            data_rows = len(processed.get('clean_df', pd.DataFrame()))
            st.markdown(f"""
            <div class="metric-card-enhanced">
                <div class="metric-icon">📊</div>
                <div class="metric-value">{data_rows:,}</div>
                <div class="metric-label">Data Rows</div>
            </div>
            """, unsafe_allow_html=True)

    
    with col2:
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="metric-icon">📦</div>
            <div class="metric-value">{summary['unique_products']:,}</div>
            <div class="metric-label">Unique Products</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="metric-icon">📊</div>
            <div class="metric-value">{summary['avg_items_per_transaction']:.1f}</div>
            <div class="metric-label">Avg Items/Transaction</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="metric-icon">🎯</div>
            <div class="metric-value">{summary['sparsity']:.1f}%</div>
            <div class="metric-label">Data Density</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Processing steps log
    st.subheader("📋 Processing Steps")
    for step in summary['processing_steps']:
        st.write(f"- {step}")
    
    # Sample processed data
    st.subheader("📊 Processed Data Sample")
    st.dataframe(processed['clean_df'].head(10), use_container_width=True)
    
    # Transaction matrix preview
    st.subheader("🔢 Transaction Matrix Preview")
    st.write("Binary matrix showing product presence in transactions:")
    st.dataframe(processed['basket_df'].head(5), use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔙 Back to Mapping", use_container_width=True):
            st.switch_page("pages/2_⚙️_Column_Mapping.py")
    
    with col3:
        if st.button("➡️ Setup Analysis", type="primary", use_container_width=True):
            st.switch_page("pages/4_🤖_Analysis_Setup.py")

# Sidebar info
st.sidebar.markdown("### 🔄 Data Processing")
st.sidebar.info("""
**Current Step:** Process Data

**Processing Steps:**
- Extract mapped columns
- Clean and standardize data
- Remove missing values
- Handle quantities
- Create transaction matrix
- Apply quality filters

**Output:**
- Clean transaction data
- Encoded product matrix
- Ready for analysis
""")

if 'processed_data' in st.session_state:
    summary = st.session_state.data_processor.get_processing_summary()
    st.sidebar.markdown("### 📊 Current Status")
    st.sidebar.write(f"**Transactions:** {summary['total_transactions']:,}")
    st.sidebar.write(f"**Products:** {summary['unique_products']:,}")
    st.sidebar.write(f"**Density:** {summary['sparsity']:.1f}%")
