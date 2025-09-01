import streamlit as st
import pandas as pd
from utils.styles import load_custom_css
from utils.export_manager import ExportManager
import io
import zipfile

st.set_page_config(page_title="Download Center", page_icon="📥", layout="wide")
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
    <h1>📥 Download Center</h1>
    <p>Export your analysis results in multiple professional formats</p>
</div>
""", unsafe_allow_html=True)

# Initialize export manager
export_manager = ExportManager()

# Get data
analysis_results = st.session_state.analysis_results
processed_data = st.session_state.get('processed_data', {})

# Update export ready status
st.session_state.export_ready = True

# Export options overview
st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
st.markdown("### 🎯 Available Export Formats")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="download-card">
        <div class="download-icon">📊</div>
        <div class="download-title">CSV Files</div>
        <div class="download-description">Individual CSV files for each analysis component</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="download-card">
        <div class="download-icon">📈</div>
        <div class="download-title">Excel Workbook</div>
        <div class="download-description">Multi-sheet Excel file with all data organized</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="download-card">
        <div class="download-icon">📄</div>
        <div class="download-title">PDF Report</div>
        <div class="download-description">Executive summary with key findings</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="download-card">
        <div class="download-icon">📦</div>
        <div class="download-title">Complete Package</div>
        <div class="download-description">ZIP file with all formats included</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Individual downloads section
st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
st.markdown("### 📊 Individual File Downloads")

# CSV Downloads
st.markdown("#### 📁 CSV Format")
csv_col1, csv_col2, csv_col3 = st.columns(3)

with csv_col1:
    if 'frequent_itemsets' in analysis_results and not analysis_results['frequent_itemsets'].empty:
        itemsets_csv, itemsets_filename = export_manager.create_csv_export(
            analysis_results['frequent_itemsets'], "frequent_itemsets"
        )
        file_size = export_manager.get_file_size_mb(itemsets_csv)
        
        export_manager.create_download_button(
            itemsets_csv,
            itemsets_filename,
            f"📊 Download Frequent Itemsets\n({file_size:.2f} MB)",
            "text/csv",
            "Download frequent itemsets as CSV file",
            key="csv_itemsets"
        )

with csv_col2:
    if 'rules' in analysis_results and not analysis_results['rules'].empty:
        # Prepare rules for CSV export
        rules_export = analysis_results['rules'].copy()
        rules_export['antecedents'] = rules_export['antecedents'].apply(lambda x: ', '.join(list(x)))
        rules_export['consequents'] = rules_export['consequents'].apply(lambda x: ', '.join(list(x)))
        rules_csv_data = rules_export[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
        
        rules_csv, rules_filename = export_manager.create_csv_export(
            rules_csv_data, "association_rules"
        )
        file_size = export_manager.get_file_size_mb(rules_csv)
        
        export_manager.create_download_button(
            rules_csv,
            rules_filename,
            f"🔗 Download Association Rules\n({file_size:.2f} MB)",
            "text/csv",
            "Download association rules as CSV file",
            key="csv_rules"
        )

with csv_col3:
    if 'clean_df' in processed_data:
        processed_csv, processed_filename = export_manager.create_csv_export(
            processed_data['clean_df'], "processed_data"
        )
        file_size = export_manager.get_file_size_mb(processed_csv)
        
        export_manager.create_download_button(
            processed_csv,
            processed_filename,
            f"🔄 Download Processed Data\n({file_size:.2f} MB)",
            "text/csv",
            "Download cleaned and processed transaction data",
            key="csv_processed"
        )

st.markdown("---")

# Excel Download
st.markdown("#### 📈 Excel Format")
excel_col1, excel_col2 = st.columns([2, 1])

with excel_col1:
    # Prepare Excel data
    excel_data_dict = {}
    
    if 'frequent_itemsets' in analysis_results and not analysis_results['frequent_itemsets'].empty:
        itemsets_export = analysis_results['frequent_itemsets'].copy()
        itemsets_export['itemsets'] = itemsets_export['itemsets'].apply(lambda x: ', '.join(list(x)))
        excel_data_dict['Frequent_Itemsets'] = itemsets_export
    
    if 'rules' in analysis_results and not analysis_results['rules'].empty:
        rules_export = analysis_results['rules'].copy()
        rules_export['antecedents'] = rules_export['antecedents'].apply(lambda x: ', '.join(list(x)))
        rules_export['consequents'] = rules_export['consequents'].apply(lambda x: ', '.join(list(x)))
        excel_data_dict['Association_Rules'] = rules_export[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
    
    if 'clean_df' in processed_data:
        excel_data_dict['Processed_Data'] = processed_data['clean_df']
    
    # Add summary sheet
    summary_data = {
        'Metric': ['Total Transactions', 'Unique Products', 'Frequent Itemsets', 'Association Rules', 'Analysis Algorithm'],
        'Value': [
            len(processed_data.get('transactions', [])),
            len(processed_data.get('basket_df', pd.DataFrame()).columns),
            len(analysis_results.get('frequent_itemsets', pd.DataFrame())),
            len(analysis_results.get('rules', pd.DataFrame())),
            analysis_results.get('algorithm', 'Unknown')
        ]
    }
    excel_data_dict['Analysis_Summary'] = pd.DataFrame(summary_data)
    
    if excel_data_dict:
        excel_data, excel_filename = export_manager.create_excel_export(excel_data_dict)
        file_size = export_manager.get_file_size_mb(excel_data)
        
        export_manager.create_download_button(
            excel_data,
            excel_filename,
            f"📈 Download Complete Excel Workbook ({file_size:.2f} MB)",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "Download all analysis results in a multi-sheet Excel workbook",
            key="excel_complete"
        )

with excel_col2:
    st.markdown("""
    **Excel Workbook Contents:**
    - 📊 Frequent Itemsets
    - 🔗 Association Rules  
    - 🔄 Processed Data
    - 📋 Analysis Summary
    - 📈 Ready for pivot tables
    """)

st.markdown("---")

# JSON Download
st.markdown("#### 🔗 JSON Format")
json_col1, json_col2 = st.columns([2, 1])

with json_col1:
    # Prepare JSON data
    json_export_data = {
        'analysis_parameters': analysis_results.get('parameters', {}),
        'analysis_algorithm': analysis_results.get('algorithm', 'Unknown'),
        'export_timestamp': export_manager.timestamp
    }
    
    if 'frequent_itemsets' in analysis_results and not analysis_results['frequent_itemsets'].empty:
        itemsets_json = analysis_results['frequent_itemsets'].copy()
        itemsets_json['itemsets'] = itemsets_json['itemsets'].apply(lambda x: list(x))
        json_export_data['frequent_itemsets'] = itemsets_json.to_dict(orient='records')
    
    if 'rules' in analysis_results and not analysis_results['rules'].empty:
        rules_json = analysis_results['rules'].copy()
        rules_json['antecedents'] = rules_json['antecedents'].apply(lambda x: list(x))
        rules_json['consequents'] = rules_json['consequents'].apply(lambda x: list(x))
        json_export_data['association_rules'] = rules_json[['antecedents', 'consequents', 'support', 'confidence', 'lift']].to_dict(orient='records')
    
    json_data, json_filename = export_manager.create_json_export(json_export_data)
    file_size = export_manager.get_file_size_mb(json_data)
    
    export_manager.create_download_button(
        json_data,
        json_filename,
        f"🔗 Download JSON Data ({file_size:.2f} MB)",
        "application/json",
        "Download analysis results in machine-readable JSON format",
        key="json_complete"
    )

with json_col2:
    st.markdown("""
    **JSON Format Benefits:**
    - 🤖 Machine readable
    - 🔄 API compatible
    - 📊 Easy to parse
    - 🌐 Web friendly
    - 📱 Mobile compatible
    """)

st.markdown("---")

# PDF Report
st.markdown("#### 📄 PDF Report")
pdf_col1, pdf_col2 = st.columns([2, 1])

with pdf_col1:
    pdf_data, pdf_filename = export_manager.create_pdf_report(analysis_results, processed_data)
    file_size = export_manager.get_file_size_mb(pdf_data)
    
    export_manager.create_download_button(
        pdf_data,
        pdf_filename,
        f"📄 Download Executive Report ({file_size:.2f} MB)",
        "application/pdf",
        "Download a comprehensive PDF report with executive summary",
        key="pdf_report"
    )

with pdf_col2:
    st.markdown("""
    **Report Contents:**
    - 📋 Executive Summary
    - 📊 Dataset Overview
    - 🎯 Key Findings
    - 📈 Top Rules Analysis
    - 💡 Recommendations
    """)

st.markdown('</div>', unsafe_allow_html=True)

# Complete Package Download
st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
st.markdown("### 📦 Complete Analysis Package")

st.markdown("""
<div class="success-box-enhanced">
    <strong>🎯 Recommended Download</strong><br>
    Get everything in one convenient package! This ZIP file contains all export formats, 
    organized in folders with detailed documentation.
