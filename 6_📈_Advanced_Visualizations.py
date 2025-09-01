import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import numpy as np
from plotly.subplots import make_subplots
from utils.styles import load_custom_css

st.set_page_config(page_title="Advanced Visualizations", page_icon="📈", layout="wide")
load_custom_css()

# Check prerequisites
if 'analysis_results' not in st.session_state or not st.session_state.analysis_results:
    st.error("❌ No analysis results found. Please complete the analysis first.")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔙 Go to Analysis Setup", use_container_width=True):
            st.switch_page("pages/4_🤖_Analysis_Setup.py")
    st.stop()

# Page header
st.markdown("""
<div class="page-header-enhanced">
    <h1>📈 Advanced Visualizations</h1>
    <p>Interactive charts and network graphs for comprehensive market basket analysis</p>
</div>
""", unsafe_allow_html=True)

# Get data
analysis_results = st.session_state.analysis_results
frequent_itemsets = analysis_results.get('frequent_itemsets', pd.DataFrame())
rules = analysis_results.get('rules', pd.DataFrame())

# Visualization controls
st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
st.subheader("🎛️ Visualization Controls")

col1, col2, col3 = st.columns(3)

with col1:
    viz_theme = st.selectbox("Chart Theme:", ["plotly", "plotly_white", "plotly_dark", "seaborn"])
with col2:
    color_scheme = st.selectbox("Color Palette:", ["viridis", "plasma", "blues", "reds", "rainbow"])
with col3:
    if not frequent_itemsets.empty:
        max_possible = min(50, len(frequent_itemsets))
        default_max = min(20, max_possible)
        max_items = st.slider("Max Items to Display:", 10, max_possible, default_max)
    else:
        max_items = 20
        st.info("No frequent itemsets available")

st.markdown('</div>', unsafe_allow_html=True)

# Visualization sections
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Itemsets Analysis", "🔗 Rules Analysis", "🕸️ Network Graph", "📈 Metrics Dashboard", "🎯 Interactive Explorer"])

