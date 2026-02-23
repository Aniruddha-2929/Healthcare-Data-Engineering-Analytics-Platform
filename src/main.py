import sys
import os
import io

# Fix Windows console encoding for emoji support
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.etl_ingest import load_csv_to_mysql
from src.data_validation import validate_patients, validate_doctors, validate_visits, validate_lab_reports
from src.pyspark_transform import run_spark_transform


def run_pipeline():
    """
    Main ETL Pipeline Runner
    ========================
    1. Validates and loads raw CSV data into MySQL (OLTP)
    2. Runs PySpark transformations for analytics
    3. Exports processed data for Power BI consumption
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

    print("=" * 60)
    print("[HEALTHCARE] Healthcare Data Platform - ETL Pipeline")
    print("=" * 60)

    # Step 1: Load data into MySQL
    print("\n[STEP 1] Loading Raw Data into MySQL...")
    print("-" * 40)

    try:
        print("  Loading Patients...")
        load_csv_to_mysql(os.path.join(RAW_DIR, "patients.csv"), "patients", validate_patients)

        print("  Loading Doctors...")
        load_csv_to_mysql(os.path.join(RAW_DIR, "doctors.csv"), "doctors", validate_doctors)

        print("  Loading Visits...")
        load_csv_to_mysql(os.path.join(RAW_DIR, "visits.csv"), "visits", validate_visits)

        print("  Loading Lab Reports...")
        load_csv_to_mysql(os.path.join(RAW_DIR, "lab_reports.csv"), "lab_reports", validate_lab_reports)

        print("  [OK] MySQL ingestion completed!")
    except Exception as e:
        print(f"  [WARN] MySQL ingestion skipped: {e}")
        print("  [INFO] Update DB_PASSWORD in src/config.py or .env file")
        print("  [INFO] Continuing with PySpark transformations...")

    # Step 2: Run PySpark Transformations
    print("\n[STEP 2] Running PySpark Transformations...")
    print("-" * 40)
    run_spark_transform()

    # Done
    print("\n" + "=" * 60)
    print("[SUCCESS] Pipeline Completed Successfully!")
    print("=" * 60)
    print("\n[NEXT STEPS]:")
    print("  1. Connect Power BI to data/processed/ CSVs")
    print("  2. Or connect Power BI directly to MySQL healthcare_db")
    print("  3. Deploy to AWS using aws_deployment.md guide")


if __name__ == "__main__":
    run_pipeline()
