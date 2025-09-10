"""
Sidebar Navigation Component for EHR Demo Portal

This component creates the left sidebar navigation with menu items.
"""

import streamlit as st
import base64
from app.utils.css_styles import get_common_styles, get_component_specific_styles

# Read and encode image as base64
with open("app/assets/Group 11.svg", "rb") as f:
    data = f.read()
encoded = base64.b64encode(data).decode()


def create_sidebar():
    """
    Creates the sidebar navigation component with menu items.

    Returns:
        str: Selected page name
    """

    # Apply common CSS styles globally (not in sidebar context)
    st.markdown(get_common_styles(), unsafe_allow_html=True)
    st.markdown(get_component_specific_styles("sidebar"), unsafe_allow_html=True)

    # Custom CSS for sidebar styling
    st.sidebar.markdown(
        f"""
    <!-- Sidebar Header -->
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:1rem;">
        <img src="data:image/svg+xml;base64,{encoded}" width="24" height="24">
        <h2 style="margin:0;">MediNext AI</h2>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Menu items with icons
    menu_items = [
        ("🏠", "Dashboard", "dashboard"),
        ("👥", "Patients", "patients"),
        ("📅", "Appointments", "appointments"),
        ("💊", "Prescriptions", "prescriptions"),
        ("📊", "Reports", "reports"),
    ]

    # Get current page from session state
    current_page = st.session_state.get("current_page", "dashboard")

    # Display menu items as buttons
    selected_page = current_page  # Default to current page

    for icon, text, page in menu_items:
        if st.sidebar.button(f"{icon} {text}", key=f"nav_{page}"):
            selected_page = page

    return selected_page
