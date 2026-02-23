# 🏥 Healthcare Data Platform – Centralized Patient Record System

## 📋 Project Overview

An industry-level **Healthcare Data Platform** that integrates Python, MySQL, PySpark, and Power BI 
to build a centralized patient record system with ETL pipelines and analytics dashboards.

---

## 🏗 Architecture Flow

```
Raw CSV Data
     ↓
Python Validation Layer
     ↓
MySQL (OLTP Database)
     ↓
PySpark ETL (Transform + Feature Engineering)
     ↓
Processed Data (Analytics Layer)
     ↓
Power BI Dashboard
     ↓
Deploy to AWS (S3 + EC2)
```

---

## 📂 Project Structure

```
healthcare-data-platform/
│
├── data/
│   ├── raw/                        ← Raw CSV files (patients, doctors, visits, lab_reports)
│   └── processed/                  ← PySpark transformed output for analytics
│
├── sql/
│   ├── db.sql                      ← Database creation script
│   ├── schema.sql                  ← Table schemas with foreign keys
│   └── procedures.sql              ← Stored procedures (Industry Feature)
│
├── src/
│   ├── __init__.py
│   ├── config.py                   ← DB configuration with dotenv support
│   ├── db_connection.py            ← MySQL connection manager
│   ├── data_validation.py          ← Data validation layer
│   ├── etl_ingest.py               ← CSV → MySQL ingestion with validation
│   ├── etl_pipeline.py             ← Utility loader (no validation)
│   ├── pyspark_transform.py        ← PySpark transformation & analytics
│   ├── models.py                   ← SQLAlchemy ORM models
│   └── main.py                     ← Pipeline runner (Entry Point)
│
├── notebooks/
│   └── analysis.ipynb              ← Jupyter analysis notebook
│
├── requirements.txt                ← Python dependencies
├── README.md                       ← This file
└── aws_deployment.md               ← AWS deployment guide
```

---

## 🗃 Data Tables

| Table | Description | Records |
|-------|-------------|---------|
| `patients` | Patient demographics (ID, name, gender, DOB, blood_group, city) | ~10,000 |
| `doctors` | Doctor details (ID, name, specialization, hospital) | ~1,000 |
| `visits` | Visit records (ID, patient, doctor, date, reason, type) | ~50,000 |
| `lab_reports` | Lab test reports (ID, visit, test_type, result, date) | ~30,000 |

---

## 🚀 Setup & Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure MySQL
Update `src/config.py` or create a `.env` file:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=healthcare_db
```

### 3. Setup Database
Run the SQL scripts in MySQL:
```sql
source sql/db.sql;
source sql/schema.sql;
source sql/procedures.sql;
```

### 4. Run the ETL Pipeline
```bash
python -m src.main
```

This will:
1. ✅ Validate and load CSV data into MySQL
2. ✅ Run PySpark transformations
3. ✅ Export processed data for Power BI

---

## ⚡ PySpark Analytics Output

| Analytics | File | Description |
|-----------|------|-------------|
| Doctor Summary | `data/processed/doctor_summary/` | Visits & unique patients per doctor |
| City Distribution | `data/processed/city_distribution/` | Patient count per city |
| Visit Reasons | `data/processed/visit_reason_analysis/` | Visit breakdown by reason |
| Lab Results | `data/processed/lab_result_distribution/` | Test type vs result distribution |
| Hospital Visits | `data/processed/hospital_visits/` | Visit summary per hospital |

---

## 📊 Power BI Dashboard

Connect Power BI to:
- **MySQL directly**: Use MySQL connector with `healthcare_db`
- **Processed CSVs**: Load from `data/processed/` folder

### Suggested Dashboard Pages:
1. **Patient Overview** – Demographics, city distribution, blood group analysis
2. **Visit Analytics** – Visit trends, reason analysis, visit types
3. **Doctor Performance** – Visits per doctor, specialization breakdown
4. **Lab Reports** – Test results distribution, abnormal result tracking
5. **Hospital Summary** – Hospital-wise performance comparison

---

## 🔧 Stored Procedures

| Procedure | Description |
|-----------|-------------|
| `GetPatientHistory(pid)` | Get complete visit history for a patient |
| `GetPatientLabReports(pid)` | Get all lab reports for a patient |
| `GetDoctorSummary(did)` | Get visit summary for a doctor |

**Usage:**
```sql
CALL GetPatientHistory('P100001');
CALL GetPatientLabReports('P100001');
CALL GetDoctorSummary('D2000');
```

---

## ☁️ AWS Deployment

See [aws_deployment.md](aws_deployment.md) for detailed deployment instructions.

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.x |
| OLTP Database | MySQL |
| Big Data Processing | PySpark |
| Visualization | Power BI |
| ORM | SQLAlchemy |
| Cloud | AWS (S3 + EC2) |

---

## 👨‍💻 Author

Built as part of CDAC Healthcare Data Platform project.
