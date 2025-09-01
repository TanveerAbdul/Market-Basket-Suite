import streamlit as st
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
from utils.styles import load_custom_css
import pandas as pd

st.set_page_config(page_title="Analysis Setup", page_icon="🤖", layout="wide")
load_custom_css()

# Check prerequisites
if 'processed_data' not in st.session_state:
    st.error("❌ No processed data found. Please complete data processing first.")
    if st.button("🔙 Go to Data Processing"):
        st.switch_page("pages/3_🔄_Data_Processing.py")
    st.stop()

processed = st.session_state.processed_data

# Page header
st.markdown("""
<div class="page-header-enhanced">
    <h1>🤖 Analysis Setup</h1>
    <p>Configure algorithm parameters and run market basket analysis</p>
</div>
""", unsafe_allow_html=True)

# Algorithm selection and parameter configuration
st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
st.subheader("⚙️ Algorithm Configuration")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔍 Algorithm Selection")
    algorithm = st.selectbox(
        "Choose Algorithm:",
        ["Apriori", "FP-Growth"],
        help="Apriori: Classic algorithm, works well with smaller datasets\nFP-Growth: Faster for larger datasets"
    )
    
    st.markdown("### 📊 Support Configuration")
    # Smart support suggestion based on dataset size
    total_transactions = len(processed['transactions'])
    suggested_support = max(0.001, min(0.05, 20 / total_transactions))
    
    min_support = st.slider(
        "Minimum Support:",
        min_value=0.001,
        max_value=0.1,
        value=suggested_support,
        step=0.001,
        format="%.3f",
        help=f"Suggested: {suggested_support:.3f} based on {total_transactions:,} transactions"
    )
    
    st.info(f"This will find itemsets that appear in at least {int(min_support * total_transactions)} transactions")

