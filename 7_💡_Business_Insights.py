import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import load_custom_css
import numpy as np

st.set_page_config(page_title="Business Insights", page_icon="💡", layout="wide")
load_custom_css()

# Check prerequisites
if 'analysis_results' not in st.session_state or not st.session_state.analysis_results:
    st.error("❌ No analysis results found. Please run the analysis first.")
    if st.button("🔙 Go to Results Dashboard"):
        st.switch_page("pages/5_📊_Results_Dashboard.py")
    st.stop()

# Page header
st.markdown("""
<div class="page-header-enhanced">
    <h1>💡 Business Insights & Recommendations</h1>
    <p>Actionable insights and strategic recommendations for your business</p>
</div>
""", unsafe_allow_html=True)

# Get analysis results
analysis_results = st.session_state.analysis_results
frequent_itemsets = analysis_results.get('frequent_itemsets', pd.DataFrame())
rules = analysis_results.get('rules', pd.DataFrame())
processed_data = st.session_state.get('processed_data', {})

# Strategic Insights
st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
st.subheader("🎯 Strategic Business Insights")

if not rules.empty:
    # Top cross-selling opportunities
    st.markdown("### 🛍️ Top Cross-Selling Opportunities")
    
    top_rules = rules.head(10)
    
    for i, (_, rule) in enumerate(top_rules.iterrows(), 1):
        antecedents = rule['antecedents_str']
        consequents = rule['consequents_str']
        confidence = rule['confidence']
        lift = rule['lift']
        support = rule['support']
        
        # Determine strength level
        if lift >= 2.0:
            strength_emoji = "🔥"
            strength_text = "Very Strong"
        elif lift >= 1.5:
            strength_emoji = "💪"
            strength_text = "Strong"
        else:
            strength_emoji = "👍"
            strength_text = "Moderate"
        
        st.markdown(f"""
        **{i}. {antecedents} → {consequents}** {strength_emoji}
        - **Strength**: {strength_text} (Lift: {lift:.2f}x)
        - **Reliability**: {confidence:.1%} of customers who buy {antecedents} also buy {consequents}
        - **Frequency**: Found in {support:.1%} of all transactions
        - **💰 Business Impact**: Customers buying {antecedents} are {lift:.1f}x more likely to buy {consequents}
        """)
        
        # Add separator except for last item
        if i < len(top_rules):
            st.markdown("---")

st.markdown('</div>', unsafe_allow_html=True)

# Revenue Impact Analysis
if 'clean_df' in processed_data:
    st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
    st.subheader("💰 Revenue Impact Analysis")
    
    clean_df = processed_data['clean_df']
    total_transactions = len(clean_df['TransactionID'].unique())
    
    # Calculate potential impact
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Current Performance")
        
        avg_items_per_transaction = len(clean_df) / total_transactions
        unique_products = clean_df['Product'].nunique()
        
        # If price data is available
        if 'Price' in clean_df.columns:
            avg_transaction_value = clean_df.groupby('TransactionID')['Price'].sum().mean()
            total_revenue = clean_df['Price'].sum()
            
            st.metric("Average Transaction Value", f"₹{avg_transaction_value:.2f}")
            st.metric("Total Revenue", f"₹{total_revenue:,.2f}")
        
        st.metric("Average Items per Transaction", f"{avg_items_per_transaction:.2f}")
        st.metric("Total Transactions", f"{total_transactions:,}")
        st.metric("Unique Products", f"{unique_products:,}")
    
    with col2:
        st.markdown("### 🚀 Projected Impact")
        
        # Calculate potential improvements based on rules
        if not rules.empty:
            # Conservative estimates
            basket_size_increase = 15  # 15% increase in basket size
            cross_sell_success_rate = 25  # 25% success rate for cross-selling
            
            projected_basket_increase = avg_items_per_transaction * (basket_size_increase / 100)
            
            if 'Price' in clean_df.columns:
                potential_additional_revenue = avg_transaction_value * total_transactions * (basket_size_increase / 100)
                st.metric(
                    "Potential Additional Revenue", 
                    f"₹{potential_additional_revenue:,.2f}",
                    f"+{basket_size_increase}% basket size"
                )
            
            st.metric(
                "Projected Basket Size", 
                f"{avg_items_per_transaction + projected_basket_increase:.2f}",
                f"+{projected_basket_increase:.2f} items"
            )
            
            # Rules implementation success metrics
            implementable_rules = len(rules[rules['confidence'] >= 0.3])
            st.metric("Implementable Rules", f"{implementable_rules}", "Confidence ≥ 30%")
            
            high_impact_rules = len(rules[rules['lift'] >= 1.5])
            st.metric("High-Impact Rules", f"{high_impact_rules}", "Lift ≥ 1.5")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Product Performance Analysis
