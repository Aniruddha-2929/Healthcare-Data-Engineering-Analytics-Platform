"""
Generate patient-level records for Patient Portal and Doctor Lookup.
Creates patient_records.json with per-patient visits, doctors, and lab reports.
"""
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
OUTPUT_FILE = os.path.join(BASE_DIR, "dashboard", "patient_records.json")


def generate():
    print("Generating patient-level records...")

    patients = pd.read_csv(os.path.join(RAW_DIR, "patients.csv"))
    doctors = pd.read_csv(os.path.join(RAW_DIR, "doctors.csv"))
    visits = pd.read_csv(os.path.join(RAW_DIR, "visits.csv"))
    lab_reports = pd.read_csv(os.path.join(RAW_DIR, "lab_reports.csv"))

    # Build doctor lookup
    doctor_map = doctors.set_index("doctor_id").to_dict(orient="index")

    # Build visit -> lab reports mapping
    visit_labs = lab_reports.groupby("visit_id").apply(
        lambda x: x[["report_id", "test_type", "result", "report_date"]].to_dict(orient="records"),
        include_groups=False
    ).to_dict()

    # Build per-patient records
    records = {}

    for _, p in patients.iterrows():
        pid = p["patient_id"]
        patient_info = {
            "patient_id": pid,
            "name": p["name"],
            "gender": p["gender"],
            "dob": str(p["dob"]),
            "blood_group": p["blood_group"],
            "city": p["city"],
            "visits": [],
            "summary": {
                "total_visits": 0,
                "total_lab_reports": 0,
                "doctors_seen": set(),
                "hospitals_visited": set(),
                "visit_types": {},
                "reasons": {},
            }
        }

        # Get patient visits
        patient_visits = visits[visits["patient_id"] == pid].sort_values("visit_date", ascending=False)

        for _, v in patient_visits.iterrows():
            vid = v["visit_id"]
            did = v["doctor_id"]
            doc_info = doctor_map.get(did, {})

            visit_record = {
                "visit_id": vid,
                "visit_date": str(v["visit_date"]),
                "reason": v["reason"],
                "visit_type": v["visit_type"],
                "doctor": {
                    "doctor_id": did,
                    "name": doc_info.get("name", "Unknown"),
                    "specialization": doc_info.get("specialization", ""),
                    "hospital": doc_info.get("hospital", ""),
                },
                "lab_reports": visit_labs.get(vid, [])
            }

            patient_info["visits"].append(visit_record)

            # Update summary
            patient_info["summary"]["total_visits"] += 1
            patient_info["summary"]["total_lab_reports"] += len(visit_record["lab_reports"])
            patient_info["summary"]["doctors_seen"].add(doc_info.get("name", "Unknown"))
            patient_info["summary"]["hospitals_visited"].add(doc_info.get("hospital", ""))

            vt = v["visit_type"]
            patient_info["summary"]["visit_types"][vt] = patient_info["summary"]["visit_types"].get(vt, 0) + 1

            reason = v["reason"]
            patient_info["summary"]["reasons"][reason] = patient_info["summary"]["reasons"].get(reason, 0) + 1

        # Convert sets to lists for JSON
        patient_info["summary"]["doctors_seen"] = list(patient_info["summary"]["doctors_seen"])
        patient_info["summary"]["hospitals_visited"] = list(patient_info["summary"]["hospitals_visited"])

        records[pid] = patient_info

    # Also create a lightweight patient index for search
    patient_index = []
    for _, p in patients.iterrows():
        pid = p["patient_id"]
        rec = records[pid]
        patient_index.append({
            "patient_id": pid,
            "name": p["name"],
            "gender": p["gender"],
            "city": p["city"],
            "blood_group": p["blood_group"],
            "total_visits": rec["summary"]["total_visits"],
            "total_lab_reports": rec["summary"]["total_lab_reports"],
        })

    output = {
        "records": records,
        "patient_index": patient_index,
        "total_patients": len(records),
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, default=str)

    size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"  [OK] Patient records written to {OUTPUT_FILE}")
    print(f"  [OK] {len(records)} patient records ({size_mb:.1f} MB)")


if __name__ == "__main__":
    generate()
