"""
SIH PS 26239: Persistence & Memory Data Store
Maintains state for Student Profiles, Applications, Sanctions, Deficiencies & Analytics
Includes auto-seeding with realistic MoTA demo records
"""
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from app.models import (
    StudentProfile, BankAccountInfo, ApplicationRecord, 
    ApplicationStatus, DocumentRecord, OCRFieldExtraction,
    VerificationTier, DeficiencyRecord, DigitalSanctionOrder
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAPSHOT_FILE = os.path.join(BASE_DIR, "db_snapshot.json")

class DatabaseStore:
    def __init__(self):
        self.students: Dict[str, StudentProfile] = {}
        self.applications: Dict[str, ApplicationRecord] = {}
        self.sanctions: Dict[str, DigitalSanctionOrder] = {}
        
        # Load from disk if snapshot exists; otherwise initialize demo seed and persist
        if not self.load_from_json():
            self.seed_initial_data()
            self.save_to_json()

    def seed_initial_data(self):
        # Seed 1: Rahul Munda - NFST Ph.D. Candidate (Smooth verification)
        p1 = StudentProfile(
            student_id="MOTA-2026-ST-881024",
            full_name="Rahul Munda",
            father_name="Shri Sukra Munda",
            dob="2000-04-14",
            gender="Male",
            aadhaar_masked="XXXX-XXXX-9281",
            is_aadhaar_verified=True,
            caste_category="ST",
            is_pvtg=False,
            state_of_domicile="Jharkhand",
            district="Ranchi",
            family_annual_income=180000.0,
            apaar_abc_id="APAAR-9812-7419-0129",
            bank_account=BankAccountInfo(
                account_number_masked="XXXXXX4910",
                ifsc_code="SBIN0001234",
                bank_name="State Bank of India, Main Branch Ranchi",
                is_aadhaar_seeded=True,
                npci_status="ACTIVE"
            )
        )
        self.students[p1.student_id] = p1

        # Seed 2: Sunita Soren - Birhor Tribe (PVTG Candidate, Top Class IIT)
        p2 = StudentProfile(
            student_id="MOTA-2026-ST-330912",
            full_name="Sunita Soren",
            father_name="Shri Mangal Soren",
            dob="2003-08-19",
            gender="Female",
            aadhaar_masked="XXXX-XXXX-4019",
            is_aadhaar_verified=True,
            caste_category="ST",
            is_pvtg=True,
            pvtg_community_name="Birhor",
            state_of_domicile="Odisha",
            district="Mayurbhanj",
            family_annual_income=95000.0,
            apaar_abc_id="APAAR-4192-8821-4491",
            bank_account=BankAccountInfo(
                account_number_masked="XXXXXX7721",
                ifsc_code="UBIN0541299",
                bank_name="Union Bank of India, Baripada",
                is_aadhaar_seeded=True,
                npci_status="ACTIVE"
            )
        )
        self.students[p2.student_id] = p2

        # Seed 3: Birsa Tirkey - Post-Matric with Deficiency in progress
        p3 = StudentProfile(
            student_id="MOTA-2026-ST-512093",
            full_name="Birsa Tirkey",
            father_name="Shri Somra Tirkey",
            dob="2004-11-02",
            gender="Male",
            aadhaar_masked="XXXX-XXXX-1934",
            is_aadhaar_verified=True,
            caste_category="ST",
            is_pvtg=False,
            state_of_domicile="Chhattisgarh",
            district="Bastar",
            family_annual_income=140000.0,
            apaar_abc_id="APAAR-1092-3849-2910",
            bank_account=BankAccountInfo(
                account_number_masked="XXXXXX8123",
                ifsc_code="PUNB0192300",
                bank_name="Punjab National Bank, Jagdalpur",
                is_aadhaar_seeded=True,
                npci_status="ACTIVE"
            )
        )
        self.students[p3.student_id] = p3

        # Seed Applications
        # App 1: Rahul Munda - NFST Fellowship
        app1 = ApplicationRecord(
            application_id="APP-MOTA-NFST-001",
            student_id=p1.student_id,
            scheme_id="NFST",
            institution_name="Indian Institute of Technology (IIT) Kharagpur",
            course_name="Ph.D. in Tribal Heritage & Sustainable Agro-forestry",
            status=ApplicationStatus.DISBURSED,
            claimed_amount=372000.0,
            approved_amount=372000.0,
            tier1_ai_audit_score=0.98,
            tier1_ai_audit_passed=True,
            tier2_institute_verified=True,
            tier2_verifier_name="Prof. A. Mukherjee (Dean Academics)",
            tier3_mota_approved=True,
            tier3_approver_name="Dr. V. K. Sharma (MoTA Director)",
            merit_score=94.5,
            merit_rank=4,
            sanction_order_id="SANCTION-MOTA-2026-00481",
            sanction_date="2026-09-15",
            pfms_transaction_id="PFMS-2026-TXN-994821",
            utr_number="SBIN260915984102",
            payment_status="DISBURSED",
            disbursement_date="2026-09-18"
        )
        self.applications[app1.application_id] = app1

        # Seed Sanction for App 1
        sanc1 = DigitalSanctionOrder(
            sanction_order_id=app1.sanction_order_id,
            application_id=app1.application_id,
            student_id=p1.student_id,
            student_name=p1.full_name,
            scheme_name="National Fellowship for Higher Education of ST Students (NFST)",
            institution_name=app1.institution_name,
            sanctioned_amount=app1.approved_amount,
            academic_year="2026-2027",
            digital_signature_hash="e8f49b1a0d7f26c59b20e14a8e63b719482a17f69201948",
            qr_code_data=f"SANCTION:{app1.sanction_order_id}|AMT:372000|SCHEME:NFST|STUDENT:{p1.student_id}",
            sanction_date=app1.sanction_date
        )
        self.sanctions[sanc1.sanction_order_id] = sanc1

        # App 2: Sunita Soren - Top Class Education (IIT Bombay) - Verified Pool, Ready for Merit
        app2 = ApplicationRecord(
            application_id="APP-MOTA-TOPCLASS-002",
            student_id=p2.student_id,
            scheme_id="TOP_CLASS",
            institution_name="Indian Institute of Technology (IIT) Bombay",
            course_name="B.Tech Computer Science & Engineering",
            status=ApplicationStatus.VERIFIED_POOL,
            claimed_amount=245000.0,
            approved_amount=245000.0,
            tier1_ai_audit_score=0.99,
            tier1_ai_audit_passed=True,
            tier2_institute_verified=True,
            tier2_verifier_name="Dr. S. K. Roy (Nodal Officer, IITB)",
            tier3_mota_approved=True,
            tier3_approver_name="Smt. R. Murmu (State Nodal Officer Odisha)",
            merit_score=98.0,
            merit_rank=1
        )
        self.applications[app2.application_id] = app2

        # App 3: Birsa Tirkey - Post-Matric with Deficiency
        defic = DeficiencyRecord(
            deficiency_id="DEF-2026-092",
            tier_raised_by=VerificationTier.TIER_2_INSTITUTE,
            issue_description="Fee receipt timestamp is illegible; hostel superintendent certificate missing.",
            required_action="Please upload an official stamped copy of your hostel occupancy certificate and current semester fee receipt.",
            flagged_document="college_fee_receipt"
        )
        app3 = ApplicationRecord(
            application_id="APP-MOTA-POSTMATRIC-003",
            student_id=p3.student_id,
            scheme_id="POST_MATRIC",
            institution_name="Government Engineering College, Jagdalpur",
            course_name="B.Tech Civil Engineering (3rd Semester)",
            status=ApplicationStatus.DEFICIENCY_RAISED,
            claimed_amount=38500.0,
            tier1_ai_audit_score=0.91,
            tier1_ai_audit_passed=True,
            tier2_institute_verified=False,
            deficiencies=[defic]
        )
        self.applications[app3.application_id] = app3

    def save_to_json(self, filepath: Optional[str] = None) -> Dict[str, Any]:
        """Serializes all in-memory students, applications, and sanctions to JSON snapshot on disk"""
        target_path = filepath or SNAPSHOT_FILE
        payload = {
            "saved_at": datetime.utcnow().isoformat(),
            "students": {k: v.model_dump(mode="json") for k, v in self.students.items()},
            "applications": {k: v.model_dump(mode="json") for k, v in self.applications.items()},
            "sanctions": {k: v.model_dump(mode="json") for k, v in self.sanctions.items()}
        }
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        return {
            "status": "SUCCESS",
            "saved_at": payload["saved_at"],
            "filepath": target_path,
            "students_count": len(self.students),
            "applications_count": len(self.applications),
            "sanctions_count": len(self.sanctions)
        }

    def load_from_json(self, filepath: Optional[str] = None) -> bool:
        """Loads and restores database state from JSON snapshot on disk"""
        target_path = filepath or SNAPSHOT_FILE
        if not os.path.exists(target_path):
            return False
        try:
            with open(target_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.students = {
                k: StudentProfile.model_validate(v) 
                for k, v in data.get("students", {}).items()
            }
            self.applications = {
                k: ApplicationRecord.model_validate(v) 
                for k, v in data.get("applications", {}).items()
            }
            self.sanctions = {
                k: DigitalSanctionOrder.model_validate(v) 
                for k, v in data.get("sanctions", {}).items()
            }
            return True
        except Exception as e:
            print(f"Warning: Failed to load snapshot from {target_path}: {e}")
            return False

# Global database instance
db = DatabaseStore()