# Tab 1: Itemsets Analysis
with tab1:
    if not frequent_itemsets.empty:
        st.markdown('<div class="viz-container">', unsafe_allow_html=True)
        st.markdown("### 📊 Frequent Itemsets Visualization")
        
        # Support distribution
        col1, col2 = st.columns(2)
        
        with col1:
            fig_hist = px.histogram(
                frequent_itemsets, 
                x='support', 
                nbins=20,
                title="Support Distribution",
                template=viz_theme,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_hist.update_layout(title_font=dict(size=16), height=400)
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Top itemsets bar chart
            top_itemsets = frequent_itemsets.head(max_items).copy()
            top_itemsets['itemsets_str'] = top_itemsets['itemsets'].apply(lambda x: ', '.join(list(x)))
            top_itemsets['itemset_size'] = top_itemsets['itemsets'].apply(len)
            
            fig_bar = px.bar(
                top_itemsets,
                x='support',
                y='itemsets_str',
                orientation='h',
                title=f"Top {max_items} Frequent Itemsets",
                template=viz_theme,
                color='itemset_size',
                color_continuous_scale=color_scheme
            )
            fig_bar.update_layout(title_font=dict(size=16), height=400, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Itemset size analysis
        itemset_sizes = frequent_itemsets['itemsets'].apply(len)
        size_counts = itemset_sizes.value_counts().sort_index()
        
        fig_pie = px.pie(
            values=size_counts.values,
            names=[f"{size}-item sets" for size in size_counts.index],
            title="Distribution of Itemset Sizes",
            template=viz_theme,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_layout(title_font=dict(size=16), height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No frequent itemsets data available for visualization.")

# Tab 2: Rules Analysis
with tab2:
    if not rules.empty:
        st.markdown('<div class="viz-container">', unsafe_allow_html=True)
        st.markdown("### 🔗 Association Rules Analysis")
        
        # Rules scatter plot matrix
        fig_scatter = px.scatter_matrix(
            rules[['support', 'confidence', 'lift']].head(100),
            title="Rules Metrics Correlation Matrix",
            template=viz_theme,
            color_discrete_sequence=[px.colors.qualitative.Set1]
        )
        fig_scatter.update_layout(title_font=dict(size=16), height=600)
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # 3D scatter plot
        col1, col2 = st.columns(2)
        
        with col1:
            fig_3d = px.scatter_3d(
                rules.head(100),
                x='support',
                y='confidence',
                z='lift',
                size='support',
                hover_name='antecedents_str',
                title="3D Rules Visualization",
                template=viz_theme,
                color='lift',
                color_continuous_scale=color_scheme
            )
            fig_3d.update_layout(title_font=dict(size=16), height=500)
            st.plotly_chart(fig_3d, use_container_width=True)
        
        with col2:
            # Confidence vs Lift with support as size
            fig_bubble = px.scatter(
                rules.head(50),
                x='confidence',
                y='lift',
                size='support',
                hover_data=['antecedents_str', 'consequents_str'],
                title="Rules Bubble Chart",
                template=viz_theme,
                color='lift',
                color_continuous_scale=color_scheme
            )
            fig_bubble.update_layout(title_font=dict(size=16), height=500)
            st.plotly_chart(fig_bubble, use_container_width=True)
        
        # Rules strength heatmap
        if len(rules) > 10:
            top_rules = rules.head(20)
            heatmap_data = top_rules[['support', 'confidence', 'lift']].values
            
            fig_heatmap = px.imshow(
                heatmap_data.T,
                x=[f"Rule {i+1}" for i in range(len(top_rules))],
                y=['Support', 'Confidence', 'Lift'],
                title="Rules Strength Heatmap",
                template=viz_theme,
                color_continuous_scale=color_scheme,
                aspect='auto'
            )
            fig_heatmap.update_layout(title_font=dict(size=16), height=300)
            st.plotly_chart(fig_heatmap, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No association rules data available for visualization.")

# Tab 3: Network Graph
with tab3:
    if not rules.empty:
        st.markdown('<div class="viz-container">', unsafe_allow_html=True)
        st.markdown("### 🕸️ Interactive Network Graph")
        
        # Network controls
        col1, col2, col3 = st.columns(3)
        with col1:
            max_network_size = min(50, len(rules))
            default_network_size = min(25, max_network_size)
            min_network_size = min(10, max_network_size)
            network_size = st.slider("Network Size:", min_network_size, max_network_size, default_network_size)
        with col2:
            layout_type = st.selectbox("Layout:", ["spring", "circular", "kamada_kawai", "shell"])
        with col3:
            node_size_metric = st.selectbox("Node Size Based On:", ["degree", "support", "uniform"])
        
        # Create network
        top_rules_network = rules.head(network_size)
        
        G = nx.DiGraph()
        
        # Add nodes and edges
        for _, rule in top_rules_network.iterrows():
            antecedents = ', '.join(list(rule['antecedents']))
            consequents = ', '.join(list(rule['consequents']))
            
            G.add_edge(antecedents, consequents, 
                      weight=rule['confidence'], 
                      lift=rule['lift'],
                      support=rule['support'])
        
        # Choose layout
        if layout_type == "spring":
            pos = nx.spring_layout(G, k=3, iterations=50)
        elif layout_type == "circular":
            pos = nx.circular_layout(G)
        elif layout_type == "kamada_kawai":
            pos = nx.kamada_kawai_layout(G)
        else:
            pos = nx.shell_layout(G)
        
        # Create plotly network graph
        edge_x, edge_y = [], []
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='rgba(125, 125, 125, 0.5)'),
            hoverinfo='none',
            mode='lines'
        )
        
        node_x, node_y = [], []
        node_text = []
        node_size = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            
            if node_size_metric == "degree":
                node_size.append(G.degree(node) * 10 + 20)
            elif node_size_metric == "support":
                max_support = 0
                for _, rule in top_rules_network.iterrows():
                    if node in [', '.join(list(rule['antecedents'])), ', '.join(list(rule['consequents']))]:
                        max_support = max(max_support, rule['support'])
                node_size.append(max_support * 1000 + 20)
            else:
                node_size.append(30)
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="middle center",
            marker=dict(
                size=node_size,
                color=px.colors.qualitative.Set1,
                line=dict(width=2, color='white')
            )
        )
        
        fig_network = go.Figure(data=[edge_trace, node_trace],
                               layout=go.Layout(
                                   title="Product Association Network",
                                   showlegend=False,
                                   hovermode='closest',
                                   margin=dict(b=20,l=5,r=5,t=40),
                                   annotations=[ dict(
                                       text="Node size represents " + node_size_metric,
                                       showarrow=False,
                                       xref="paper", yref="paper",
                                       x=0.005, y=-0.002,
                                       xanchor="left", yanchor="bottom",
                                       font=dict(color="gray", size=12)
                                   )],
                                   xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                   yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                   plot_bgcolor='white',
                                   height=700
                               ))
        
        fig_network.update_layout(title_font=dict(size=16))
        st.plotly_chart(fig_network, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No association rules data available for network visualization.")

# Tab 4: Metrics Dashboard
with tab4:
    st.markdown('<div class="viz-container">', unsafe_allow_html=True)
    st.markdown("### 📈 Comprehensive Metrics Dashboard")
    
    # Create comprehensive dashboard
    fig_dashboard = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Support Distribution', 'Confidence vs Lift', 'Rules by Itemset Size', 'Top Products Frequency'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    if not frequent_itemsets.empty:
        # Support distribution
        fig_dashboard.add_trace(
            go.Histogram(x=frequent_itemsets['support'], name='Support Distribution', nbinsx=20),
            row=1, col=1
        )
    
    if not rules.empty:
        # Confidence vs Lift scatter
        fig_dashboard.add_trace(
            go.Scatter(
                x=rules['confidence'], 
                y=rules['lift'], 
                mode='markers',
                marker=dict(size=8, opacity=0.6),
                name='Rules'
            ),
            row=1, col=2
        )
        
        # Rules by itemset size
        rule_sizes = rules['antecedents'].apply(len) + rules['consequents'].apply(len)
        size_counts = rule_sizes.value_counts().sort_index()
        
        fig_dashboard.add_trace(
            go.Bar(x=size_counts.index, y=size_counts.values, name='Rules by Size'),
            row=2, col=1
        )
    
    # Top products frequency (from processed data if available)
    if 'processed_data' in st.session_state and st.session_state.processed_data:
        clean_df = st.session_state.processed_data['clean_df']
        product_counts = clean_df['Product'].value_counts().head(10)
        
        fig_dashboard.add_trace(
            go.Bar(x=product_counts.index, y=product_counts.values, name='Product Frequency'),
            row=2, col=2
        )
    
    fig_dashboard.update_layout(height=800, showlegend=False, template=viz_theme)
    st.plotly_chart(fig_dashboard, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 5: Interactive Explorer
with tab5:
    st.markdown('<div class="viz-container">', unsafe_allow_html=True)
    st.markdown("### 🎯 Interactive Data Explorer")
    
    if not rules.empty:
        st.markdown("#### Filter and Explore Rules")
        
        # Interactive filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Safe slider for support
            support_min = float(rules['support'].min())
            support_max = float(rules['support'].max())
            
            if support_min == support_max:
                st.write(f"**Minimum Support:** {support_min:.3f} (all rules have same support)")
                min_support_filter = support_min
            else:
                min_support_filter = st.slider("Minimum Support:", support_min, support_max, float(rules['support'].median()))
        
        with col2:
            # Safe slider for confidence
            confidence_min = float(rules['confidence'].min())
            confidence_max = float(rules['confidence'].max())
            
            if confidence_min == confidence_max:
                st.write(f"**Minimum Confidence:** {confidence_min:.3f} (all rules have same confidence)")
                min_confidence_filter = confidence_min
            else:
                min_confidence_filter = st.slider("Minimum Confidence:", confidence_min, confidence_max, float(rules['confidence'].median()))
        
        with col3:
            # Safe slider for lift
            lift_min = float(rules['lift'].min())
            lift_max = float(rules['lift'].max())
            
            if lift_min == lift_max:
                st.write(f"**Minimum Lift:** {lift_min:.3f} (all rules have same lift)")
                min_lift_filter = lift_min
            else:
                min_lift_filter = st.slider("Minimum Lift:", lift_min, lift_max, float(rules['lift'].median()))
        
        # Apply filters
        filtered_rules = rules[
            (rules['support'] >= min_support_filter) &
            (rules['confidence'] >= min_confidence_filter) &
            (rules['lift'] >= min_lift_filter)
        ]
        
        st.write(f"**Showing {len(filtered_rules)} rules matching your criteria:**")
        
        if not filtered_rules.empty:
            # Interactive scatter plot with selection
            fig_interactive = px.scatter(
                filtered_rules,
                x='confidence',
                y='lift',
                size='support',
                hover_data=['antecedents_str', 'consequents_str'],
                title="Interactive Rules Explorer (Click and drag to select)",
                template=viz_theme,
                color='support',
                color_continuous_scale=color_scheme
            )
            
            fig_interactive.update_layout(
                title_font=dict(size=16),
                height=500,
                dragmode='select',
                hovermode='closest'
            )
            
            st.plotly_chart(fig_interactive, use_container_width=True, key="interactive_plot")
            
            # Display filtered data
            display_columns = ['antecedents_str', 'consequents_str', 'support', 'confidence', 'lift']
            filtered_display = filtered_rules[display_columns].round(4)
            filtered_display.columns = ['Antecedents (If)', 'Consequents (Then)', 'Support', 'Confidence', 'Lift']
            
            st.dataframe(filtered_display, use_container_width=True)
            
        else:
            st.warning("No rules match the current filter criteria. Try adjusting the thresholds.")
    else:
        pass
    
    st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🔙 Back to Results", use_container_width=True):
        st.switch_page("pages/5_📊_Results_Dashboard.py")

with col3:
    if st.button("➡️ Business Insights", type="primary", use_container_width=True):
        st.switch_page("pages/7_💡_Business_Insights.py")

# Update session state
st.session_state.current_step = max(st.session_state.current_step, 6)

# Sidebar info
st.sidebar.markdown("### 📈 Advanced Visualizations")
st.sidebar.info("""
**Current Step:** Interactive Visualizations

**Available Charts:**
- Itemsets analysis charts
- Association rules visualizations  
- Interactive network graphs
- Comprehensive metrics dashboard
- Filterable data explorer

**Features:**
- Multiple chart themes
- Customizable color schemes
- Interactive selections
- Real-time filtering
""")

if analysis_results:
    st.sidebar.markdown("### 📊 Current Data")
    itemsets_count = len(frequent_itemsets) if not frequent_itemsets.empty else 0
    rules_count = len(rules) if not rules.empty else 0
    st.sidebar.write(f"**Frequent Itemsets:** {itemsets_count}")
    st.sidebar.write(f"**Association Rules:** {rules_count}")
    st.sidebar.write(f"**Algorithm:** {analysis_results.get('algorithm', 'Unknown')}")
