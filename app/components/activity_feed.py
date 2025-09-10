"""
Activity Feed Component for MediNext AI

This component creates the recent activities display based on real patient data.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from app.utils.logger import get_logger
from app.utils.css_styles import get_common_styles

# Initialize logger
logger = get_logger(__name__)


def load_patient_data():
    """Load patient data from CSV file"""
    try:
        csv_path = "app/assets/synthetic_ehr_data.csv"
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            # Convert dates
            df["birth_date"] = pd.to_datetime(df["birth_date"], errors="coerce")
            df["last_visit"] = pd.to_datetime(df["last_visit"], errors="coerce")
            # Convert numeric fields
            df["hemoglobin"] = pd.to_numeric(df["hemoglobin"], errors="coerce")
            df["glucose"] = pd.to_numeric(df["glucose"], errors="coerce")
            return df
        else:
            return None
    except Exception as e:
        st.error(f"Error loading patient data: {str(e)}")
        return None


def generate_activities_from_data(df):
    """Generate realistic activities based on patient data"""
    if df is None or len(df) == 0:
        return []

    activities = []

    # Get recent patients (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_patients = df[df["last_visit"] >= thirty_days_ago].head(10)

    # Generate activities based on patient data
    for idx, patient in recent_patients.iterrows():
        # Calculate time ago
        visit_time = patient["last_visit"]
        time_diff = datetime.now() - visit_time
        hours_ago = int(time_diff.total_seconds() / 3600)

        if hours_ago < 24:
            time_str = f"{hours_ago} hours ago"
        else:
            days_ago = hours_ago // 24
            time_str = f"{days_ago} days ago"

        # Generate activity based on patient conditions and metrics
        patient_name = patient["name"]

        # Check for critical conditions
        if patient["glucose"] > 200:
            activities.append(
                {
                    "time": time_str,
                    "activity": f"Critical: High glucose level ({patient['glucose']:.1f} mg/dL) detected for {patient_name}",
                    "type": "alert",
                    "priority": "critical",
                }
            )

        if patient["hemoglobin"] < 12:
            activities.append(
                {
                    "time": time_str,
                    "activity": f"Alert: Low hemoglobin ({patient['hemoglobin']:.1f} g/dL) for {patient_name}",
                    "type": "alert",
                    "priority": "critical",
                }
            )

        if patient["guardrail_violation_flag"]:
            activities.append(
                {
                    "time": time_str,
                    "activity": f"Guardrail violation detected for {patient_name}",
                    "type": "alert",
                    "priority": "critical",
                }
            )

        # Regular activities
        if "diabetes" in str(patient["conditions"]).lower():
            activities.append(
                {
                    "time": time_str,
                    "activity": f"Diabetes management review completed for {patient_name}",
                    "type": "questionnaire",
                    "priority": "normal",
                }
            )

        if "hypertension" in str(patient["conditions"]).lower():
            activities.append(
                {
                    "time": time_str,
                    "activity": f"Blood pressure monitoring scheduled for {patient_name}",
                    "type": "appointment",
                    "priority": "normal",
                }
            )

        # Lab results
        if patient["glucose"] > 126:
            activities.append(
                {
                    "time": time_str,
                    "activity": f"Lab results: Elevated glucose levels for {patient_name}",
                    "type": "lab_result",
                    "priority": "normal",
                }
            )

        # Prescription activities
        if pd.notna(patient["medications"]) and patient["medications"]:
            activities.append(
                {
                    "time": time_str,
                    "activity": f"Prescription review completed for {patient_name}",
                    "type": "prescription",
                    "priority": "normal",
                }
            )

    # Sort by time (most recent first)
    activities.sort(key=lambda x: x["time"])

    # Limit to 10 most recent activities
    return activities[:10]


def create_activity_feed():
    """
    Creates the recent activities feed component based on real patient data.

    Returns:
        None: Renders the activity feed directly to the Streamlit app
    """

    # Load patient data and generate activities
    df = load_patient_data()
    activities = generate_activities_from_data(df)

    # Load common CSS styles
    st.markdown(get_common_styles(), unsafe_allow_html=True)

    # Activity feed container
    st.markdown(
        """
    <div class="activity-feed">
        <div class="feed-header">
            <span class="feed-icon">📋</span>
            <h3 class="feed-title">Recent Patient Activities</h3>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if not activities:
        st.info("📊 No recent patient activities to display")
        return

    # Display activities
    for i, activity in enumerate(activities):
        # Determine icon based on activity type
        icon_map = {
            "lab_result": "🔬",
            "appointment": "📅",
            "prescription": "💊",
            "alert": "⚠️",
            "questionnaire": "📝",
        }

        icon = icon_map.get(activity["type"], "📋")
        priority_class = f"priority-{activity['priority']}"

        # Create activity item
        col1, col2, col3 = st.columns([0.1, 0.7, 0.2])

        with col1:
            st.markdown(
                f"<div class='activity-icon' style='background-color: #f3f4f6; color: #6b7280;'>{icon}</div>",
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"<p class='activity-text'>{activity['activity']}</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p class='activity-time'>{activity['time']}</p>",
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                f"<span class='activity-priority {priority_class}'>{activity['priority']}</span>",
                unsafe_allow_html=True,
            )

    # Refresh button
    if st.button("🔄 Refresh Activities", key="refresh_activities"):
        st.rerun()

    # Activity summary
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Activities", len(activities))
    with col2:
        critical_count = len([a for a in activities if a["priority"] == "critical"])
        st.metric("Critical Alerts", critical_count, delta=critical_count)
    with col3:
        normal_count = len([a for a in activities if a["priority"] == "normal"])
        st.metric("Normal Activities", normal_count)
