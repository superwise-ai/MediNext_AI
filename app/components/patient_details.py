"""
Patient Details Component for EHR Demo Portal

This component displays detailed patient information with Superwise integration.
"""

import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
from app.utils.logger import get_logger
from app.utils.css_styles import get_common_styles
import os
from app.config.api_config import (
    get_superwise_headers,
    validate_api_config,
    SUPERWISE_API_URL,
    API_TIMEOUT,
    SUPERWISE_API_VERSION,
    SUPERWISE_APP_ID,
)

# Initialize logger
logger = get_logger(__name__)


def calculate_age(birth_date):
    """
    Calculate age from birth date
    
    Args:
        birth_date (str): Birth date in format 'YYYY-MM-DD' or 'MM/DD/YYYY' or 'DD-MMM-YYYY'
    
    Returns:
        int: Age in years, or None if invalid date format
    """
    try:
        # Handle different date formats
        if isinstance(birth_date, str):
            # Try different date formats - prioritize dd-MMM-yyyy format
            for fmt in ['%d-%b-%Y', '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S']:
                try:
                    birth_dt = datetime.strptime(birth_date, fmt)
                    break
                except ValueError:
                    continue
            else:
                logger.warning(f"Could not parse birth date: {birth_date}")
                return None
        else:
            # If it's already a datetime object
            birth_dt = birth_date
        
        # Calculate age
        today = datetime.now()
        age = today.year - birth_dt.year
        
        # Adjust if birthday hasn't occurred this year
        if today.month < birth_dt.month or (today.month == birth_dt.month and today.day < birth_dt.day):
            age -= 1
            
        return age
        
    except Exception as e:
        logger.error(f"Error calculating age from {birth_date}: {str(e)}")
        return None