</div>
""", unsafe_allow_html=True)

# Create comprehensive ZIP
zip_data, zip_filename = export_manager.create_comprehensive_zip(analysis_results, processed_data)
file_size = export_manager.get_file_size_mb(zip_data)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    export_manager.create_download_button(
        zip_data,
        zip_filename,
        f"📦 Download Complete Package ({file_size:.2f} MB)",
        "application/zip",
        "Download everything: CSV, Excel, JSON, PDF report, and documentation",
        key="complete_package"
    )

# Package contents
st.markdown("#### 📋 Package Contents")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **📁 CSV Folder:**
    - frequent_itemsets.csv
    - association_rules.csv
    - processed_data.csv
    """)

with col2:
    st.markdown("""
    **📁 Excel Folder:**
    - Multi-sheet workbook
    - All data organized
    - Ready for analysis
    """)

with col3:
    st.markdown("""
    **📁 Reports Folder:**
    - Executive PDF report
    - JSON data export  
    - README documentation
    """)

st.markdown('</div>', unsafe_allow_html=True)

# Export statistics
st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
st.markdown("### 📊 Export Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    itemsets_count = len(analysis_results.get('frequent_itemsets', pd.DataFrame()))
    st.markdown(f"""
    <div class="metric-card-enhanced">
        <div class="metric-icon">📊</div>
        <div class="metric-value">{itemsets_count:,}</div>
        <div class="metric-label">Frequent Itemsets</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    rules_count = len(analysis_results.get('rules', pd.DataFrame()))
    st.markdown(f"""
    <div class="metric-card-enhanced">
        <div class="metric-icon">🔗</div>
        <div class="metric-value">{rules_count:,}</div>
        <div class="metric-label">Association Rules</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    transactions_count = len(processed_data.get('transactions', []))
    st.markdown(f"""
    <div class="metric-card-enhanced">
        <div class="metric-icon">🛒</div>
        <div class="metric-value">{transactions_count:,}</div>
        <div class="metric-label">Total Transactions</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    export_formats = 8  # CSV(3) + Excel + JSON + PDF + ZIP + HTML
    st.markdown(f"""
    <div class="metric-card-enhanced">
        <div class="metric-icon">📥</div>
        <div class="metric-value">{export_formats}</div>
        <div class="metric-label">Export Formats</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Usage instructions
st.markdown('<div class="card-container-enhanced">', unsafe_allow_html=True)
st.markdown("### 📖 Usage Instructions")

st.markdown("""
#### 🎯 Recommended Workflow:
1. **📦 Download Complete Package** - Get everything in one ZIP file
2. **📊 Use CSV files** for quick data import into other tools
3. **📈 Open Excel workbook** for detailed analysis and pivot tables
4. **📄 Share PDF report** with stakeholders and management
5. **🔗 Use JSON data** for web applications or API integration

#### 💡 Tips for Best Results:
- **CSV files** work great with Python, R, and Excel
- **Excel workbook** includes all data in organized sheets
- **PDF report** is perfect for presentations and meetings
- **JSON format** is ideal for developers and web applications
- **Complete ZIP** ensures you have everything backed up

#### 🔧 Technical Details:
- All files use UTF-8 encoding for international characters
- Excel files are compatible with Excel 2010 and later
- PDF reports include embedded fonts for consistent display
- JSON follows standard formatting for maximum compatibility
""")

st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🔙 Back to Insights", use_container_width=True):
        st.switch_page("pages/7_💡_Business_Insights.py")

with col2:
    if st.button("🏠 Return to Home", use_container_width=True):
        st.switch_page("app.py")

with col3:
    if st.button("🔄 New Analysis", type="primary", use_container_width=True):
        # Reset session state for new analysis
        for key in list(st.session_state.keys()):
            if key not in ['export_ready']:  # Keep some states
                del st.session_state[key]
        st.switch_page("pages/1_📁_Data_Upload.py")

# Update session state
st.session_state.current_step = max(st.session_state.current_step, 8)

# Sidebar info
st.sidebar.markdown("### 📥 Download Center")
st.sidebar.success("""
**Export Status:** Ready ✅

**Available Formats:**
- 📊 CSV Files (3 files)
- 📈 Excel Workbook
- 🔗 JSON Data
- 📄 PDF Report
- 📦 Complete ZIP Package

**Total Size:** ~{:.2f} MB
""".format(file_size if 'file_size' in locals() else 0))

st.sidebar.markdown("### 🎯 Quick Actions")
if st.sidebar.button("📧 Email Support", help="Get help with downloads"):
    st.sidebar.info("📧 Contact: support@marketbasket.com")

if st.sidebar.button("📖 Documentation", help="View detailed documentation"):
    st.sidebar.info("📖 Visit: docs.marketbasket.com")
