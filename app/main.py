"""
Main MediNext AI Application

This is the main entry point for the MediNext AI Streamlit application.
"""

import sys
import os

# Add the parent directory to Python path to enable app.* imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import components
from components.header import create_header
from components.sidebar import create_sidebar
from components.dashboard_cards import create_dashboard_cards
from components.patient_table import create_patient_table
from components.patient_details import show_patient_details_page
from components.activity_feed import create_activity_feed
from components.analytics_charts import create_analytics_charts
from components.landing_page import create_landing_page

# Import global logging
from utils.logger import get_logger


# Page navigation helper functions
def set_page(page_name: str):
    """Set the current page in session state"""
    if st.session_state.current_page != page_name:
        st.session_state.current_page = page_name
        logger = get_logger(__name__)
        logger.info(f"🔄 Page set to: {page_name}")
        st.rerun()


def get_current_page() -> str:
    """Get the current page from session state"""
    return st.session_state.get("current_page", "dashboard")


def navigate_to_page(page_name: str):
    """Navigate to a specific page"""
    set_page(page_name)


# Page configuration
st.set_page_config(
    page_title="MediNext AI",
    page_icon="app/assets/Group 11.svg",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
<style>
    /* Global styles */
    .main .block-container {
        padding-top: 0rem;
        padding-bottom: 2rem;
    }
    
    /* Remove any top margin from the first element */
    .main .block-container > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Ensure header starts from top */
    .stApp > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Remove main content area spacing */
    .main .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    /* Ensure no gaps between sidebar and main content */
    .stApp > div {
        gap: 0 !important;
    }
    
    /* Remove any margin between sidebar and main */
    .stApp .main .block-container {
        margin-left: 0 !important;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
    

    
    /* Ensure proper text colors */
    .stMarkdown, .stMarkdown * {
        color: #31333f !important;
    }
    
    .stHeader, .stHeader * {
        color: #31333f !important;
    }
    
    .stSubheader, .stSubheader * {
        color: #31333f !important;
    }
    
    /* Main content text colors */
    .main div, .main div * {
        color: #31333f !important;
    }
    
    /* Data table backgrounds */
    .stDataFrame {
        background-color: #ffffff !important;
    }
    
    .stDataFrame > div {
        background-color: #ffffff !important;
    }
    
    .stDataFrame table {
        background-color: #ffffff !important;
    }
    
    .stDataFrame th {
        background-color: #f8fafc !important;
        color: #374151 !important;
    }
    
    .stDataFrame td {
        background-color: #ffffff !important;
        color: #374151 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


def main():
    """
    Main application function that orchestrates all components.
    """

    # Get logger for main application
    logger = get_logger(__name__)
    logger.info("🎯 Main application function started")

    # Initialize page state
    if "current_page" not in st.session_state:
        st.session_state.current_page = "landing"
        logger.info("🔧 Initialized session state: current_page = landing")

    # Show landing page if not on dashboard
    if st.session_state.current_page == "landing":
        create_landing_page()
        return

    # User is on dashboard - show main application
    # Create header
    create_header()

    # Create sidebar and get selected page
    selected_page = create_sidebar()

    # Update page state if sidebar button was clicked
    if selected_page != st.session_state.current_page:
        st.session_state.current_page = selected_page
        logger.info(f"🔧 Updated session state: current_page = {selected_page}")
        st.rerun()

    # Main content area based on session state
    current_page = st.session_state.current_page
    if current_page == "dashboard" or current_page is None:
        show_dashboard()
    elif current_page == "patients":
        show_patients()
    elif current_page == "patient_details":
        show_patient_details_page()
    elif current_page == "appointments":
        show_appointments()
    elif current_page == "prescriptions":
        show_prescriptions()
    elif current_page == "reports":
        show_reports()


def show_dashboard():
    """
    Displays the main dashboard view.
    """

    # Dashboard title
    st.markdown("## 📊 Dashboard Overview")
    st.markdown("Welcome to MediNext AI. Here's your current overview.")

    # Create dashboard cards
    create_dashboard_cards()

    # Analytics section (full width)
    st.markdown("---")
    create_analytics_charts()


def show_patients():
    """
    Displays the patients page.
    """
    st.markdown("## 👥 Patient Management")
    st.markdown("Manage patient information, records, and history.")

    # Create patient table
    create_patient_table()


def show_appointments():
    """
    Displays the appointments page.
    """
    st.markdown("## 📅 Appointment Management")
    st.markdown("Schedule and manage patient appointments.")

    # Sample appointment data
    appointments = [
        {
            "Time": "09:00 AM",
            "Patient": "John Doe",
            "Type": "Follow-up",
            "Status": "Confirmed",
        },
        {
            "Time": "10:30 AM",
            "Patient": "Jane Smith",
            "Type": "New Patient",
            "Status": "Confirmed",
        },
        {
            "Time": "02:00 PM",
            "Patient": "Mike Johnson",
            "Type": "Consultation",
            "Status": "Pending",
        },
        {
            "Time": "03:30 PM",
            "Patient": "Sarah Wilson",
            "Type": "Follow-up",
            "Status": "Confirmed",
        },
    ]

    # Display appointments
    st.markdown("### Today's Appointments")

    for appt in appointments:
        col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
        with col1:
            st.write(f"🕐 {appt['Time']}")
        with col2:
            st.write(f"👤 {appt['Patient']}")
        with col3:
            st.write(f"📋 {appt['Type']}")
        with col4:
            status_color = "🟢" if appt["Status"] == "Confirmed" else "🟡"
            st.write(f"{status_color} {appt['Status']}")
        st.markdown("---")

    # Appointment scheduling
    st.markdown("### Schedule New Appointment")

    col1, col2 = st.columns(2)

    with col1:
        st.date_input("Appointment Date", key="appt_date")
        st.time_input("Appointment Time", key="appt_time")

    with col2:
        st.selectbox(
            "Patient",
            ["John Doe", "Jane Smith", "Mike Johnson", "Sarah Wilson"],
            key="appt_patient",
        )
        st.selectbox(
            "Appointment Type",
            ["Consultation", "Follow-up", "New Patient", "Emergency"],
            key="appt_type",
        )

    if st.button("📅 Schedule Appointment", key="schedule"):
        st.success("Appointment scheduled successfully!")


def show_prescriptions():
    """
    Displays the prescriptions page.
    """
    st.markdown("## 💊 Prescription Management")
    st.markdown("Manage patient medications and prescriptions.")

    # Sample prescription data
    prescriptions = [
        {
            "Patient": "John Doe",
            "Medication": "Lisinopril",
            "Dosage": "10mg daily",
            "Status": "Active",
        },
        {
            "Patient": "Jane Smith",
            "Medication": "Metformin",
            "Dosage": "500mg twice daily",
            "Status": "Active",
        },
        {
            "Patient": "Mike Johnson",
            "Medication": "Atorvastatin",
            "Dosage": "20mg daily",
            "Status": "Refill Needed",
        },
        {
            "Patient": "Sarah Wilson",
            "Medication": "Omeprazole",
            "Dosage": "40mg daily",
            "Status": "Active",
        },
    ]

    # Display prescriptions
    st.markdown("### Current Prescriptions")

    for rx in prescriptions:
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        with col1:
            st.write(f"👤 {rx['Patient']}")
        with col2:
            st.write(f"💊 {rx['Medication']}")
        with col3:
            st.write(f"📏 {rx['Dosage']}")
        with col4:
            if rx["Status"] == "Active":
                st.write("🟢 Active")
            elif rx["Status"] == "Refill Needed":
                st.write("🟡 Refill")
        st.markdown("---")

    # New prescription form
    st.markdown("### New Prescription")

    with st.form("new_prescription"):
        col1, col2 = st.columns(2)

        with col1:
            st.selectbox(
                "Patient",
                ["John Doe", "Jane Smith", "Mike Johnson", "Sarah Wilson"],
                key="rx_patient",
            )
            st.text_input("Medication Name", key="rx_medication")

        with col2:
            st.text_input("Dosage", key="rx_dosage")
            st.text_input("Frequency", key="rx_frequency")

        st.text_area("Instructions", key="rx_instructions")

        if st.form_submit_button("💊 Prescribe Medication"):
            st.success("Prescription created successfully!")


def show_reports():
    """
    Displays the reports page.
    """
    st.markdown("## 📊 Reports & Analytics")
    st.markdown("Generate comprehensive reports and view analytics.")

    # Report types
    st.markdown("### Available Reports")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Patient Reports")
        st.button("📋 Patient Demographics", key="demo_report")
        st.button("📈 Patient Growth", key="growth_report")
        st.button("🏥 Department Utilization", key="util_report")
        st.button("📅 Appointment Statistics", key="appt_report")

    with col2:
        st.markdown("#### Clinical Reports")
        st.button("💊 Prescription Analysis", key="rx_report")
        st.button("🔬 Lab Results Summary", key="lab_report")
        st.button("⚠️ Critical Alerts", key="alert_report")
        st.button("📊 Quality Metrics", key="quality_report")

    # Date range selection
    st.markdown("---")
    st.markdown("### Report Parameters")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.date_input("Start Date", key="report_start")

    with col2:
        st.date_input("End Date", key="report_end")

    with col3:
        st.selectbox("Report Format", ["PDF", "Excel", "CSV"], key="report_format")

    if st.button("📊 Generate Report", key="generate_report"):
        st.success("Report generated successfully!")
        st.info("Report will be available for download shortly.")


if __name__ == "__main__":
    main()
