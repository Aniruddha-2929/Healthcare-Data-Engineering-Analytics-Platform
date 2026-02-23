from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, countDistinct
import os

# Set HADOOP_HOME for Windows (winutils.exe)
_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_HADOOP_HOME = os.path.join(_BASE, "hadoop")
os.environ["HADOOP_HOME"] = _HADOOP_HOME
os.environ["PATH"] = os.path.join(_HADOOP_HOME, "bin") + ";" + os.environ.get("PATH", "")


def run_spark_transform():
    """
    PySpark transformation layer:
    - Reads raw CSVs
    - Performs aggregations and feature engineering
    - Writes processed data for analytics / Power BI
    """
    spark = SparkSession.builder \
        .appName("Healthcare Analytics") \
        .master("local[*]") \
        .getOrCreate()

    # Set log level to reduce noise
    spark.sparkContext.setLogLevel("WARN")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
    PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

    # Ensure processed directory exists
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    # ---- Read Raw Data ----
    patients_df = spark.read.csv(os.path.join(RAW_DIR, "patients.csv"), header=True, inferSchema=True)
    doctors_df = spark.read.csv(os.path.join(RAW_DIR, "doctors.csv"), header=True, inferSchema=True)
    visits_df = spark.read.csv(os.path.join(RAW_DIR, "visits.csv"), header=True, inferSchema=True)
    lab_reports_df = spark.read.csv(os.path.join(RAW_DIR, "lab_reports.csv"), header=True, inferSchema=True)

    # ---- Transform 1: Doctor Visit Summary ----
    doctor_summary = visits_df.groupBy("doctor_id") \
        .agg(
            count("visit_id").alias("total_visits"),
            countDistinct("patient_id").alias("unique_patients")
        )
    doctor_summary = doctor_summary.join(doctors_df, on="doctor_id", how="left")
    doctor_summary.coalesce(1).write.csv(
        os.path.join(PROCESSED_DIR, "doctor_summary"), header=True, mode="overwrite"
    )
    print("  [OK] Doctor Summary written to data/processed/doctor_summary/")

    # ---- Transform 2: City-wise Patient Distribution ----
    city_distribution = patients_df.groupBy("city") \
        .agg(count("patient_id").alias("patient_count"))
    city_distribution.coalesce(1).write.csv(
        os.path.join(PROCESSED_DIR, "city_distribution"), header=True, mode="overwrite"
    )
    print("  [OK] City Distribution written to data/processed/city_distribution/")

    # ---- Transform 3: Visit Reason Analysis ----
    visit_reason_analysis = visits_df.groupBy("reason") \
        .agg(
            count("visit_id").alias("total_visits"),
            countDistinct("patient_id").alias("unique_patients")
        )
    visit_reason_analysis.coalesce(1).write.csv(
        os.path.join(PROCESSED_DIR, "visit_reason_analysis"), header=True, mode="overwrite"
    )
    print("  [OK] Visit Reason Analysis written to data/processed/visit_reason_analysis/")

    # ---- Transform 4: Lab Test Result Distribution ----
    lab_result_dist = lab_reports_df.groupBy("test_type", "result") \
        .agg(count("report_id").alias("report_count"))
    lab_result_dist.coalesce(1).write.csv(
        os.path.join(PROCESSED_DIR, "lab_result_distribution"), header=True, mode="overwrite"
    )
    print("  [OK] Lab Result Distribution written to data/processed/lab_result_distribution/")

    # ---- Transform 5: Hospital-wise Visit Summary ----
    hospital_visits = visits_df.join(doctors_df, on="doctor_id", how="left") \
        .groupBy("hospital") \
        .agg(
            count("visit_id").alias("total_visits"),
            countDistinct("patient_id").alias("unique_patients"),
            countDistinct("doctor_id").alias("active_doctors")
        )
    hospital_visits.coalesce(1).write.csv(
        os.path.join(PROCESSED_DIR, "hospital_visits"), header=True, mode="overwrite"
    )
    print("  [OK] Hospital Visit Summary written to data/processed/hospital_visits/")

    # ---- Power BI Ready Exports ----
    patients_df.coalesce(1).write.csv(
        os.path.join(PROCESSED_DIR, "patients_powerbi"), header=True, mode="overwrite"
    )
    doctors_df.coalesce(1).write.csv(
        os.path.join(PROCESSED_DIR, "doctors_powerbi"), header=True, mode="overwrite"
    )
    visits_df.coalesce(1).write.csv(
        os.path.join(PROCESSED_DIR, "visits_powerbi"), header=True, mode="overwrite"
    )
    lab_reports_df.coalesce(1).write.csv(
        os.path.join(PROCESSED_DIR, "lab_reports_powerbi"), header=True, mode="overwrite"
    )
    print("  [OK] Power BI ready exports written to data/processed/")

    spark.stop()


if __name__ == "__main__":
    run_spark_transform()
