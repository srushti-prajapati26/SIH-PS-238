"""
SIH PS 26239: Digital Sanction & DBT Payment Processing Service
Handles cryptographic sanction order generation and PFMS/NPCI APBS disbursement
"""
import hashlib
import random
from datetime import datetime
from app.models import (
    ApplicationRecord, ApplicationStatus, DigitalSanctionOrder
)
from app.database import db
from app.config import SCHEMES_CONFIG

class DBTPaymentService:
    @staticmethod
    def issue_digital_sanction(app_id: str) -> DigitalSanctionOrder:
        """Generates a tamper-evident digital sanction order with QR code data"""
        if app_id not in db.applications:
            raise ValueError(f"Application {app_id} not found.")

        app = db.applications[app_id]
        student = db.students.get(app.student_id)
        if not student:
            raise ValueError(f"Student profile for {app.student_id} not found.")

        sanction_id = f"SANCTION-MOTA-2026-{random.randint(10000, 99999)}"
        scheme_info = SCHEMES_CONFIG.get(app.scheme_id, {})
        scheme_name = scheme_info.get("name", app.scheme_id)

        # Generate digital signature hash
        signature_raw = f"{sanction_id}|{app.student_id}|{app.approved_amount}|2026-2027|GOV_MOTA_KEY"
        sig_hash = hashlib.sha256(signature_raw.encode()).hexdigest()

        order = DigitalSanctionOrder(
            sanction_order_id=sanction_id,
            application_id=app.application_id,
            student_id=student.student_id,
            student_name=student.full_name,
            scheme_name=scheme_name,
            institution_name=app.institution_name,
            sanctioned_amount=app.approved_amount,
            academic_year="2026-2027",
            digital_signature_hash=sig_hash,
            qr_code_data=f"https://mota.gov.in/verify-sanction?id={sanction_id}&amt={app.approved_amount}&hash={sig_hash[:12]}",
            sanction_date=datetime.utcnow().strftime("%Y-%m-%d")
        )

        # Update application state
        app.sanction_order_id = sanction_id
        app.sanction_date = order.sanction_date
        app.status = ApplicationStatus.SANCTIONED
        app.last_updated = datetime.utcnow()

        db.sanctions[sanction_id] = order
        return order

    @staticmethod
    def execute_pfms_dbt_disbursement(app_id: str) -> ApplicationRecord:
        """Pushes payment order through PFMS and NPCI APBS directly to student bank account"""
        if app_id not in db.applications:
            raise ValueError(f"Application {app_id} not found.")

        app = db.applications[app_id]
        if not app.sanction_order_id:
            raise ValueError("Application must have a valid Digital Sanction Order before DBT disbursement.")

        # Simulate PFMS batch routing and NPCI Aadhaar Bridge settlement
        txn_id = f"PFMS-2026-TXN-{random.randint(100000, 999999)}"
        utr_num = f"SBIN{datetime.utcnow().strftime('%y%m%d')}{random.randint(100000, 999999)}"

        app.pfms_transaction_id = txn_id
        app.utr_number = utr_num
        app.payment_status = "DISBURSED"
        app.status = ApplicationStatus.DISBURSED
        app.disbursement_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        app.last_updated = datetime.utcnow()

        return app