st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
st.subheader("📦 Product Performance Analysis")

if not frequent_itemsets.empty and 'clean_df' in processed_data:
    clean_df = processed_data['clean_df']
    
    # Product popularity analysis
    product_counts = clean_df['Product'].value_counts().head(15)
    
    # Combine with frequent itemsets data
    single_items = frequent_itemsets[frequent_itemsets['itemsets'].apply(len) == 1].copy()
    single_items['product'] = single_items['itemsets'].apply(lambda x: list(x)[0])
    
    # Create comprehensive product analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Top products by frequency
        fig_products = px.bar(
            x=product_counts.values,
            y=product_counts.index,
            orientation='h',
            title="Top 15 Products by Transaction Frequency",
            labels={'x': 'Number of Transactions', 'y': 'Product'}
        )
        fig_products.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_products, use_container_width=True)
    
    with col2:
        # Support vs Frequency analysis
        if not single_items.empty:
            # Merge frequency data with support data
            freq_support_data = []
            for _, item in single_items.iterrows():
                product_name = item['product']
                if product_name in product_counts:
                    freq_support_data.append({
                        'Product': product_name,
                        'Frequency': product_counts[product_name],
                        'Support': item['support']
                    })
            
            if freq_support_data:
                freq_support_df = pd.DataFrame(freq_support_data)
                
                fig_support = px.scatter(
                    freq_support_df,
                    x='Frequency',
                    y='Support',
                    title="Product Frequency vs Support",
                    hover_data=['Product'],
                    labels={'Frequency': 'Transaction Count', 'Support': 'Support Value'}
                )
                fig_support.update_layout(height=500)
                st.plotly_chart(fig_support, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Actionable Recommendations
st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
st.subheader("📋 Actionable Business Recommendations")

# Generate recommendations based on analysis
recommendations = []

if not rules.empty:
    # Product bundling recommendations
    strong_rules = rules[rules['lift'] >= 1.5]
    if not strong_rules.empty:
        recommendations.extend([
            {
                "category": "🛍️ Product Bundling",
                "priority": "High",
                "action": "Create product bundles based on strong association rules",
                "details": f"Implement {len(strong_rules)} high-lift product combinations as bundles",
                "expected_impact": "15-25% increase in average basket size",
                "implementation": "Bundle products with lift ≥ 1.5 and offer 5-10% discount"
            },
            {
                "category": "📍 Store Layout Optimization",
                "priority": "High", 
                "action": "Reorganize store layout based on product associations",
                "details": "Place frequently associated products in proximity or same aisle",
                "expected_impact": "Reduce customer search time, increase impulse purchases",
                "implementation": "Use top 20 association rules for layout decisions"
            }
        ])
    
    # Marketing recommendations
    high_confidence_rules = rules[rules['confidence'] >= 0.4]
    if not high_confidence_rules.empty:
        recommendations.extend([
            {
                "category": "🎯 Targeted Marketing",
                "priority": "Medium",
                "action": "Implement personalized product recommendations",
                "details": f"Use {len(high_confidence_rules)} high-confidence rules for recommendations",
                "expected_impact": "20-30% increase in cross-sell success rate",
                "implementation": "Email campaigns and website recommendation engine"
            },
            {
                "category": "🏷️ Dynamic Pricing Strategy",
                "priority": "Medium",
                "action": "Implement strategic discount pricing on antecedent products",
                "details": "Offer discounts on antecedent items to drive consequent item sales",
                "expected_impact": "Higher overall transaction value despite discounts",
                "implementation": "A/B test discount strategies on top 10 rules"
            }
        ])

# Inventory and operations recommendations
if 'clean_df' in processed_data:
    recommendations.extend([
        {
            "category": "📦 Inventory Management",
            "priority": "High",
            "action": "Synchronize inventory for associated products",
            "details": "Ensure complementary products are stocked together",
            "expected_impact": "Reduce stockouts, improve customer satisfaction",
            "implementation": "Adjust reorder points based on association patterns"
        },
        {
            "category": "📊 Performance Monitoring",
            "priority": "Low",
            "action": "Track basket size and cross-sell metrics",
            "details": "Monitor success rate of implemented recommendations",
            "expected_impact": "Data-driven optimization of strategies",
            "implementation": "Weekly dashboard tracking key metrics"
        }
    ])

# Display recommendations
priority_colors = {
    "High": "🔴",
    "Medium": "🟡", 
    "Low": "🟢"
}

for i, rec in enumerate(recommendations, 1):
    priority_color = priority_colors.get(rec["priority"], "⚪")
    
    st.markdown(f"""
    ### {i}. {rec["category"]} {priority_color}
    
    **Priority**: {rec["priority"]}
    
    **Action**: {rec["action"]}
    
    **Details**: {rec["details"]}
    
    **Expected Impact**: {rec["expected_impact"]}
    
    **Implementation**: {rec["implementation"]}
    """)
    
    if i < len(recommendations):
        st.markdown("---")

st.markdown('</div>', unsafe_allow_html=True)

# Implementation Timeline
st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
st.subheader("📅 Implementation Timeline")

timeline_data = {
    "Week 1-2": ["Analyze top association rules", "Plan product bundling strategy"],
    "Week 3-4": ["Implement store layout changes", "Launch first product bundles"],
    "Week 5-6": ["Deploy recommendation engine", "Start targeted email campaigns"],
    "Week 7-8": ["Implement dynamic pricing", "Monitor and measure results"],
    "Week 9-12": ["Optimize based on results", "Scale successful strategies"]
}

for period, tasks in timeline_data.items():
    st.markdown(f"**{period}**")
    for task in tasks:
        st.write(f"• {task}")
    st.write("")

st.markdown('</div>', unsafe_allow_html=True)

# Key Performance Indicators (KPIs)
st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
st.subheader("📈 Key Performance Indicators to Track")

kpi_categories = {
    "🛒 Basket Metrics": [
        "Average items per transaction",
        "Average transaction value",
        "Basket size distribution"
    ],
    "🔗 Cross-Selling Metrics": [
        "Cross-sell success rate",
        "Revenue from cross-sold items",
        "Customer response to recommendations"
    ],
    "📊 Operational Metrics": [
        "Inventory turnover for bundled products",
        "Customer satisfaction scores",
        "Time spent in store/on website"
    ],
    "💰 Financial Metrics": [
        "Total revenue growth",
        "Profit margin improvement",
        "Return on marketing investment"
    ]
}

col1, col2 = st.columns(2)
col_items = list(kpi_categories.items())

for i, (category, kpis) in enumerate(col_items):
    target_col = col1 if i % 2 == 0 else col2
    
    with target_col:
        st.markdown(f"**{category}**")
        for kpi in kpis:
            st.write(f"• {kpi}")
        st.write("")

st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🔙 Back to Results", use_container_width=True):
        st.switch_page("pages/5_📊_Results_Dashboard.py")

with col2:
    if st.button("📈 Advanced Visualizations", use_container_width=True):
        st.switch_page("pages/6_📈_Advanced_Visualizations.py")

with col3:
    if st.button("📥 Download Results", type="primary", use_container_width=True):
        st.switch_page("pages/8_📥_Download_Center.py")

# Update session state
st.session_state.current_step = max(st.session_state.current_step, 7)

# Sidebar info
st.sidebar.markdown("### 💡 Business Insights")
st.sidebar.success("""
**Current Step:** Strategic Insights

**Key Features:**
- Cross-selling opportunities
- Revenue impact analysis
- Product performance insights
- Actionable recommendations
- Implementation timeline
- KPI tracking guide

**Business Value:**
- Increase average basket size
- Improve cross-sell success
- Optimize store operations
- Drive revenue growth
""")

if analysis_results:
    st.sidebar.markdown("### 📊 Analysis Summary")
    itemsets_count = len(frequent_itemsets) if not frequent_itemsets.empty else 0
    rules_count = len(rules) if not rules.empty else 0
    implementable_rules = len(rules[rules['confidence'] >= 0.3]) if not rules.empty else 0
    
    st.sidebar.write(f"**Total Rules:** {rules_count:,}")
    st.sidebar.write(f"**Implementable Rules:** {implementable_rules:,}")
    st.sidebar.write(f"**Frequent Itemsets:** {itemsets_count:,}")
    
    if not rules.empty:
        avg_lift = rules['lift'].mean()
        st.sidebar.write(f"**Average Lift:** {avg_lift:.2f}")
