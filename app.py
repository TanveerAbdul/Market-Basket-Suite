import streamlit as st
import pandas as pd
import load_custom_css
import DataProcessor
import ExportManager

# Page config
st.set_page_config(
    page_title="Market Basket Analysis Professional Suite",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_custom_css()

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables"""
    defaults = {
        'current_step': 1,
        'data': None,
        'column_mapping': {},
        'processed_data': None,
        'analysis_results': {},
        'visualization_data': None,
        'export_ready': False,
        'analysis_complete': False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Initialize session state
initialize_session_state()

# Enhanced hero section with animated gradient
st.markdown("""
<div class="hero-container-enhanced">
    <div class="hero-content">
        <h1 class="hero-title-enhanced">🛒 Market Basket Analysis Professional Suite</h1>
        <p class="hero-subtitle-enhanced">Advanced retail analytics platform with comprehensive visualizations and export capabilities</p>
        <div class="hero-features">
            <span class="feature-badge">📊 Advanced Analytics</span>
            <span class="feature-badge">📈 Rich Visualizations</span>
            <span class="feature-badge">📥 Multi-format Export</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced progress indicator with animations
st.markdown("### 🗺️ Analysis Progress")

steps = [
    ("📁", "Data Upload", 1, "Upload your retail dataset"),
    ("⚙️", "Column Mapping", 2, "Map columns to analysis fields"),
    ("🔄", "Data Processing", 3, "Clean and prepare data"),
    ("🤖", "Analysis Setup", 4, "Configure algorithms and parameters"),
    ("📊", "Results Dashboard", 5, "View itemsets and rules"),
    ("📈", "Visualizations", 6, "Explore interactive charts"),
    ("💡", "Business Insights", 7, "Get actionable recommendations"),
    ("📥", "Download Center", 8, "Export results in multiple formats")
]

# Create progress grid
col_count = 4
rows = [steps[i:i+col_count] for i in range(0, len(steps), col_count)]

for row in rows:
    cols = st.columns(len(row))
    for col, (icon, name, step, desc) in zip(cols, row):
        with col:
            current_step = st.session_state.current_step
            
            if current_step > step:
                status_class = "step-completed-enhanced"
                status_icon = "✅"
            elif current_step == step:
                status_class = "step-current-enhanced"
                status_icon = "🔥"
            else:
                status_class = "step-pending-enhanced"
                status_icon = "⏳"
            
            st.markdown(f"""
            <div class="{status_class}">
                <div class="step-header">
                    <div class="step-icon-large">{icon}</div>
                    <div class="step-status">{status_icon}</div>
                </div>
                <div class="step-info">
                    <div class="step-name-large">{name}</div>
                    <div class="step-description">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")

# Enhanced dashboard metrics
if st.session_state.data is not None:
    st.markdown("### 📊 Current Dataset Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="metric-icon">📊</div>
            <div class="metric-value">{len(st.session_state.data):,}</div>
            <div class="metric-label">Total Records</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="metric-icon">📋</div>
            <div class="metric-value">{len(st.session_state.data.columns)}</div>
            <div class="metric-label">Data Columns</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.session_state.processed_data:
            transactions_count = len(st.session_state.processed_data.get('transactions', []))
            st.markdown(f"""
            <div class="metric-card-enhanced">
                <div class="metric-icon">🛒</div>
                <div class="metric-value">{transactions_count:,}</div>
                <div class="metric-label">Transactions</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="metric-card-enhanced">
                <div class="metric-icon">🛒</div>
                <div class="metric-value">-</div>
                <div class="metric-label">Transactions</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        if st.session_state.analysis_results:
            rules_count = len(st.session_state.analysis_results.get('rules', pd.DataFrame()))
            st.markdown(f"""
            <div class="metric-card-enhanced">
                <div class="metric-icon">🔗</div>
                <div class="metric-value">{rules_count:,}</div>
                <div class="metric-label">Association Rules</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="metric-card-enhanced">
                <div class="metric-icon">🔗</div>
                <div class="metric-value">-</div>
                <div class="metric-label">Association Rules</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col5:
        export_status = "Ready" if st.session_state.export_ready else "Pending"
        export_icon = "✅" if st.session_state.export_ready else "⏳"
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="metric-icon">{export_icon}</div>
            <div class="metric-value">{export_status}</div>
            <div class="metric-label">Export Status</div>
        </div>
        """, unsafe_allow_html=True)

# Navigation guide
st.markdown("### 🧭 Quick Navigation")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="nav-card">
        <h4>🚀 Getting Started</h4>
        <p>New to Market Basket Analysis? Start with uploading your data and follow the guided workflow.</p>
        <ul>
            <li>Upload CSV data</li>
            <li>Map your columns</li>
            <li>Process & analyze</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="nav-card">
        <h4>📈 Advanced Features</h4>
        <p>Explore powerful visualization and export capabilities for comprehensive analysis.</p>
        <ul>
            <li>Interactive charts</li>
            <li>Network graphs</li>
            <li>Business insights</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="nav-card">
        <h4>📥 Export & Share</h4>
        <p>Download your results in multiple formats for presentations and further analysis.</p>
        <ul>
            <li>CSV, Excel, JSON</li>
            <li>PDF reports</li>
            <li>Interactive HTML</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Sidebar enhancements
st.sidebar.markdown("### 🎛️ Quick Controls")

if st.sidebar.button("🔄 Reset Analysis", help="Clear all data and start fresh"):
    for key in st.session_state.keys():
        del st.session_state[key]
    initialize_session_state()
    st.rerun()

# Sample data option
st.sidebar.markdown("### 📝 Sample Data")
if st.sidebar.button("📊 Load Sample Dataset", help="Load sample retail data for testing"):
    # Create sample data
    sample_data = pd.DataFrame({
        'OrderID': ['O001', 'O001', 'O001', 'O002', 'O002', 'O003', 'O003', 'O004', 'O004', 'O004'],
        'Product': ['Bread', 'Milk', 'Butter', 'Bread', 'Eggs', 'Milk', 'Cheese', 'Bread', 'Milk', 'Yogurt'],
        'Customer': ['John', 'John', 'John', 'Alice', 'Alice', 'Bob', 'Bob', 'Carol', 'Carol', 'Carol'],
        'Price': [2.5, 3.0, 1.8, 2.5, 2.2, 3.0, 4.5, 2.5, 3.0, 1.5],
        'Quantity': [1, 1, 2, 1, 3, 1, 1, 2, 1, 1]
    })
    st.session_state.data = sample_data
    st.session_state.current_step = 2
    st.success("Sample data loaded successfully!")
    st.rerun()

# Current status
st.sidebar.markdown("### 📊 Analysis Status")
st.sidebar.info(f"""
**Current Step:** {st.session_state.current_step}/8

**Data Status:** {'✅ Loaded' if st.session_state.data is not None else '❌ Not Loaded'}

**Processing:** {'✅ Complete' if st.session_state.processed_data else '⏳ Pending'}

**Analysis:** {'✅ Complete' if st.session_state.analysis_complete else '⏳ Pending'}

**Export Ready:** {'✅ Yes' if st.session_state.export_ready else '❌ No'}
""")