with col2:
    st.markdown("### 🎯 Rule Thresholds")
    
    min_confidence = st.slider(
        "Minimum Confidence:",
        min_value=0.1,
        max_value=1.0,
        value=0.3,
        step=0.05,
        format="%.2f",
        help="Probability that consequent is bought when antecedent is bought"
    )
    
    min_lift = st.slider(
        "Minimum Lift:",
        min_value=1.0,
        max_value=5.0,
        value=1.2,
        step=0.1,
        format="%.1f",
        help="How much more likely the consequent is bought when antecedent is bought"
    )
    
    st.markdown("### 📈 Advanced Options")
    max_len = st.slider(
        "Maximum Itemset Length:",
        min_value=2,
        max_value=8,
        value=4,
        help="Maximum number of items in an itemset"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Parameter explanation
st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
st.subheader("📚 Parameter Guide")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🎯 Support**
    - Measures how frequently an itemset appears
    - Higher values = more common patterns
    - Lower values = discover rare patterns
    - Range: 0.001 (0.1%) to 0.1 (10%)
    """)

with col2:
    st.markdown("""
    **🎯 Confidence**
    - Measures rule reliability
    - Higher values = stronger rules
    - 0.5 = 50% chance consequent bought
    - Range: 0.1 (10%) to 1.0 (100%)
    """)

with col3:
    st.markdown("""
    **🎯 Lift**
    - Measures association strength
    - 1.0 = no association
    - >1.0 = positive association
    - <1.0 = negative association
    """)

st.markdown('</div>', unsafe_allow_html=True)

# Run analysis
st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
st.subheader("🚀 Execute Analysis")

# Estimated runtime
estimated_time = "< 1 minute" if total_transactions < 1000 else "1-3 minutes" if total_transactions < 10000 else "3-10 minutes"
st.info(f"📊 **Dataset Info**: {total_transactions:,} transactions, {len(processed['basket_df'].columns):,} products  \n⏱️ **Estimated Runtime**: {estimated_time}")

if st.button("🔥 Execute Market Basket Analysis", type="primary", use_container_width=True):
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Find frequent itemsets
        status_text.text(f"Step 1/3: Running {algorithm} algorithm...")
        progress_bar.progress(33)
        
        if algorithm == "Apriori":
            frequent_itemsets = apriori(
                processed['basket_df'], 
                min_support=min_support, 
                use_colnames=True,
                max_len=max_len
            )
        else:  # FP-Growth
            frequent_itemsets = fpgrowth(
                processed['basket_df'], 
                min_support=min_support, 
                use_colnames=True,
                max_len=max_len
            )
        
        if len(frequent_itemsets) == 0:
            progress_bar.empty()
            status_text.empty()
            st.warning("⚠️ No frequent itemsets found. Try lowering the support threshold.")
            st.stop()
        
        # Step 2: Generate association rules
        status_text.text("Step 2/3: Generating association rules...")
        progress_bar.progress(66)
        
        rules = association_rules(
            frequent_itemsets, 
            metric="confidence", 
            min_threshold=min_confidence
        )
        
        # Filter by lift
        rules = rules[rules['lift'] >= min_lift]
        
        if len(rules) == 0:
            st.warning("⚠️ No association rules found with current thresholds.")
            rules_found = False
        else:
            rules_found = True
            
            # Sort by confidence and lift
            rules = rules.sort_values(['confidence', 'lift'], ascending=False)
            
            # Add string representations for display
            rules['antecedents_str'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
            rules['consequents_str'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
        
        # Step 3: Store results
        status_text.text("Step 3/3: Preparing results...")
        progress_bar.progress(100)
        
        st.session_state.analysis_results = {
            'frequent_itemsets': frequent_itemsets,
            'rules': rules if rules_found else pd.DataFrame(),
            'algorithm': algorithm,
            'parameters': {
                'min_support': min_support,
                'min_confidence': min_confidence,
                'min_lift': min_lift,
                'max_len': max_len
            }
        }
        
        st.session_state.current_step = 5
        st.session_state.analysis_complete = True
        st.session_state.export_ready = True
        
        progress_bar.empty()
        status_text.empty()
        
        # Success message
        if rules_found:
            st.markdown(f"""
            <div class="success-box-enhanced">
                <strong>✅ Analysis completed successfully!</strong><br>
                Found {len(frequent_itemsets)} frequent itemsets and {len(rules)} association rules using {algorithm}.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="warning-box-enhanced">
                <strong>⚠️ Partial success!</strong><br>
                Found {len(frequent_itemsets)} frequent itemsets but no association rules with current thresholds.
            </div>
            """, unsafe_allow_html=True)
        
        # Quick results preview
        st.subheader("📊 Quick Results Preview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card-enhanced">
                <div class="metric-icon">📊</div>
                <div class="metric-value">{len(frequent_itemsets)}</div>
                <div class="metric-label">Frequent Itemsets</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            rules_count = len(rules) if rules_found else 0
            st.markdown(f"""
            <div class="metric-card-enhanced">
                <div class="metric-icon">🔗</div>
                <div class="metric-value">{rules_count}</div>
                <div class="metric-label">Association Rules</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            max_support = frequent_itemsets['support'].max()
            st.markdown(f"""
            <div class="metric-card-enhanced">
                <div class="metric-icon">🎯</div>
                <div class="metric-value">{max_support:.3f}</div>
                <div class="metric-label">Max Support</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            max_lift = rules['lift'].max() if rules_found else 0
            st.markdown(f"""
            <div class="metric-card-enhanced">
                <div class="metric-icon">🚀</div>
                <div class="metric-value">{max_lift:.2f}</div>
                <div class="metric-label">Max Lift</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Show top results
        if len(frequent_itemsets) > 0:
            st.subheader("🔝 Top Frequent Itemsets")
            display_itemsets = frequent_itemsets.head(5).copy()
            display_itemsets['itemsets'] = display_itemsets['itemsets'].apply(lambda x: ', '.join(list(x)))
            st.dataframe(
                display_itemsets[['itemsets', 'support']].rename(columns={
                    'itemsets': 'Items',
                    'support': 'Support'
                }), 
                use_container_width=True
            )
        
        if rules_found and len(rules) > 0:
            st.subheader("🔝 Top Association Rules")
            display_rules = rules.head(5)[['antecedents_str', 'consequents_str', 'support', 'confidence', 'lift']].copy()
            display_rules.columns = ['Antecedents (If)', 'Consequents (Then)', 'Support', 'Confidence', 'Lift']
            display_rules = display_rules.round(4)
            st.dataframe(display_rules, use_container_width=True)
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.markdown(f"""
        <div class="error-box-enhanced">
            <strong>❌ Analysis error:</strong><br>
            {str(e)}
            <br><br>
            <strong>Troubleshooting tips:</strong><br>
            • Try lowering the minimum support threshold<br>
            • Ensure your dataset has sufficient transactions<br>
            • Check that products appear in multiple transactions
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Navigation buttons
if 'analysis_results' in st.session_state:
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔙 Back to Processing", use_container_width=True):
            st.switch_page("pages/3_🔄_Data_Processing.py")
    
    with col3:
        if st.button("➡️ View Results", type="primary", use_container_width=True):
            st.switch_page("pages/5_📊_Results_Dashboard.py")

# Sidebar info
st.sidebar.markdown("### 🤖 Analysis Setup")
st.sidebar.info("""
**Current Step:** Configure & Execute Analysis

**Algorithm Options:**
- **Apriori**: Classic, reliable
- **FP-Growth**: Fast, efficient

**Key Parameters:**
- **Support**: Item frequency
- **Confidence**: Rule strength  
- **Lift**: Association power

**Tips:**
- Start with suggested values
- Lower support for rare patterns
- Higher confidence for reliable rules
""")

if 'analysis_results' in st.session_state:
    params = st.session_state.analysis_results.get('parameters', {})
    st.sidebar.markdown("### ⚙️ Current Settings")
    st.sidebar.write(f"**Algorithm:** {st.session_state.analysis_results.get('algorithm', 'Unknown')}")
    st.sidebar.write(f"**Min Support:** {params.get('min_support', 'N/A') if params.get('min_support') is None else f'{params.get('min_support'):.3f}'}")
    st.sidebar.write(f"**Min Confidence:** {params.get('min_confidence', 'N/A') if params.get('min_confidence') is None else f'{params.get('min_confidence'):.2f}'}")
    st.sidebar.write(f"**Min Lift:** {params.get('min_lift', 'N/A') if params.get('min_lift') is None else f'{params.get('min_lift'):.1f}'}")

