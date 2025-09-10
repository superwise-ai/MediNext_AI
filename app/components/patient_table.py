"""
Patient Table Component for EHR Demo Portal

This component creates the patient search and data table with CSV integration.
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
    """Load patient data from CSV file or use sample data as fallback"""
    try:
        # Try to load from CSV file in assets directory
        csv_path = "app/assets/synthetic_ehr_data.csv"
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)

            # Validate the CSV structure
            if validate_patient_csv(df):
                return df
            else:
                st.error("❌ CSV structure is invalid. Using sample data.")
                return get_sample_data()
        else:
            st.info(
                "📁 No CSV file found. Using sample data. Place synthetic_ehr_data.csv in app/assets/ to use real data."
            )
            return get_sample_data()

    except Exception as e:
        st.error(f"❌ Error loading CSV: {str(e)}")
        st.info("📁 Using sample data as fallback.")
        return get_sample_data()


def rename_columns_for_display(df):
    """Rename columns to match our display requirements"""
    # Create a copy to avoid modifying the original
    display_df = df.copy()

    # Rename columns for better display
    column_mapping = {"sex": "gender", "conditions": "medical_conditions"}

    # Only rename columns that exist
    for old_name, new_name in column_mapping.items():
        if old_name in display_df.columns:
            display_df = display_df.rename(columns={old_name: new_name})

    return display_df


def validate_patient_csv(df):
    """Validate that the CSV has the required columns and data types"""
    # These are the columns we actually need from your CSV (excluding extra columns)
    required_columns = [
        "patient_id",
        "name",
        "sex",
        "birth_date",
        "address",
        "last_visit",
        "conditions",
        "medications",
        "hemoglobin",
        "glucose",
        "ssn",
        "phone_number",
        "guardrail_violation_flag",
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
        return False

    # Check for empty values in critical fields
    critical_fields = ["patient_id", "name"]
    empty_critical = df[critical_fields].isnull().any(axis=1)

    if empty_critical.any():
        st.warning(
            f"⚠️ {empty_critical.sum()} patients have missing critical information"
        )

    # Validate data types
    try:
        # Convert dates
        df["birth_date"] = pd.to_datetime(df["birth_date"], errors="coerce")
        df["last_visit"] = pd.to_datetime(df["last_visit"], errors="coerce")

        # Convert numeric fields
        df["hemoglobin"] = pd.to_numeric(df["hemoglobin"], errors="coerce")
        df["glucose"] = pd.to_numeric(df["glucose"], errors="coerce")

        # Convert boolean
        df["guardrail_violation_flag"] = df["guardrail_violation_flag"].astype(bool)

    except Exception as e:
        st.error(f"❌ Data type conversion error: {str(e)}")
        return False

    return True


def get_sample_data():
    """Generate sample data matching your CSV structure"""
    return pd.DataFrame(
        {
            "patient_id": ["P001", "P002", "P003", "P004", "P005"],
            "first_name": ["John", "Jane", "Mike", "Sarah", "David"],  # Will be ignored
            "middle_initial": ["A", "B", "C", "D", "E"],  # Will be ignored
            "last_name": [
                "Doe",
                "Smith",
                "Johnson",
                "Wilson",
                "Brown",
            ],  # Will be ignored
            "name": [
                "John A Doe",
                "Jane B Smith",
                "Mike C Johnson",
                "Sarah D Wilson",
                "David E Brown",
            ],
            "sex": ["M", "F", "M", "F", "M"],  # Will be displayed as 'gender'
            "birth_date": [
                "1979-05-15",
                "1992-08-20",
                "1966-03-10",
                "1995-11-25",
                "1957-12-03",
            ],
            "address": [
                "123 Main St",
                "456 Oak Ave",
                "789 Pine Rd",
                "321 Elm St",
                "654 Maple Dr",
            ],
            "last_visit": [
                "2024-01-15",
                "2024-01-20",
                "2024-01-18",
                "2024-01-22",
                "2024-01-19",
            ],
            "conditions": [
                "Hypertension",
                "Diabetes",
                "Asthma",
                "None",
                "Arthritis",
            ],  # Will be displayed as 'medical_conditions'
            "medications": [
                "Lisinopril",
                "Metformin",
                "Albuterol",
                "None",
                "Ibuprofen",
            ],
            "hemoglobin": [14.2, 13.8, 15.1, 14.5, 13.9],
            "glucose": [95, 120, 88, 92, 105],
            "ssn": [
                "123-45-6789",
                "234-56-7890",
                "345-67-8901",
                "456-78-9012",
                "567-89-0123",
            ],
            "phone_number": [
                "555-0101",
                "555-0102",
                "555-0103",
                "555-0104",
                "555-0105",
            ],
            "guardrail_violation_flag": [False, True, False, False, True],
        }
    )


def create_patient_table():
    """
    Creates the patient search and data table component with CSV integration.

    Returns:
        None: Renders the table directly to the Streamlit app
    """

    # Load patient data
    df = load_patient_data()

    # Load common CSS styles
    st.markdown(get_common_styles(), unsafe_allow_html=True)

    # Enhanced summary statistics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Patients", len(df))
    with col2:
        # Calculate active patients (visited in last year)
        if "last_visit" in df.columns:
            try:
                last_visit_dates = pd.to_datetime(df["last_visit"], errors="coerce")
                active_patients = len(
                    last_visit_dates[
                        last_visit_dates >= datetime.now() - timedelta(days=365)
                    ]
                )
                st.metric("Active Patients (1 year)", active_patients)
            except:
                st.metric("Active Patients", "N/A")
        else:
            st.metric("Active Patients", "N/A")
    with col3:
        if "guardrail_violation_flag" in df.columns:
            guardrail_violations = df["guardrail_violation_flag"].sum()
            st.metric("Guardrail Violations", guardrail_violations)
        else:
            st.metric("Guardrail Violations", "N/A")
    with col4:
        if "hemoglobin" in df.columns:
            try:
                avg_hemoglobin = df["hemoglobin"].mean()
                st.metric("Avg Hemoglobin", f"{avg_hemoglobin:.1f} g/dL")
            except:
                st.metric("Avg Hemoglobin", "N/A")
        else:
            st.metric("Avg Hemoglobin", "N/A")
    with col5:
        if "glucose" in df.columns:
            try:
                avg_glucose = df["glucose"].mean()
                st.metric("Avg Glucose", f"{avg_glucose:.0f} mg/dL")
            except:
                st.metric("Avg Glucose", "N/A")
        else:
            st.metric("Avg Glucose", "N/A")

    st.markdown("---")

    # Session state for pagination
    if "current_page_number" not in st.session_state:
        st.session_state.current_page_number = 1
    if "page_size" not in st.session_state:
        st.session_state.page_size = 10

    # Enhanced search functionality
    search_term = st.text_input(
        "🔍 Search patients by ID, name, medical conditions, or medications:",
        placeholder="Type to search...",
        key="patient_search",
    )

    # Filter data based on search across multiple columns
    if search_term:
        # Use original column names for filtering
        filtered_df = df[
            df["patient_id"].str.contains(search_term, case=False, na=False)
            | df["name"].str.contains(search_term, case=False, na=False)
            | df["conditions"].str.contains(search_term, case=False, na=False)
            | df["medications"].str.contains(search_term, case=False, na=False)
            | df["glucose"].astype(str).str.contains(search_term, case=False, na=False)
            | df["ssn"].str.contains(search_term, case=False, na=False)
        ]

    else:
        filtered_df = df

    # Display patient table
    st.markdown("### Patient List")

    # Show total records info
    total_records = len(filtered_df)
    st.caption(f"📊 Total records: {total_records}")

    # Create display dataframe with all columns and rename for display
    display_columns = [
        "patient_id",
        "name",
        "sex",
        "birth_date",
        "last_visit",
        "conditions",
        "medications",
        "glucose",
        "hemoglobin",
        "guardrail_violation_flag",
    ]

    display_df = filtered_df[display_columns]

    # Rename columns for display
    column_rename_map = {
        "sex": "gender",
        "conditions": "medical_conditions",
        "glucose": "glucose_mg/dL",
        "hemoglobin": "hemoglobin_g/dL",
    }

    display_df = display_df.rename(columns=column_rename_map)

    # Convert guardrail_violation_flag to Yes/No for display
    display_df["guardrail_violation_flag"] = display_df["guardrail_violation_flag"].map(
        {True: "Yes", False: "No"}
    )

    # Format dates to dd-MMM-yyyy format
    def format_date(date_val):
        try:
            if pd.isna(date_val):
                return "N/A"
            # Parse the date and format it
            parsed_date = pd.to_datetime(date_val)
            return parsed_date.strftime("%d-%b-%Y")
        except:
            return str(date_val)

    # Apply date formatting
    display_df["birth_date"] = display_df["birth_date"].apply(format_date)
    display_df["last_visit"] = display_df["last_visit"].apply(format_date)

    # Custom Pagination

    page_size = st.selectbox(
        "Rows per page",
        [10, 20, 50, 100],
        index=[10, 20, 50, 100].index(st.session_state.page_size),
        key="page_size_selector",
    )
    st.session_state.page_size = page_size
    total_records = len(display_df)
    total_pages = max(1, (total_records - 1) // page_size + 1)

    # Clamp page if search reduced total_pages
    if st.session_state.current_page_number > total_pages:
        st.session_state.current_page_number = total_pages

    start_idx = (st.session_state.current_page_number - 1) * page_size
    end_idx = start_idx + page_size
    page_df = display_df.iloc[start_idx:end_idx]

    logger.info(f"Session state: {st.session_state}")
    # Ensure page state exists
    if "current_page" not in st.session_state:
        st.session_state.current_page = "patients"

    # Click to select rows, then show selected data
    event = st.dataframe(
        page_df,
        key="patient_dataframe",
        on_select="rerun",
        selection_mode=["single-row"],
    )

    # Pagination controls
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Previous", disabled=st.session_state.current_page_number <= 1):
            st.session_state.current_page_number -= 1
            st.rerun()
    with col2:
        st.markdown(
            f"<div style='text-align:center;'>Page {st.session_state.current_page_number} of {total_pages}</div>",
            unsafe_allow_html=True,
        )
    with col3:
        if st.button(
            "Next ➡️", disabled=st.session_state.current_page_number >= total_pages
        ):
            st.session_state.current_page_number += 1
            st.rerun()

    logger.info(f"Event: {event}")
    logger.info(f"After set Session state: {st.session_state}")

    # Store selection in session state to prevent redirects
    if event.selection.rows:
        st.session_state.selected_patient_rows = event.selection.rows
        st.session_state.selected_patient_data = page_df.iloc[event.selection.rows]
        logger.info(f"Patient row selected: {event.selection.rows}")
        logger.info(
            f"Selected patient data: {st.session_state.selected_patient_data.to_dict('records')}"
        )

        # Redirect to patient details page with selected patient data
        st.session_state.current_page = "patient_details"
        st.rerun()