def call_superwise_api(patient_data):
    """
    Call the Superwise API with patient data

    Args:
        patient_data (dict): Patient information

    Returns:
        dict: API response or error message
    """
    # Validate API configuration
    if not validate_api_config():
        return {
            "success": False,
            "error": "Configuration Error",
            "message": "Superwise API configuration is missing. Please set environment variables in .env file.",
        }

    age = calculate_age(patient_data['birth_date']) if patient_data['birth_date'] else ""
    
    try:
        # Prepare the request payload
        payload = {
            "input": f"""Here is de-identified patient information:
                        - Age: {age}
                        {f"- SSN: {patient_data.get('ssn', '').strip()}" if patient_data.get('ssn', '').strip() else ""}
                        {f"- Phone Number: {patient_data.get('phone_number', '').strip()}" if patient_data.get('phone_number', '').strip() else ""}
                        - Gender: {patient_data['sex']}
                        - Medical Conditions: {patient_data['conditions']}
                        - Hemoglobin Level: {patient_data['hemoglobin']} g/dL
                        - Current Medications: {patient_data['medications']}
                        - Glucose Level: {patient_data['glucose']} mg/dL

                        Please provide:

                        1. General interpretation of this data (clinical significance).
                        2. General next steps a healthcare professional might consider.
                        
                        Keep the details concise so doctors can read quickly and provide their judgment.""",
            "chat_history": [],
        }

        # Get headers from configuration
        headers = get_superwise_headers()

        # Build API URL
        api_url = f"{SUPERWISE_API_URL}{SUPERWISE_API_VERSION}/app-worker/{SUPERWISE_APP_ID}/{SUPERWISE_API_VERSION}/ask"

        # Make the API call
        logger.info(f"Calling Superwise API for patient: {patient_data['patient_id']}")
        logger.info(f"Payload: {payload}")
        response = requests.post(
            api_url, json=payload, headers=headers, timeout=API_TIMEOUT
        )

        # Check if request was successful
        if response.status_code == 200:
            api_response = response.json()
            logger.info(
                f"Superwise API call successful for patient: {patient_data['patient_id']}"
            )
            return {
                "success": True,
                "data": api_response,
                "message": "Analysis completed successfully",
            }
        else:
            logger.error(
                f"Superwise API error: {response.status_code} - {response.text}"
            )
            return {
                "success": False,
                "error": f"API Error: {response.status_code}",
                "message": "Failed to get analysis from Superwise",
            }

    except requests.exceptions.Timeout:
        logger.error("Superwise API timeout")
        return {
            "success": False,
            "error": "Timeout",
            "message": "Request timed out. Please try again.",
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Superwise API request error: {str(e)}")
        return {
            "success": False,
            "error": "Request Error",
            "message": f"Failed to connect to Superwise API: {str(e)}",
        }
    except Exception as e:
        logger.error(f"Unexpected error in Superwise API call: {str(e)}")
        return {
            "success": False,
            "error": "Unexpected Error",
            "message": f"An unexpected error occurred: {str(e)}",
        }


def get_sample_patient_data():
    """Generate sample patient data for demonstration"""
    return {
        "patient_id": "P001",
        "first_name": "John",
        "middle_initial": "A",
        "last_name": "Doe",
        "name": "John A Doe",
        "sex": "M",
        "birth_date": "1979-05-15",
        "age": calculate_age("1979-05-15"),
        "address": "123 Main St, Anytown, ST 12345",
        "last_visit": "2024-01-15",
        "conditions": "Hypertension, Type 2 Diabetes",
        "medications": "Lisinopril 10mg daily, Metformin 500mg twice daily",
        "hemoglobin": 14.2,
        "glucose": 95,
        "ssn": "123-45-6789",
        "phone_number": "555-0101",
    }

def create_patient_details():
    """
    Creates the patient details component with comprehensive patient information.

    Returns:
        None: Renders the component directly to the Streamlit app
    """

    # Get patient data from session state or use sample data as fallback
    if (
        "selected_patient_data" in st.session_state
        and st.session_state.selected_patient_data is not None
    ):
        # Convert the selected patient data to the format expected by the component
        selected_patient = st.session_state.selected_patient_data.iloc[0]

        # Map the display data back to the original format
        patient_data = {
            "patient_id": selected_patient["patient_id"],
            "first_name": (
                selected_patient["name"].split()[0]
                if len(selected_patient["name"].split()) > 0
                else ""
            ),
            "middle_initial": (
                selected_patient["name"].split()[1]
                if len(selected_patient["name"].split()) > 1
                else ""
            ),
            "last_name": (
                selected_patient["name"].split()[2]
                if len(selected_patient["name"].split()) > 2
                else ""
            ),
            "name": selected_patient["name"],
            "sex": selected_patient.get("gender", "M"),
            "birth_date": selected_patient["birth_date"],
            "address": selected_patient.get("address", ""),
            "last_visit": selected_patient["last_visit"],
            "conditions": selected_patient.get("medical_conditions", "None"),
            "medications": selected_patient.get("medications", "None"),
            "hemoglobin": float(selected_patient.get("hemoglobin_g/dL", 14.0)),
            "glucose": float(selected_patient.get("glucose_mg/dL", 100)),
            "ssn": selected_patient.get("ssn", ""),
            "phone_number": selected_patient.get("phone_number", ""),
        }
    else:
        # Use sample data if no patient is selected
        patient_data = get_sample_patient_data()

    # Load common CSS styles
    st.markdown(get_common_styles(), unsafe_allow_html=True)

    # Patient Details Header
    st.markdown(
        """
    <div class="patient-details-container">
        <div class="patient-header">
            <div>
                <h1 class="patient-name">{name}</h1>
                <p class="patient-id">Patient ID: {patient_id}</p>
            </div>
        </div>
    """.format(
            name=patient_data["name"], patient_id=patient_data["patient_id"]
        ),
        unsafe_allow_html=True,
    )

    # Personal Information Section
    st.markdown("### 📋 Personal Information")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Full Name:**")
        st.write(
            f"{patient_data['first_name']} {patient_data['middle_initial']} {patient_data['last_name']}"
        )

        st.markdown("**Gender:**")
        st.write(patient_data["sex"])

        st.markdown("**Date of Birth:**")
        st.write(patient_data["birth_date"])

        st.markdown("**SSN:**")
        st.write(patient_data["ssn"])

    with col2:
        st.markdown("**Address:**")
        st.write(patient_data["address"])

        st.markdown("**Phone Number:**")
        st.write(patient_data["phone_number"])

        st.markdown("**Last Visit:**")
        st.write(patient_data["last_visit"])

    st.markdown("---")

    # Medical Information Section
    st.markdown("### 🏥 Medical Information")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Medical Conditions:**")
        st.write(patient_data["conditions"])

        st.markdown("**Current Medications:**")
        # Handle empty/None medications - replace nan with "-"
        medications_value = patient_data["medications"]
        if (
            pd.isna(medications_value)
            or medications_value == "None"
            or medications_value == ""
            or str(medications_value).lower() == "nan"
        ):
            st.write("-")
        else:
            st.write(medications_value)

    with col2:
        st.markdown("**Hemoglobin Level:**")
        st.write(f"{patient_data['hemoglobin']} g/dL")

        st.markdown("**Glucose Level:**")
        st.write(f"{patient_data['glucose']} mg/dL")

    st.markdown("---")

    # Superwise Integration Section
    st.markdown("### 🤖 Superwise AI Assistant")

    # Create columns for Ask Superwise button and response
    col1, col2 = st.columns([1, 3])

    with col1:
        if st.button("Ask Superwise", key="ask_superwise_btn", type="primary"):
            # Show loading state
            with st.spinner("Analyzing patient data with Superwise AI..."):
                # Call the Superwise API
                api_result = call_superwise_api(patient_data)

                if api_result["success"]:
                    # Format the API response for display
                    api_data = api_result["data"]

                    # Handle the specific Superwise API response format
                    if isinstance(api_data, dict) and "output" in api_data:
                        # Extract the output text from the API response
                        response_text = api_data["output"]
                    else:
                        # Fallback: convert to string if unexpected format
                        response_text = str(api_data)

                    # Check for guardrail violation
                    guardrail_keywords = [
                        "guardrail violation",
                        "message has been blocked",
                        "blocked due to a guardrail",
                        "rephrase your message"
                    ]
                    
                    is_guardrail_violation = any(
                        keyword.lower() in response_text.lower() 
                        for keyword in guardrail_keywords
                    )
                    
                    if is_guardrail_violation:
                        # Format guardrail violation with highlighting
                        st.session_state.superwise_response = f"""
                        <div style="background-color: #ffebee; border-left: 4px solid #f44336; padding: 15px; margin: 10px 0; border-radius: 4px;">
                            <h4 style="color: #d32f2f; margin: 0 0 10px 0;">⚠️ Guardrail Violation Detected</h4>
                            <p style="color: #c62828; margin: 0; font-weight: 500;">{response_text}</p>
                        </div>
                        """
                    else:
                        st.session_state.superwise_response = response_text
                else:
                    # Show error message
                    st.session_state.superwise_response = f"""
                    **Error: {api_result['error']}**
                    
                    {api_result['message']}
                    
                    Please try again or contact support if the problem persists.
                    """
    with col2:
        if "superwise_response" in st.session_state:
            st.markdown("**Superwise Response:**")
            # Enhanced display using Streamlit components
            st.subheader("🤖 AI Analysis Summary")

            # Create a container for the analysis
            with st.container():
                st.markdown("---")

                # Display the main response content
                st.markdown(st.session_state.superwise_response, unsafe_allow_html=True)

                st.markdown("---")
        else:
            st.info(
                "Click 'Ask Superwise' to get AI-powered insights about this patient."
            )

    # Close the container div
    st.markdown("</div>", unsafe_allow_html=True)

    # Log the component rendering
    logger.info(
        f"Patient details component rendered for patient: {patient_data['patient_id']}"
    )


def show_patient_details_page():
    """
    Wrapper function to show the patient details page with proper layout.
    This can be called from main.py when navigating to patient details.
    """

    # Clear Superwise response from session state
    if "superwise_response" in st.session_state:
        del st.session_state.superwise_response
        logger.info("🧹 Cleared Superwise response for fresh patient analysis")

    # Create header with title and back button inline
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Patient Details")
    with col2:
        st.markdown(
            "<br>", unsafe_allow_html=True
        )  # Add some spacing to align with title
        if st.button("← Back to Patients", key="back_to_patients"):
            st.session_state.current_page = "patients"
            # Clear Superwise response from session state
            if "superwise_response" in st.session_state:
                del st.session_state.superwise_response
                logger.info("🧹 Cleared Superwise response for fresh patient analysis")
            st.rerun()

    st.markdown("---")

    create_patient_details()
