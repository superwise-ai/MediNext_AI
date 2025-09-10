"""
Data Generator Utility for EHR Demo Portal

This module provides functions to generate sample data for demonstration purposes.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_patient_data(num_patients=50):
    """
    Generate sample patient data.

    Args:
        num_patients (int): Number of patients to generate

    Returns:
        pd.DataFrame: DataFrame containing patient information
    """

    # Sample names for variety
    first_names = [
        "James",
        "Mary",
        "John",
        "Patricia",
        "Robert",
        "Jennifer",
        "Michael",
        "Linda",
        "William",
        "Elizabeth",
        "David",
        "Barbara",
        "Richard",
        "Susan",
        "Joseph",
        "Jessica",
        "Thomas",
        "Sarah",
        "Christopher",
        "Karen",
        "Charles",
        "Nancy",
        "Daniel",
        "Lisa",
        "Matthew",
        "Betty",
        "Anthony",
        "Helen",
        "Mark",
        "Sandra",
        "Donald",
        "Donna",
        "Steven",
        "Carol",
        "Paul",
        "Ruth",
        "Andrew",
        "Sharon",
        "Joshua",
        "Michelle",
        "Kenneth",
        "Laura",
        "Kevin",
        "Emily",
        "Brian",
        "Kimberly",
        "George",
        "Deborah",
    ]

    last_names = [
        "Smith",
        "Johnson",
        "Williams",
        "Brown",
        "Jones",
        "Garcia",
        "Miller",
        "Davis",
        "Rodriguez",
        "Martinez",
        "Hernandez",
        "Lopez",
        "Gonzalez",
        "Wilson",
        "Anderson",
        "Thomas",
        "Taylor",
        "Moore",
        "Jackson",
        "Martin",
        "Lee",
        "Perez",
        "Thompson",
        "White",
        "Harris",
        "Sanchez",
        "Clark",
        "Ramirez",
        "Lewis",
        "Robinson",
        "Walker",
        "Young",
        "Allen",
        "King",
        "Wright",
        "Scott",
        "Torres",
        "Nguyen",
        "Hill",
        "Flores",
        "Green",
        "Adams",
        "Nelson",
        "Baker",
        "Hall",
        "Rivera",
        "Campbell",
        "Mitchell",
    ]

    # Generate patient data
    patients = []

    for i in range(num_patients):
        patient_id = f"P{str(i+1).zfill(3)}"
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        name = f"{first_name} {last_name}"
        age = random.randint(18, 85)

        # Generate last visit date (within last 6 months)
        days_ago = random.randint(1, 180)
        last_visit = datetime.now() - timedelta(days=days_ago)

        # Determine status based on last visit
        if days_ago <= 30:
            status = "Active"
        elif days_ago <= 90:
            status = "Follow-up"
        else:
            status = "Inactive"

        patients.append(
            {
                "Patient ID": patient_id,
                "Name": name,
                "Age": age,
                "Last Visit": last_visit.strftime("%Y-%m-%d"),
                "Status": status,
            }
        )

    return pd.DataFrame(patients)


def generate_appointment_data(num_appointments=30):
    """
    Generate sample appointment data.

    Args:
        num_appointments (int): Number of appointments to generate

    Returns:
        pd.DataFrame: DataFrame containing appointment information
    """

    appointment_types = [
        "Consultation",
        "Follow-up",
        "New Patient",
        "Emergency",
        "Routine Check",
    ]
    statuses = ["Confirmed", "Pending", "Cancelled", "Completed"]

    appointments = []

    for i in range(num_appointments):
        # Generate appointment date (within next 30 days)
        days_ahead = random.randint(0, 30)
        appointment_date = datetime.now() + timedelta(days=days_ahead)

        # Generate time (business hours: 8 AM to 6 PM)
        hour = random.randint(8, 17)
        minute = random.choice([0, 15, 30, 45])
        appointment_time = appointment_date.replace(hour=hour, minute=minute)

        appointment_type = random.choice(appointment_types)
        status = random.choice(statuses)

        # Generate patient name
        patient_name = f"Patient {random.randint(1, 50)}"

        appointments.append(
            {
                "Date": appointment_date.strftime("%Y-%m-%d"),
                "Time": appointment_time.strftime("%I:%M %p"),
                "Patient": patient_name,
                "Type": appointment_type,
                "Status": status,
            }
        )

    return pd.DataFrame(appointments)


def generate_prescription_data(num_prescriptions=40):
    """
    Generate sample prescription data.

    Args:
        num_prescriptions (int): Number of prescriptions to generate

    Returns:
        pd.DataFrame: DataFrame containing prescription information
    """

    medications = [
        "Lisinopril",
        "Metformin",
        "Atorvastatin",
        "Omeprazole",
        "Amlodipine",
        "Losartan",
        "Simvastatin",
        "Metoprolol",
        "Hydrochlorothiazide",
        "Sertraline",
        "Albuterol",
        "Ibuprofen",
        "Acetaminophen",
        "Aspirin",
        "Warfarin",
    ]

    dosages = [
        "10mg daily",
        "20mg daily",
        "40mg daily",
        "500mg twice daily",
        "1000mg daily",
        "25mg daily",
        "50mg daily",
        "75mg daily",
        "100mg daily",
        "5mg daily",
    ]

    frequencies = [
        "Once daily",
        "Twice daily",
        "Three times daily",
        "As needed",
        "Every 8 hours",
        "Every 12 hours",
        "Weekly",
        "Monthly",
    ]

    prescriptions = []

    for i in range(num_prescriptions):
        medication = random.choice(medications)
        dosage = random.choice(dosages)
        frequency = random.choice(frequencies)

        # Generate prescription date (within last 3 months)
        days_ago = random.randint(1, 90)
        prescription_date = datetime.now() - timedelta(days=days_ago)

        # Determine status based on prescription date
        if days_ago <= 30:
            status = "Active"
        elif days_ago <= 60:
            status = "Refill Needed"
        else:
            status = "Expired"

        # Generate patient name
        patient_name = f"Patient {random.randint(1, 50)}"

        prescriptions.append(
            {
                "Patient": patient_name,
                "Medication": medication,
                "Dosage": dosage,
                "Frequency": frequency,
                "Prescribed Date": prescription_date.strftime("%Y-%m-%d"),
                "Status": status,
            }
        )

    return pd.DataFrame(prescriptions)


def generate_activity_data(num_activities=25):
    """
    Generate sample activity data.

    Args:
        num_activities (int): Number of activities to generate

    Returns:
        list: List of activity dictionaries
    """

    activity_types = [
        "lab_result",
        "appointment",
        "prescription",
        "alert",
        "questionnaire",
        "check_in",
        "check_out",
        "test_result",
        "referral",
        "note",
    ]

    activities = []

    for i in range(num_activities):
        # Generate time (within last 24 hours)
        hours_ago = random.randint(0, 24)
        minutes_ago = random.randint(0, 59)
        time_ago = (
            f"{hours_ago}h {minutes_ago}m ago"
            if hours_ago > 0
            else f"{minutes_ago}m ago"
        )

        activity_type = random.choice(activity_types)

        # Generate activity description based on type
        if activity_type == "lab_result":
            activity = (
                f"New lab result uploaded for Patient P{random.randint(1, 50):03d}"
            )
        elif activity_type == "appointment":
            activity = (
                f"Appointment scheduled for tomorrow at {random.randint(8, 17)}:00"
            )
        elif activity_type == "prescription":
            activity = f"Prescription renewed for Patient P{random.randint(1, 50):03d}"
        elif activity_type == "alert":
            activity = f"Critical alert: Patient P{random.randint(1, 50):03d} requires attention"
        elif activity_type == "questionnaire":
            activity = f"Patient P{random.randint(1, 50):03d} completed follow-up questionnaire"
        else:
            activity = f"Activity {i+1} completed"

        # Determine priority
        if "Critical" in activity or "alert" in activity_type:
            priority = "critical"
        else:
            priority = "normal"

        activities.append(
            {
                "time": time_ago,
                "activity": activity,
                "type": activity_type,
                "priority": priority,
            }
        )

    return activities


def generate_analytics_data():
    """
    Generate sample analytics data for charts.

    Returns:
        dict: Dictionary containing various analytics datasets
    """

    # Generate patient visits data for the last 30 days
    dates = pd.date_range(start="2024-01-01", end="2024-01-31", freq="D")
    np.random.seed(42)

    # Base visits with some randomness
    base_visits = 15
    patient_visits = np.random.poisson(base_visits, len(dates)) + np.random.normal(
        0, 2, len(dates)
    )
    patient_visits = np.maximum(patient_visits, 0).astype(int)

    visits_df = pd.DataFrame({"Date": dates, "Patient Visits": patient_visits})

    # Department data
    departments = [
        "Cardiology",
        "Neurology",
        "Orthopedics",
        "Pediatrics",
        "Emergency",
        "General",
    ]
    department_counts = [45, 32, 28, 38, 52, 41]

    dept_df = pd.DataFrame(
        {"Department": departments, "Patient Count": department_counts}
    )

    # Weekly pattern
    weekly_visits = visits_df.groupby(visits_df["Date"].dt.dayofweek)[
        "Patient Visits"
    ].mean()
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    weekly_df = pd.DataFrame({"Day": days, "Average Visits": weekly_visits.values})

    # Efficiency data
    efficiency_data = {
        "Department": departments,
        "Efficiency Score": [85, 92, 78, 88, 95, 82],
        "Avg Wait Time (min)": [15, 8, 22, 12, 5, 18],
    }

    efficiency_df = pd.DataFrame(efficiency_data)

    return {
        "visits": visits_df,
        "departments": dept_df,
        "weekly": weekly_df,
        "efficiency": efficiency_df,
    }
