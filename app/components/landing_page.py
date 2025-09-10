"""
Landing Page Component for EHR Demo Portal

This component creates the landing page shown when user is not logged in.
"""

import streamlit as st
import base64

# Import global logging
from utils.logger import get_logger
from app.utils.css_styles import get_common_styles, get_component_specific_styles

# Read and encode image as base64
with open("app/assets/superwise_logo.svg", "rb") as f:
    data = f.read()
encoded = base64.b64encode(data).decode()


def create_landing_page():
    """
    Creates the landing page component with header and dashboard redirect.

    Returns:
        None: Renders the landing page directly to the Streamlit app
    """
    # Get logger for landing page
    logger = get_logger(__name__)
    logger.info("🚀 Creating landing page component")

    # Load common CSS styles and component-specific styles
    st.markdown(get_common_styles(), unsafe_allow_html=True)
    st.markdown(get_component_specific_styles("landing_page"), unsafe_allow_html=True)

    # Landing page header with dashboard button on the right
    st.markdown(
        f"""
    <div class="landing-header">
        <div class="landing-header-content">
            <div class="landing-header-left">
                <div class="logo">
                    <img src="data:image/svg+xml;base64,{encoded}" alt="SUPERWISE Logo">
                </div>
                <div>
                    <h1 class="title">MediNext AI</h1>
                </div>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Landing page content using Streamlit components
    st.markdown(
        """
    <div class="landing-content">
        <h1 class="welcome-title">Welcome to MediNext AI</h1>
        <p class="welcome-subtitle">
            Advanced AI-powered Healthcare Management System. 
            Access patient data, manage appointments, and get AI-powered insights efficiently.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Use Streamlit button for dashboard redirect
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "🚀 Dashboard", key="enter_dashboard_btn", use_container_width=True
        ):
            logger.info("📊 Dashboard button clicked - redirecting to dashboard")
            st.session_state.current_page = "dashboard"
            st.rerun()

    logger.info("✅ Landing page rendering completed")
