"""
Common CSS Styles for EHR Demo Portal

This module contains all the common CSS styles used across components
to avoid code duplication and maintain consistency.
"""


def get_common_styles():
    """
    Returns the common CSS styles used across all components.

    Returns:
        str: CSS styles as a string
    """
    return """
    <style>
    /* Import Inter font from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap');
    
    /* Override Streamlit default font to Inter, excluding sidebar buttons */
    .stApp, .stApp > div, .main .block-container, 
    .stMarkdown, .stText, .stSelectbox, .stTextInput, 
    .stNumberInput, .stTextArea, .stDateInput, .stTimeInput,
    .stFileUploader, .stColorPicker, .stSlider, .stRadio, 
    .stCheckbox, .stMultiselect, .stDataFrame, .stTable, 
    .stMetric, .stAlert, .stSuccess, .stInfo, .stWarning, 
    .stError, .stCaption, .stCode, .stJson, .stLatex, .stMath,
    .stPlotlyChart, .stPyplot, .stBokehChart, .stAltairChart,
    .stVegaLiteChart, .stGraphvizChart, .stMap, .stImage,
    .stVideo, .stAudio, .stDownloadButton, .stButton,
    .stSidebar .stMarkdown, .stSidebar .stText, .stSidebar .stSelectbox,
    .stSidebar .stTextInput, .stSidebar .stNumberInput, .stSidebar .stTextArea,
    .stSidebar .stDateInput, .stSidebar .stTimeInput, .stSidebar .stFileUploader,
    .stSidebar .stColorPicker, .stSidebar .stSlider, .stSidebar .stRadio,
    .stSidebar .stCheckbox, .stSidebar .stMultiselect, .stSidebar .stDataFrame,
    .stSidebar .stTable, .stSidebar .stMetric, .stSidebar .stAlert,
    .stSidebar .stSuccess, .stSidebar .stInfo, .stSidebar .stWarning,
    .stSidebar .stError, .stSidebar .stCaption, .stSidebar .stCode,
    .stSidebar .stJson, .stSidebar .stLatex, .stSidebar .stMath,
    .stSidebar .stPlotlyChart, .stSidebar .stPyplot, .stSidebar .stBokehChart,
    .stSidebar .stAltairChart, .stSidebar .stVegaLiteChart, .stSidebar .stGraphvizChart,
    .stSidebar .stMap, .stSidebar .stImage, .stSidebar .stVideo,
    .stSidebar .stAudio, .stSidebar .stDownloadButton {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }
    
    /* Protect sidebar buttons from font changes */
    .stSidebar button[data-testid="baseButton-secondary"],
    .stSidebar button[data-testid="baseButton-secondary"] *,
    .stSidebar .stButton button,
    .stSidebar .stButton button * {
        font-family: inherit !important;
    }
    
    /* ===== COMMON CARD STYLES ===== */
    .common-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .common-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    /* ===== METRIC CARD STYLES ===== */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    .metric-card .card-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    
    .metric-card .card-icon {
        font-size: 2rem;
        padding: 0.5rem;
        border-radius: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 3rem;
        height: 3rem;
    }
    
    .metric-card .card-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: #64748b;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-card .card-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0;
    }
    
    .metric-card .card-change {
        font-size: 0.875rem;
        color: #059669;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .metric-card .card-change.negative {
        color: #dc2626;
    }
    
    /* ===== SECTION STYLES ===== */
    .section-container {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .section-header {
        display: flex;
        justify-content: flex-start;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1e293b;
        margin: 0;
    }
    
    .section-icon {
        font-size: 1.25rem;
        color: #6b7280;
    }
    
    /* ===== STATUS BADGE STYLES ===== */
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
    }
    
    .status-active {
        background-color: #d1fae5;
        color: #047857;
    }
    
    .status-followup {
        background-color: #fef3c7;
        color: #d97706;
    }
    
    .status-violation {
        background-color: #fef2f2;
        color: #dc2626;
    }
    
    .status-clear {
        background-color: #d1fae5;
        color: #047857;
    }
    
    /* ===== PATIENT TABLE STYLES ===== */
    .patient-table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .patient-table th {
        background-color: #f8fafc;
        padding: 0.75rem;
        text-align: left;
        font-weight: 600;
        color: #374151;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .patient-table td {
        padding: 0.75rem;
        border-bottom: 1px solid #f3f4f6;
        color: #374151;
    }
    
    .patient-table tr:hover {
        background-color: #f9fafb;
    }
    
    /* ===== SEARCH STYLES ===== */
    .search-container {
        position: relative;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .search-input {
        padding: 0.5rem 1rem 0.5rem 2.5rem;
        border: 1px solid #d1d5db;
        border-radius: 0.5rem;
        font-size: 0.875rem;
        width: 300px;
    }
    
    .search-icon {
        position: absolute;
        left: 0.75rem;
        color: #6b7280;
        font-size: 1rem;
    }
    
    /* ===== PATIENT DETAILS STYLES ===== */
    .patient-details-container {
        background: white;
        padding: 2rem;
        border-radius: 0.75rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .patient-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e5e7eb;
    }
    
    .patient-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0;
    }
    
    .patient-id {
        font-size: 1rem;
        color: #6b7280;
        margin: 0;
    }
    
    .details-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .detail-section {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
    }
    
    .detail-section h3 {
        font-size: 1rem;
        font-weight: 600;
        color: #374151;
        margin: 0 0 1rem 0;
    }
    
    .detail-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .detail-item:last-child {
        border-bottom: none;
    }
    
    .detail-label {
        font-weight: 500;
        color: #6b7280;
        font-size: 0.875rem;
    }
    
    .detail-value {
        font-weight: 600;
        color: #1e293b;
        text-align: right;
        font-size: 0.875rem;
    }
    
    /* ===== SUPERWISE SECTION STYLES ===== */
    .superwise-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 0.75rem;
        color: white;
        margin-top: 2rem;
    }
    
    .superwise-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    
    .superwise-title {
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0;
    }
    
    .ask-superwise-btn {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .ask-superwise-btn:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-1px);
    }
    
    .superwise-response {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-top: 1rem;
    }
    
    /* ===== ACTIVITY FEED STYLES ===== */
    .activity-feed {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        height: 100%;
    }
    
    .activity-feed .feed-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .activity-feed .feed-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: #1e293b;
        margin: 0;
    }
    
    .activity-feed .feed-icon {
        font-size: 1.25rem;
        color: #6b7280;
    }
    
    .activity-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.75rem 0;
        border-bottom: 1px solid #f3f4f6;
    }
    
    .activity-item:last-child {
        border-bottom: none;
    }
    
    .activity-item .activity-icon {
        font-size: 1rem;
        padding: 0.25rem;
        border-radius: 0.25rem;
        min-width: 1.5rem;
        height: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 0.125rem;
    }
    
    .activity-item .activity-content {
        flex: 1;
    }
    
    .activity-item .activity-text {
        font-size: 0.875rem;
        color: #374151;
        margin: 0 0 0.25rem 0;
        line-height: 1.4;
    }
    
    .activity-item .activity-time {
        font-size: 0.75rem;
        color: #6b7280;
        margin: 0;
    }
    
    .activity-item .activity-priority {
        padding: 0.125rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.625rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .priority-normal {
        background-color: #f3f4f6;
        color: #6b7280;
    }
    
    .priority-critical {
        background-color: #fee2e2;
        color: #dc2626;
    }
    
    .activity-feed .refresh-button {
        margin-top: 1rem;
        width: 100%;
        padding: 0.5rem;
        background-color: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        color: #6b7280;
        font-size: 0.875rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .activity-feed .refresh-button:hover {
        background-color: #f1f5f9;
        border-color: #d1d5db;
    }
    
    /* ===== ANALYTICS CHART STYLES ===== */
    .analytics-section {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .chart-container {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .chart-title {
        font-size: 1rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.75rem;
        text-align: center;
    }
    
    .metrics-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .metric-item {
        flex: 1;
        text-align: center;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #6b7280;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* ===== HEADER STYLES ===== */
    .header-container {
        background: white;
        padding: 1rem 1rem 1rem 1rem;
        border-radius: 0;
        margin: 0;
        margin-bottom: 2rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-bottom: 1px solid #e5e7eb;
        position: relative;
        top: 0;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
     
    .header-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }
     
    .header-left {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .header-left img {
        height: 37px;
        width: 160px;
        filter: none;
    }

    .header-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2c2f38;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .title {
        color: black;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .logout-button {
        background-color: #ef4444;
        color: white !important;
        border: none;
        padding: 0.4rem 1rem;
        border-radius: 0.375rem;
        font-size: 0.9rem;
        font-weight: 600;
        cursor: pointer;
        transition: background-color 0.2s ease;
        margin-left: auto;
    }
    
    .logout-button:hover {
        background-color: #dc2626;
    }
    
    /* ===== BUTTON STYLES ===== */
    .btn-primary {
        background-color: #3b82f6;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.2s ease;
    }
    
    .btn-primary:hover {
        background-color: #2563eb;
    }
    
    .btn-secondary {
        background-color: #6b7280;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.2s ease;
    }
    
    .btn-secondary:hover {
        background-color: #4b5563;
    }
    
    .btn-danger {
        background-color: #ef4444;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.2s ease;
    }
    
    .btn-danger:hover {
        background-color: #dc2626;
    }
    
    /* ===== FORM STYLES ===== */
    .form-container {
        background: white;
        padding: 2rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        width: 100%;
    }
    
    .form-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .form-group {
        margin-bottom: 1.5rem;
    }
    
    .form-label {
        display: block;
        font-size: 0.875rem;
        font-weight: 500;
        color: #374151;
        margin-bottom: 0.5rem;
    }
    
    .form-input {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid #d1d5db;
        border-radius: 0.375rem;
        font-size: 1rem;
        transition: border-color 0.2s ease;
    }
    
    .form-input:focus {
        outline: none;
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    </style>
    """


