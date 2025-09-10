"""
Configuration Settings for MediNext AI

This module contains configuration settings and constants for the application.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent.parent

# Application settings
APP_NAME = "MediNext AI"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Advanced AI-powered Healthcare Management System"

# Streamlit configuration
STREAMLIT_CONFIG = {
    "page_title": APP_NAME,
    "page_icon": "🏥",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# API settings (for future use)
API_CONFIG = {
    "base_url": os.getenv("API_BASE_URL", "http://localhost:8000"),
    "timeout": int(os.getenv("API_TIMEOUT", "30")),
    "retry_attempts": int(os.getenv("API_RETRY_ATTEMPTS", "3")),
}

# Feature flags
FEATURES = {
    "patient_search": True,
    "appointment_scheduling": True,
    "prescription_management": True,
    "analytics_charts": True,
    "activity_feed": True,
    "report_generation": True,
}

# UI settings
UI_CONFIG = {
    "theme": "light",
    "primary_color": "#3b82f6",
    "secondary_color": "#10b981",
    "accent_color": "#f59e0b",
    "danger_color": "#ef4444",
    "max_width": 1200,
}

# Sample data settings
SAMPLE_DATA = {
    "max_patients": 100,
    "max_appointments": 50,
    "max_prescriptions": 75,
    "refresh_interval": 300,  # seconds
}
