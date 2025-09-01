import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import load_custom_css

st.set_page_config(page_title="Results Dashboard", page_icon="📊", layout="wide")
load_custom_css()

# Check prerequisites
if 'analysis_results' not in st.session_state or not st.session_state.analysis_results:
    st.error("❌ No analysis results found. Please run the analysis first.")
    if st.button("🔙 Go to Analysis Setup"):
        st.switch_page("pages/4_🤖_Analysis_Setup.py")
    st.stop()

# Page header
st.markdown("""
<div class="page-header-enhanced">
    <h1>📊 Results Dashboard</h1>
    <p>Comprehensive view of your market basket analysis results</p>
</div>
""", unsafe_allow_html=True)

# Get analysis results
analysis_results = st.session_state.analysis_results
frequent_itemsets = analysis_results.get('frequent_itemsets', pd.DataFrame())
rules = analysis_results.get('rules', pd.DataFrame())
algorithm = analysis_results.get('algorithm', 'Unknown')
parameters = analysis_results.get('parameters', {})

# Results overview
st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
st.subheader("📈 Analysis Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    itemsets_count = len(frequent_itemsets) if not frequent_itemsets.empty else 0
    st.markdown(f"""
    <div class="metric-card-enhanced">
        <div class="metric-icon">📊</div>
        <div class="metric-value">{itemsets_count:,}</div>
        <div class="metric-label">Frequent Itemsets</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    rules_count = len(rules) if not rules.empty else 0
    st.markdown(f"""
    <div class="metric-card-enhanced">
        <div class="metric-icon">🔗</div>
        <div class="metric-value">{rules_count:,}</div>
        <div class="metric-label">Association Rules</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    max_support = frequent_itemsets['support'].max() if not frequent_itemsets.empty else 0
    st.markdown(f"""
    <div class="metric-card-enhanced">
        <div class="metric-icon">🎯</div>
        <div class="metric-value">{max_support:.3f}</div>
        <div class="metric-label">Highest Support</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    max_confidence = rules['confidence'].max() if not rules.empty else 0
    st.markdown(f"""
    <div class="metric-card-enhanced">
        <div class="metric-icon">🚀</div>
        <div class="metric-value">{max_confidence:.3f}</div>
        <div class="metric-label">Highest Confidence</div>
    </div>
    """, unsafe_allow_html=True)

# Analysis parameters
st.subheader("⚙️ Analysis Parameters")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info(f"**Algorithm**: {algorithm}")
with col2:
    st.info(f"**Min Support**: {parameters.get('min_support', 'N/A')}")
with col3:
    st.info(f"**Min Confidence**: {parameters.get('min_confidence', 'N/A')}")
with col4:
    st.info(f"**Min Lift**: {parameters.get('min_lift', 'N/A')}")

st.markdown('</div>', unsafe_allow_html=True)

# Frequent Itemsets Section
if not frequent_itemsets.empty:
    st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
    st.subheader("📊 Frequent Itemsets Analysis")
    
    # Controls for itemsets visualization
    col1, col2 = st.columns(2)
    with col1:
        max_itemsets_display = st.slider("Number of itemsets to display:", 5, min(50, len(frequent_itemsets)), 20)
    with col2:
        itemset_size_filter = st.multiselect(
            "Filter by itemset size:",
            options=sorted(frequent_itemsets['itemsets'].apply(len).unique()),
            default=sorted(frequent_itemsets['itemsets'].apply(len).unique())
        )
    
    # Filter itemsets
    if itemset_size_filter:
        filtered_itemsets = frequent_itemsets[frequent_itemsets['itemsets'].apply(len).isin(itemset_size_filter)]
    else:
        filtered_itemsets = frequent_itemsets
    
    # Top frequent itemsets visualization
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart of top itemsets
        top_itemsets = filtered_itemsets.head(max_itemsets_display).copy()
        top_itemsets['itemsets_str'] = top_itemsets['itemsets'].apply(lambda x: ', '.join(list(x)))
        top_itemsets['itemset_size'] = top_itemsets['itemsets'].apply(len)
        
        fig_itemsets = px.bar(
            top_itemsets,
            x='support',
            y='itemsets_str',
            orientation='h',
            title=f"Top {max_itemsets_display} Frequent Itemsets",
            color='itemset_size',
            color_continuous_scale='viridis',
            labels={'support': 'Support', 'itemsets_str': 'Itemsets'}
        )
        fig_itemsets.update_layout(
            height=500,
            yaxis={'categoryorder': 'total ascending'},
            showlegend=False
        )
        st.plotly_chart(fig_itemsets, use_container_width=True)
    
    with col2:
        # Support distribution
        fig_hist = px.histogram(
            filtered_itemsets,
            x='support',
            nbins=20,
            title="Support Distribution",
            labels={'support': 'Support', 'count': 'Number of Itemsets'}
        )
        fig_hist.update_layout(height=500)
        st.plotly_chart(fig_hist, use_container_width=True)
    
    # Itemset size analysis
    itemset_sizes = filtered_itemsets['itemsets'].apply(len)
    size_counts = itemset_sizes.value_counts().sort_index()
    
    fig_size = px.pie(
        values=size_counts.values,
        names=[f"{size}-item sets" for size in size_counts.index],
        title="Distribution of Itemset Sizes"
    )
    fig_size.update_layout(height=400)
    st.plotly_chart(fig_size, use_container_width=True)
    
    # Itemsets data table
    st.subheader("📋 Frequent Itemsets Table")
    display_itemsets = filtered_itemsets.head(max_itemsets_display).copy()
    display_itemsets['itemsets'] = display_itemsets['itemsets'].apply(lambda x: ', '.join(list(x)))
    display_itemsets['support'] = display_itemsets['support'].round(4)
    
    st.dataframe(
        display_itemsets[['itemsets', 'support']].rename(columns={
            'itemsets': 'Items',
            'support': 'Support'
        }),
        use_container_width=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Association Rules Section
if not rules.empty:
    st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
    st.subheader("🔗 Association Rules Analysis")
    
    # Controls for rules visualization
    col1, col2 = st.columns(2)
    with col1:
        max_rules_display = st.slider("Number of rules to display:", 5, min(50, len(rules)), 20)
    with col2:
        metric_color = st.selectbox("Color rules by:", ["lift", "confidence", "support"])
    
    # Rules scatter plot
    col1, col2 = st.columns(2)
    
    with col1:
        fig_scatter = px.scatter(
            rules.head(max_rules_display),
            x='confidence',
            y='lift',
            size='support',
            hover_data=['antecedents_str', 'consequents_str'],
            title="Association Rules: Confidence vs Lift",
            color=metric_color,
            color_continuous_scale='viridis',
            labels={
                'confidence': 'Confidence',
                'lift': 'Lift',
                'support': 'Support'
            }
        )
        fig_scatter.update_layout(height=500)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        # Rules metrics distribution
        fig_metrics = px.box(
            rules.head(100),
            y=['support', 'confidence', 'lift'],
            title="Rules Metrics Distribution"
        )
        fig_metrics.update_layout(height=500)
        st.plotly_chart(fig_metrics, use_container_width=True)
    
    # Top rules by different metrics
    st.subheader("🏆 Top Rules by Different Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**🎯 Highest Support**")
        top_support = rules.nlargest(5, 'support')[['antecedents_str', 'consequents_str', 'support']]
        for _, rule in top_support.iterrows():
            st.write(f"• {rule['antecedents_str']} → {rule['consequents_str']} ({rule['support']:.3f})")
    
    with col2:
        st.write("**🎯 Highest Confidence**")
        top_confidence = rules.nlargest(5, 'confidence')[['antecedents_str', 'consequents_str', 'confidence']]
        for _, rule in top_confidence.iterrows():
            st.write(f"• {rule['antecedents_str']} → {rule['consequents_str']} ({rule['confidence']:.3f})")
    
    with col3:
        st.write("**🎯 Highest Lift**")
        top_lift = rules.nlargest(5, 'lift')[['antecedents_str', 'consequents_str', 'lift']]
        for _, rule in top_lift.iterrows():
            st.write(f"• {rule['antecedents_str']} → {rule['consequents_str']} ({rule['lift']:.3f})")
    
    # Rules data table
    st.subheader("📋 Association Rules Table")
    
    # Search functionality
    search_term = st.text_input("🔍 Search for specific products in rules:", placeholder="e.g., milk, bread")
    
    display_rules = rules.head(max_rules_display).copy()
    
    if search_term:
        mask = (
            display_rules['antecedents_str'].str.contains(search_term, case=False, na=False) |
            display_rules['consequents_str'].str.contains(search_term, case=False, na=False)
        )
        display_rules = display_rules[mask]
        
        if len(display_rules) > 0:
            st.success(f"Found {len(display_rules)} rules containing '{search_term}'")
        else:
            st.warning(f"No rules found containing '{search_term}'")
    
    if len(display_rules) > 0:
        # Round numeric columns
        numeric_columns = ['support', 'confidence', 'lift']
        for col in numeric_columns:
            display_rules[col] = display_rules[col].round(4)
        
        st.dataframe(
            display_rules[['antecedents_str', 'consequents_str', 'support', 'confidence', 'lift']].rename(columns={
                'antecedents_str': 'Antecedents (If)',
                'consequents_str': 'Consequents (Then)',
                'support': 'Support',
                'confidence': 'Confidence',
                'lift': 'Lift'
            }),
            use_container_width=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
    st.warning("⚠️ No association rules were generated with the current parameters. Try lowering the confidence and lift thresholds.")
    st.markdown('</div>', unsafe_allow_html=True)

# Quick insights
st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
st.subheader("💡 Quick Insights")

insights = []

if not frequent_itemsets.empty:
    # Most popular single items
    single_items = frequent_itemsets[frequent_itemsets['itemsets'].apply(len) == 1]
    if not single_items.empty:
        most_popular = single_items.iloc[0]
        insights.append(f"📊 **Most popular single item**: {', '.join(list(most_popular['itemsets']))} (Support: {most_popular['support']:.3f})")
    
    # Largest frequent itemset
    largest_itemset = frequent_itemsets.loc[frequent_itemsets['itemsets'].apply(len).idxmax()]
    insights.append(f"📦 **Largest frequent itemset**: {', '.join(list(largest_itemset['itemsets']))} ({len(largest_itemset['itemsets'])} items)")

if not rules.empty:
    # Strongest rule by confidence
    strongest_rule = rules.iloc[0]
    insights.append(f"🎯 **Strongest rule**: {strongest_rule['antecedents_str']} → {strongest_rule['consequents_str']} (Confidence: {strongest_rule['confidence']:.3f})")
    
    # Highest lift rule
    highest_lift = rules.loc[rules['lift'].idxmax()]
    insights.append(f"🚀 **Highest lift rule**: {highest_lift['antecedents_str']} → {highest_lift['consequents_str']} (Lift: {highest_lift['lift']:.3f})")

for insight in insights:
    st.write(insight)

if not insights:
    st.info("Run the analysis to see insights about your data patterns.")

st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🔙 Back to Analysis", use_container_width=True):
        st.switch_page("pages/4_🤖_Analysis_Setup.py")

with col2:
    if st.button("📈 Advanced Visualizations", use_container_width=True):
        st.switch_page("pages/6_📈_Advanced_Visualizations.py")

with col3:
    if st.button("➡️ Business Insights", type="primary", use_container_width=True):
        st.switch_page("pages/7_💡_Business_Insights.py")

# Update session state
st.session_state.current_step = max(st.session_state.current_step, 5)

# Sidebar info
st.sidebar.markdown("### 📊 Results Dashboard")
st.sidebar.info("""
**Current Step:** View Results

**Dashboard Features:**
- Frequent itemsets analysis
- Association rules exploration
- Interactive visualizations
- Search and filtering
- Quick insights

**Key Metrics:**
- Support: Item frequency
- Confidence: Rule strength
- Lift: Association power
""")

if analysis_results:
    st.sidebar.markdown("### 📈 Current Results")
    itemsets_count = len(frequent_itemsets) if not frequent_itemsets.empty else 0
    rules_count = len(rules) if not rules.empty else 0
    st.sidebar.write(f"**Frequent Itemsets:** {itemsets_count:,}")
    st.sidebar.write(f"**Association Rules:** {rules_count:,}")
    st.sidebar.write(f"**Algorithm Used:** {algorithm}")
