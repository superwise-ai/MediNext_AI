"""
Header Component for EHR Demo Portal

This component creates the main header with logo and title.
"""

import streamlit as st
import base64

# Import global logging
from utils.logger import get_logger
from app.utils.css_styles import get_common_styles

# Read and encode image as base64
with open("app/assets/superwise_logo.svg", "rb") as f:
    data = f.read()
encoded = base64.b64encode(data).decode()


def create_header():
    """
    Creates the main header component with logo and title.

    Returns:
        None: Renders the header directly to the Streamlit app
    """
    # Get logger for header
    logger = get_logger(__name__)
    logger.info("📋 Creating application header")

    # Load common CSS styles
    st.markdown(get_common_styles(), unsafe_allow_html=True)

    # Create header container with relative positioning
    st.markdown(
        f"""
    <div class="header-container">
        <div class="header-left">
                <img src="data:image/svg+xml;base64,{encoded}" alt="SUPERWISE Logo">
                <span class="header-title">MediNext AI</span>
        </div>    
    </div>
    """,
        unsafe_allow_html=True,
    )
