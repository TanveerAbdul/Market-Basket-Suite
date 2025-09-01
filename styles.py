import streamlit as st

def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Enhanced Hero Section */
    .hero-container-enhanced {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }
    
    .hero-container-enhanced::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        pointer-events: none;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .hero-title-enhanced {
        color: white;
        font-size: 3.8rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle-enhanced {
        color: rgba(255,255,255,0.95);
        font-size: 1.4rem;
        font-weight: 400;
        margin-bottom: 2rem;
        position: relative;
        z-index: 1;
    }
    
    .hero-features {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
        position: relative;
        z-index: 1;
    }
    
    .feature-badge {
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .feature-badge:hover {
        background: rgba(255,255,255,0.3);
        transform: translateY(-2px);
    }
    
    /* Enhanced Step Components */
    .step-completed-enhanced {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px rgba(16, 185, 129, 0.3);
        transform: scale(1);
        transition: all 0.3s ease;
        border: 2px solid rgba(255,255,255,0.1);
    }
    
    .step-completed-enhanced:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 40px rgba(16, 185, 129, 0.4);
    }
    
    .step-current-enhanced {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.4);
        animation: pulseGlow 2s infinite;
        border: 2px solid rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .step-current-enhanced::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .step-pending-enhanced {
        background: linear-gradient(135deg, #f8fafc, #e2e8f0);
        color: #64748b;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem 0;
        border: 2px dashed #cbd5e1;
        transition: all 0.3s ease;
    }
    
    .step-pending-enhanced:hover {
        background: linear-gradient(135deg, #e2e8f0, #cbd5e1);
        transform: translateY(-2px);
    }
    
    .step-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .step-icon-large {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .step-status {
        font-size: 1.2rem;
    }
    
    .step-name-large {
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.3rem;
    }
    
    .step-description {
        font-size: 0.8rem;
        opacity: 0.8;
        line-height: 1.3;
    }
    
    @keyframes pulseGlow {
        0%, 100% { 
            box-shadow: 0 8px 32px rgba(59, 130, 246, 0.4);
        }
        50% { 
            box-shadow: 0 8px 32px rgba(59, 130, 246, 0.6);
        }
    }
    
    /* Enhanced Metric Cards */
    .metric-card-enhanced {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card-enhanced::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .metric-card-enhanced:hover::before {
        left: 100%;
    }
    
    .metric-card-enhanced:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
    }
    
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    
    /* Navigation Cards */
    .nav-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .nav-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(0,0,0,0.12);
        border-color: #3b82f6;
    }
    
    .nav-card h4 {
        color: #1f2937;
        margin-bottom: 1rem;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    .nav-card p {
        color: #6b7280;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .nav-card ul {
        color: #374151;
        padding-left: 1.2rem;
    }
    
    .nav-card li {
        margin-bottom: 0.3rem;
        font-size: 0.9rem;
    }
    
    /* Enhanced Page Headers */
    .page-header-enhanced {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 12px 48px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }
    
    .page-header-enhanced::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 30px 30px;
        animation: float 20s infinite linear;
    }
    
    @keyframes float {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }
    
    .page-header-enhanced h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: 800;
        position: relative;
        z-index: 1;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    }
    
    .page-header-enhanced p {
        margin: 1rem 0 0 0;
        font-size: 1.3rem;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }
    
    /* Card Containers Enhanced */
    .card-container-enhanced {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.06);
        margin: 2rem 0;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .card-container-enhanced::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px 20px 0 0;
    }
    
    .card-container-enhanced:hover {
        box-shadow: 0 16px 48px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    }
    
    /* Status Boxes Enhanced */
    .success-box-enhanced {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        border: 2px solid #10b981;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .success-box-enhanced::before {
        content: '✅';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 1.5rem;
        opacity: 0.7;
    }
    
    .warning-box-enhanced {
        background: linear-gradient(135deg, #fef3cd, #fed7aa);
        border: 2px solid #f59e0b;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .warning-box-enhanced::before {
        content: '⚠️';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 1.5rem;
        opacity: 0.7;
    }
    
    .error-box-enhanced {
        background: linear-gradient(135deg, #fee2e2, #fecaca);
        border: 2px solid #ef4444;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .error-box-enhanced::before {
        content: '❌';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 1.5rem;
        opacity: 0.7;
    }
    
    /* Visualization Containers */
    .viz-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.06);
        margin: 1.5rem 0;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .viz-container:hover {
        box-shadow: 0 12px 36px rgba(0,0,0,0.1);
    }
    
    .viz-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .viz-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f2937;
        margin: 0;
    }
    
    .viz-controls {
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    
    /* Download Center Styles */
    .download-card {
        background: linear-gradient(135deg, #f8fafc, #e2e8f0);
        border: 2px solid #cbd5e1;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .download-card:hover {
        background: linear-gradient(135deg, #e2e8f0, #cbd5e1);
        border-color: #3b82f6;
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    }
    
    .download-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .download-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .download-description {
        color: #6b7280;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title-enhanced {
            font-size: 2.5rem;
        }
        
        .hero-subtitle-enhanced {
            font-size: 1.1rem;
        }
        
        .feature-badge {
            font-size: 0.8rem;
            padding: 0.4rem 0.8rem;
        }
        
        .nav-card {
            padding: 1.5rem;
        }
        
        .metric-card-enhanced {
            padding: 1.5rem 1rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
    }
    
    /* Loading Animations */
    .loading-spinner {
        border: 3px solid #f3f4f6;
        border-top: 3px solid #3b82f6;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Sidebar Enhancements */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Data Tables */
    .dataframe {
        border: none !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1) !important;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
    }
    
    .dataframe td {
        border: none !important;
        border-bottom: 1px solid #e2e8f0 !important;
    }
    
    .dataframe tbody tr:nth-child(even) {
        background-color: #f8fafc !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: #e2e8f0 !important;
    }
    
    </style>
    """, unsafe_allow_html=True)
