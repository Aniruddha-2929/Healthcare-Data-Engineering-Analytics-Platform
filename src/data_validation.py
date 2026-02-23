import pandas as pd


def validate_patients(df):
    """Validate patient data - drop nulls, ensure valid fields."""
    df = df.dropna(subset=['patient_id', 'name'])
    df = df.drop_duplicates(subset=['patient_id'])
    # Ensure gender is valid
    df = df[df['gender'].isin(['M', 'F', 'Other'])]
    return df


def validate_doctors(df):
    """Validate doctor data - drop nulls, ensure valid fields."""
    df = df.dropna(subset=['doctor_id', 'name'])
    df = df.drop_duplicates(subset=['doctor_id'])
    return df


def validate_visits(df):
    """Validate visit data - drop nulls, ensure referential integrity."""
    df = df.dropna(subset=['visit_id', 'patient_id', 'doctor_id'])
    df = df.drop_duplicates(subset=['visit_id'])
    return df


def validate_lab_reports(df):
    """Validate lab report data - drop nulls."""
    df = df.dropna(subset=['report_id', 'visit_id'])
    df = df.drop_duplicates(subset=['report_id'])
    return df
