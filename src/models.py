from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'

    patient_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    gender = Column(String)
    dob = Column(Date)
    blood_group = Column(String)
    city = Column(String)

    visits = relationship("Visit", back_populates="patient")

class Doctor(Base):
    __tablename__ = 'doctors'

    doctor_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    specialization = Column(String)
    hospital = Column(String)

    visits = relationship("Visit", back_populates="doctor")

class Visit(Base):
    __tablename__ = 'visits'

    visit_id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey('patients.patient_id'))
    doctor_id = Column(String, ForeignKey('doctors.doctor_id'))
    visit_date = Column(Date)
    reason = Column(Text)
    visit_type = Column(String)

    patient = relationship("Patient", back_populates="visits")
    doctor = relationship("Doctor", back_populates="visits")
    reports = relationship("LabReport", back_populates="visit")

class LabReport(Base):
    __tablename__ = 'lab_reports'

    report_id = Column(String, primary_key=True)
    visit_id = Column(String, ForeignKey('visits.visit_id'))
    test_type = Column(String)
    result = Column(String)
    report_date = Column(Date)

    visit = relationship("Visit", back_populates="reports")
