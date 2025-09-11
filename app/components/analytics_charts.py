"""
Analytics Charts Component for MediNext AI

This component creates the analytics charts for data visualization based on real patient data.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
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


def analyze_patient_data(df):
    """Analyze patient data for charts"""
    if df is None or len(df) == 0:
        return None

    # Calculate age (round to whole number)
    df["age"] = ((datetime.now() - df["birth_date"]).dt.days / 365.25).round(0).astype(int)

    # Extract conditions
    all_conditions = []
    for conditions in df["conditions"].dropna():
        if conditions:
            # Split multiple conditions
            condition_list = [c.strip() for c in conditions.split(",")]
            all_conditions.extend(condition_list)

    # Count conditions
    condition_counts = pd.Series(all_conditions).value_counts().head(10)

    # Age distribution
    age_bins = [0, 18, 30, 45, 60, 75, 100]
    age_labels = ["0-18", "19-30", "31-45", "46-60", "61-75", "75+"]
    df["age_group"] = pd.cut(df["age"], bins=age_bins, labels=age_labels, right=False)
    age_distribution = df["age_group"].value_counts().sort_index()

    # Gender distribution
    gender_distribution = df["sex"].value_counts()

    # Visit patterns (last 12 months)
    twelve_months_ago = datetime.now() - timedelta(days=365)
    recent_visits = df[df["last_visit"] >= twelve_months_ago]
    visit_by_month = recent_visits.groupby(
        recent_visits["last_visit"].dt.to_period("M")
    ).size()

    # Health metrics distribution
    glucose_ranges = [0, 70, 100, 126, 200, 300]
    glucose_labels = ["Low", "Normal", "Pre-diabetes", "Diabetes", "High"]
    df["glucose_category"] = pd.cut(
        df["glucose"], bins=glucose_ranges, labels=glucose_labels, right=False
    )
    glucose_distribution = df["glucose_category"].value_counts()

    hemoglobin_ranges = [0, 12, 13, 16, 20]
    hemoglobin_labels = ["Low", "Normal", "High", "Very High"]
    df["hemoglobin_category"] = pd.cut(
        df["hemoglobin"], bins=hemoglobin_ranges, labels=hemoglobin_labels, right=False
    )
    hemoglobin_distribution = df["hemoglobin_category"].value_counts()

    return {
        "condition_counts": condition_counts,
        "age_distribution": age_distribution,
        "gender_distribution": gender_distribution,
        "visit_by_month": visit_by_month,
        "glucose_distribution": glucose_distribution,
        "hemoglobin_distribution": hemoglobin_distribution,
        "total_patients": len(df),
        "avg_age": round(df["age"].mean()),
        "avg_glucose": df["glucose"].mean(),
        "avg_hemoglobin": df["hemoglobin"].mean(),
    }


def create_analytics_charts():
    """
    Creates the analytics charts component with real patient data visualization.

    Returns:
        None: Renders the charts directly to the Streamlit app
    """

    # Load and analyze patient data
    df = load_patient_data()
    analysis = analyze_patient_data(df)

    if analysis is None:
        st.error("❌ Unable to load patient data for analytics")
        return

    # Load common CSS styles
    st.markdown(get_common_styles(), unsafe_allow_html=True)

    # Analytics section container
    st.markdown(
        """
    <div class="analytics-section">
        <div class="section-header">
            <span class="section-icon">📊</span>
            <h3 class="section-title">Patient Analytics</h3>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Key metrics row
    st.markdown("### Key Patient Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Patients", f"{analysis['total_patients']:,}")

    with col2:
        st.metric("Average Age", f"{analysis['avg_age']:.0f}")

    with col3:
        st.metric("Average Glucose", f"{analysis['avg_glucose']:.1f} mg/dL")

    with col4:
        st.metric("Average Hemoglobin", f"{analysis['avg_hemoglobin']:.1f} g/dL")

    st.markdown("---")

    # Charts section
    st.markdown("### Patient Demographics & Health Metrics")

    # Row 1: Age and Gender Distribution
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Age Distribution")

        age_df = pd.DataFrame(
            {
                "Age Group": analysis["age_distribution"].index,
                "Patient Count": analysis["age_distribution"].values,
            }
        )

        fig_age = px.bar(
            age_df,
            x="Age Group",
            y="Patient Count",
            title="Patient Age Distribution",
            template="plotly_white",
            color="Patient Count",
            color_continuous_scale="Blues",
        )

        fig_age.update_layout(
            height=400, margin=dict(l=20, r=20, t=40, b=20), showlegend=False
        )

        st.plotly_chart(fig_age, use_container_width=True)

    with col2:
        st.markdown("#### Gender Distribution")

        gender_df = pd.DataFrame(
            {
                "Gender": analysis["gender_distribution"].index,
                "Count": analysis["gender_distribution"].values,
            }
        )

        fig_gender = px.pie(
            gender_df,
            values="Count",
            names="Gender",
            title="Patient Gender Distribution",
            template="plotly_white",
        )

        fig_gender.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))

        st.plotly_chart(fig_gender, use_container_width=True)

    # Row 2: Health Metrics
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Glucose Levels Distribution")

        glucose_df = pd.DataFrame(
            {
                "Category": analysis["glucose_distribution"].index,
                "Patient Count": analysis["glucose_distribution"].values,
            }
        )

        fig_glucose = px.bar(
            glucose_df,
            x="Category",
            y="Patient Count",
            title="Glucose Levels Distribution",
            template="plotly_white",
            color="Patient Count",
            color_continuous_scale="Reds",
        )

        fig_glucose.update_layout(
            height=400, margin=dict(l=20, r=20, t=40, b=20), showlegend=False
        )

        st.plotly_chart(fig_glucose, use_container_width=True)

    with col2:
        st.markdown("#### Hemoglobin Levels Distribution")

        hemoglobin_df = pd.DataFrame(
            {
                "Category": analysis["hemoglobin_distribution"].index,
                "Patient Count": analysis["hemoglobin_distribution"].values,
            }
        )

        fig_hemoglobin = px.bar(
            hemoglobin_df,
            x="Category",
            y="Patient Count",
            title="Hemoglobin Levels Distribution",
            template="plotly_white",
            color="Patient Count",
            color_continuous_scale="Greens",
        )

        fig_hemoglobin.update_layout(
            height=400, margin=dict(l=20, r=20, t=40, b=20), showlegend=False
        )

        st.plotly_chart(fig_hemoglobin, use_container_width=True)

    # Row 3: Medical Conditions and Visit Patterns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Top Medical Conditions")

        conditions_df = pd.DataFrame(
            {
                "Condition": analysis["condition_counts"].index,
                "Patient Count": analysis["condition_counts"].values,
            }
        )

        fig_conditions = px.bar(
            conditions_df,
            x="Patient Count",
            y="Condition",
            orientation="h",
            title="Top Medical Conditions",
            template="plotly_white",
            color="Patient Count",
            color_continuous_scale="Purples",
        )

        fig_conditions.update_layout(
            height=400, margin=dict(l=20, r=20, t=40, b=20), showlegend=False
        )

        st.plotly_chart(fig_conditions, use_container_width=True)

    with col2:
        st.markdown("#### Visit Patterns (Last 12 Months)")

        if len(analysis["visit_by_month"]) > 0:
            visits_df = pd.DataFrame(
                {
                    "Month": [str(x) for x in analysis["visit_by_month"].index],
                    "Visits": analysis["visit_by_month"].values,
                }
            )

            fig_visits = px.line(
                visits_df,
                x="Month",
                y="Visits",
                title="Patient Visits Over Time",
                template="plotly_white",
                markers=True,
            )

            fig_visits.update_layout(
                height=400, margin=dict(l=20, r=20, t=40, b=20), showlegend=False
            )

            fig_visits.update_traces(
                line_color="#3b82f6",
                line_width=3,
                marker_color="#3b82f6",
                marker_size=6,
            )

            st.plotly_chart(fig_visits, use_container_width=True)
        else:
            st.info("No recent visit data available")

    # Additional insights
    st.markdown("---")
    st.markdown("### Health Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Health Risk Analysis")

        # Calculate health risks
        high_glucose = len(df[df["glucose"] > 126])
        low_hemoglobin = len(df[df["hemoglobin"] < 12])
        guardrail_violations = df["guardrail_violation_flag"].sum()

        risk_data = {
            "Risk Type": ["High Glucose", "Low Hemoglobin", "Guardrail Violations"],
            "Patient Count": [high_glucose, low_hemoglobin, guardrail_violations],
        }

        risk_df = pd.DataFrame(risk_data)

        fig_risk = px.bar(
            risk_df,
            x="Risk Type",
            y="Patient Count",
            title="Health Risk Distribution",
            template="plotly_white",
            color="Patient Count",
            color_continuous_scale="Oranges",
        )

        fig_risk.update_layout(
            height=300, margin=dict(l=20, r=20, t=40, b=20), showlegend=False
        )

        st.plotly_chart(fig_risk, use_container_width=True)

    with col2:
        st.markdown("#### Patient Health Overview")

        # Create a summary table
        summary_data = {
            "Metric": [
                "Total Patients",
                "Average Age",
                "Diabetes Patients",
                "Hypertension Patients",
                "Critical Alerts",
            ],
            "Value": [
                int(analysis["total_patients"]),
                int(round(analysis['avg_age'])),
                int(len(
                    df[df["conditions"].str.contains("diabetes", case=False, na=False)]
                )),
                int(len(
                    df[
                        df["conditions"].str.contains(
                            "hypertension", case=False, na=False
                        )
                    ]
                )),
                int(len(
                    df[
                        (df["glucose"] > 200)
                        | (df["hemoglobin"] < 12)
                        | (df["guardrail_violation_flag"] == True)
                    ]
                )),
            ],
        }

        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
