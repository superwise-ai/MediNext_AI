"""
Dashboard Cards Component for MediNext AI

This component creates the summary cards for key metrics based on real patient data.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from app.utils.css_styles import get_common_styles


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


def calculate_patient_metrics(df):
    """Calculate key metrics from patient data"""
    if df is None or len(df) == 0:
        return {
            "total_patients": 0,
            "active_patients": 0,
            "critical_alerts": 0,
            "avg_age": 0,
            "diabetes_patients": 0,
            "hypertension_patients": 0,
            "guardrail_violations": 0,
            "recent_visits": 0,
        }

    # Calculate age
    df["age"] = (datetime.now() - df["birth_date"]).dt.days / 365.25

    # Active patients (visited in last 6 months)
    six_months_ago = datetime.now() - timedelta(days=180)
    active_patients = len(df[df["last_visit"] >= six_months_ago])

    # Recent visits (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_visits = len(df[df["last_visit"] >= thirty_days_ago])

    # Critical alerts (high glucose or low hemoglobin)
    critical_alerts = len(
        df[
            (df["glucose"] > 200)
            | (df["hemoglobin"] < 12)
            | (df["guardrail_violation_flag"] == True)
        ]
    )

    # Condition counts
    diabetes_patients = len(
        df[df["conditions"].str.contains("diabetes", case=False, na=False)]
    )
    hypertension_patients = len(
        df[df["conditions"].str.contains("hypertension", case=False, na=False)]
    )

    return {
        "total_patients": len(df),
        "active_patients": active_patients,
        "critical_alerts": critical_alerts,
        "avg_age": df["age"].mean(),
        "diabetes_patients": diabetes_patients,
        "hypertension_patients": hypertension_patients,
        "guardrail_violations": df["guardrail_violation_flag"].sum(),
        "recent_visits": recent_visits,
    }


def create_dashboard_cards():
    """
    Creates the dashboard summary cards for key metrics based on real patient data.

    Returns:
        None: Renders the cards directly to the Streamlit app
    """

    # Load patient data
    df = load_patient_data()
    metrics = calculate_patient_metrics(df)

    # Load common CSS styles
    st.markdown(get_common_styles(), unsafe_allow_html=True)

    # Create three columns for the metric cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
        <div class="metric-card" style="border-left-color: #3b82f6;">
            <div class="card-header">
                <div class="card-icon" style="background-color: #dbeafe; color: #1d4ed8;">
                    👥
                </div>
                <div>
                    <p class="card-title">Total Patients</p>
                </div>
            </div>
            <h2 class="card-value">{metrics['total_patients']:,}</h2>
            <p class="card-change">↗️ {metrics['active_patients']} active (6 months)</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="metric-card" style="border-left-color: #10b981;">
            <div class="card-header">
                <div class="card-icon" style="background-color: #d1fae5; color: #047857;">
                    📅
                </div>
                <div>
                    <p class="card-title">Recent Visits</p>
                </div>
            </div>
            <h2 class="card-value">{metrics['recent_visits']}</h2>
            <p class="card-change">↗️ Last 30 days</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class="metric-card" style="border-left-color: #f59e0b;">
            <div class="card-header">
                <div class="card-icon" style="background-color: #fef3c7; color: #d97706;">
                    🔬
                </div>
                <div>
                    <p class="card-title">Avg Age</p>
                </div>
            </div>
            <h2 class="card-value">{metrics['avg_age']:.1f}</h2>
            <p class="card-change">📊 Years</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Additional metrics row
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
        <div class="metric-card" style="border-left-color: #8b5cf6;">
            <div class="card-header">
                <div class="card-icon" style="background-color: #ede9fe; color: #6d28d9;">
                    💊
                </div>
                <div>
                    <p class="card-title">Diabetes Patients</p>
                </div>
            </div>
            <h2 class="card-value">{metrics['diabetes_patients']}</h2>
            <p class="card-change">📈 {metrics['diabetes_patients']/metrics['total_patients']*100:.1f}% of total</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="metric-card" style="border-left-color: #06b6d4;">
            <div class="card-header">
                <div class="card-icon" style="background-color: #cffafe; color: #0891b2;">
                    ❤️
                </div>
                <div>
                    <p class="card-title">Hypertension</p>
                </div>
            </div>
            <h2 class="card-value">{metrics['hypertension_patients']}</h2>
            <p class="card-change">📈 {metrics['hypertension_patients']/metrics['total_patients']*100:.1f}% of total</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class="metric-card" style="border-left-color: #ef4444;">
            <div class="card-header">
                <div class="card-icon" style="background-color: #fee2e2; color: #dc2626;">
                    🏥
                </div>
                <div>
                    <p class="card-title">Health Status</p>
                </div>
            </div>
            <h2 class="card-value">{metrics['total_patients'] - metrics['diabetes_patients'] - metrics['hypertension_patients']}</h2>
            <p class="card-change">✅ Healthy patients</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

