"""
Generate dashboard_data.json from processed CSVs and MySQL for the frontend dashboard.
"""
import sys
import os
import json
import glob

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
OUTPUT_FILE = os.path.join(BASE_DIR, "dashboard", "dashboard_data.json")


def read_spark_csv(folder_name):
    """Read a Spark partitioned CSV output."""
    pattern = os.path.join(PROCESSED_DIR, folder_name, "part-*.csv")
    files = glob.glob(pattern)
    if files:
        return pd.read_csv(files[0])
    return pd.DataFrame()


def generate():
    print("Generating dashboard data...")

    # Raw data
    patients = pd.read_csv(os.path.join(RAW_DIR, "patients.csv"))
    doctors = pd.read_csv(os.path.join(RAW_DIR, "doctors.csv"))
    visits = pd.read_csv(os.path.join(RAW_DIR, "visits.csv"))
    lab_reports = pd.read_csv(os.path.join(RAW_DIR, "lab_reports.csv"))

    # Processed aggregations
    city_dist = read_spark_csv("city_distribution")
    doctor_summary = read_spark_csv("doctor_summary")
    hospital_visits = read_spark_csv("hospital_visits")
    lab_result_dist = read_spark_csv("lab_result_distribution")
    visit_reason = read_spark_csv("visit_reason_analysis")

    # Build dashboard data
    data = {
        "overview": {
            "total_patients": len(patients),
            "total_doctors": len(doctors),
            "total_visits": len(visits),
            "total_lab_reports": len(lab_reports),
            "total_cities": patients["city"].nunique(),
            "total_hospitals": doctors["hospital"].nunique(),
        },
        "gender_distribution": patients["gender"].value_counts().to_dict(),
        "blood_group_distribution": patients["blood_group"].value_counts().to_dict(),
        "top_cities": city_dist.sort_values("patient_count", ascending=False).head(15).to_dict(orient="records"),
        "all_cities": city_dist.sort_values("patient_count", ascending=False).to_dict(orient="records"),
        "specialization_distribution": doctors["specialization"].value_counts().to_dict(),
        "hospital_distribution": doctors["hospital"].value_counts().to_dict(),
        "visit_type_distribution": visits["visit_type"].value_counts().to_dict(),
        "visit_reason_analysis": visit_reason.sort_values("total_visits", ascending=False).to_dict(orient="records"),
        "doctor_summary": doctor_summary.sort_values("total_visits", ascending=False).head(20).to_dict(orient="records"),
        "hospital_visits": hospital_visits.sort_values("total_visits", ascending=False).to_dict(orient="records"),
        "lab_result_distribution": lab_result_dist.to_dict(orient="records"),
        "lab_test_types": lab_reports["test_type"].value_counts().to_dict(),
        "lab_results_overview": lab_reports["result"].value_counts().to_dict(),
        # Recent patients sample
        "recent_patients": patients.head(50).to_dict(orient="records"),
        # Monthly visit trends (from visit_date)
        "monthly_visits": visits.assign(
            month=pd.to_datetime(visits["visit_date"]).dt.to_period("M").astype(str)
        ).groupby("month").size().to_dict(),
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)

    print(f"  [OK] Dashboard data written to {OUTPUT_FILE}")
    print(f"  [OK] {len(data)} data sections generated")


if __name__ == "__main__":
    generate()