def get_component_specific_styles(component_name):
    """
    Returns component-specific CSS styles.

    Args:
        component_name (str): Name of the component

    Returns:
        str: Component-specific CSS styles
    """
    styles = {
        "landing_page": """
        <style>
        .landing-header {
            background: white;
            padding: 1rem 1rem 1rem 1rem;
            border-radius: 0;
            margin: 0;
            margin-bottom: 2rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border-bottom: 1px solid #e5e7eb;
            position: relative;
            top: 0;
        }
        
        .landing-header-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
        }
        
        .landing-header-left {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .landing-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 60vh;
            text-align: center;
            padding: 2rem;
        }
        
        .welcome-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1e293b;
            margin-bottom: 1rem;
        }
        
        .welcome-subtitle {
            font-size: 1.25rem;
            color: #64748b;
            margin-bottom: 2rem;
            max-width: 600px;
        }
        </style>
        """,
        "login_page": """
        <style>
        .login-header {
            background: white;
            padding: 1rem 1rem 1rem 1rem;
            border-radius: 0;
            margin: 0;
            margin-bottom: 2rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border-bottom: 1px solid #e5e7eb;
            position: relative;
            top: 0;
        }
        
        .login-header-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
        }
        
        .login-header-left {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 60vh;
            padding: 2rem;
        }
        
        .login-form-subtitle {
            font-size: 1rem;
            color: #64748b;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .forgot-password {
            text-align: center;
            margin-top: 1rem;
        }
        
        .forgot-password a {
            color: #3b82f6;
            text-decoration: none;
            font-size: 0.875rem;
        }
        
        .forgot-password a:hover {
            text-decoration: underline;
        }
        </style>
        """,
        "sidebar": """
        <style>
        .sidebar .sidebar-content {
            background-color: #f8fafc;
            padding: 0rem 1rem 1rem 1rem;
        }
        
        .stSidebar button[data-testid="baseButton-secondary"] {
            background-color: transparent !important;
            border: none !important;
            padding: 0.75rem 1rem !important;
            margin: 0.25rem 0 !important;
            border-radius: 0.5rem !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
            font-size: 1rem !important;
        }
        
        .stSidebar button[data-testid="baseButton-secondary"]:hover {
            background-color: #e2e8f0 !important;
            transform: translateX(4px) !important;
        }
        </style>
        """,
    }

    return styles.get(component_name, "")
