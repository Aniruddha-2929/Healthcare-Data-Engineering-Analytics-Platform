USE healthcare_db;

-- Stored Procedure: Get Patient Visit History
DELIMITER //

CREATE PROCEDURE GetPatientHistory(IN pid VARCHAR(20))
BEGIN
    SELECT p.name, p.gender, p.dob, p.blood_group, p.city,
           v.visit_date, v.reason, v.visit_type,
           d.name AS doctor_name, d.specialization, d.hospital
    FROM patients p
    JOIN visits v ON p.patient_id = v.patient_id
    JOIN doctors d ON v.doctor_id = d.doctor_id
    WHERE p.patient_id = pid
    ORDER BY v.visit_date DESC;
END //

DELIMITER ;

-- Stored Procedure: Get Patient Lab Reports
DELIMITER //

CREATE PROCEDURE GetPatientLabReports(IN pid VARCHAR(20))
BEGIN
    SELECT p.name AS patient_name,
           v.visit_date, v.reason,
           lr.test_type, lr.result, lr.report_date
    FROM patients p
    JOIN visits v ON p.patient_id = v.patient_id
    JOIN lab_reports lr ON v.visit_id = lr.visit_id
    WHERE p.patient_id = pid
    ORDER BY lr.report_date DESC;
END //

DELIMITER ;

-- Stored Procedure: Get Doctor Visit Summary
DELIMITER //

CREATE PROCEDURE GetDoctorSummary(IN did VARCHAR(20))
BEGIN
    SELECT d.name AS doctor_name, d.specialization, d.hospital,
           COUNT(v.visit_id) AS total_visits,
           COUNT(DISTINCT v.patient_id) AS unique_patients
    FROM doctors d
    LEFT JOIN visits v ON d.doctor_id = v.doctor_id
    WHERE d.doctor_id = did
    GROUP BY d.doctor_id, d.name, d.specialization, d.hospital;
END //

DELIMITER ;
