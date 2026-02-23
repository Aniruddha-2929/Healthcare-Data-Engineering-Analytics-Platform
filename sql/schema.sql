USE healthcare_db;

CREATE TABLE IF NOT EXISTS patients (
    patient_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    gender VARCHAR(10),
    dob DATE,
    blood_group VARCHAR(10),
    city VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS doctors (
    doctor_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    specialization VARCHAR(100),
    hospital VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS visits (
    visit_id VARCHAR(20) PRIMARY KEY,
    patient_id VARCHAR(20),
    doctor_id VARCHAR(20),
    visit_date DATE,
    reason VARCHAR(255),
    visit_type VARCHAR(50),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

CREATE TABLE IF NOT EXISTS lab_reports (
    report_id VARCHAR(20) PRIMARY KEY,
    visit_id VARCHAR(20),
    test_type VARCHAR(100),
    result VARCHAR(100),
    report_date DATE,
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id)
);
