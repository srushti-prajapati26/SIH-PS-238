"""
SIH PS 26239: Federated Digital Integration Service
Simulates UIDAI Aadhaar e-KYC, DigiLocker, APAAR, UDISE+ and PFMS/NPCI
"""
import hashlib
import random
from typing import Dict, Any
from app.models import StudentProfile, BankAccountInfo, OTRRegistrationRequest

class FederatedIntegrationService:
    @staticmethod
    def verify_aadhaar_ekyc(aadhaar_number: str) -> Dict[str, Any]:
        """UIDAI e-KYC demographic verification simulation"""
        clean_aadhaar = aadhaar_number.replace("-", "").strip()
        if len(clean_aadhaar) != 12 or not clean_aadhaar.isdigit():
            return {"verified": False, "error": "Invalid 12-digit Aadhaar number format."}
        
        masked = f"XXXX-XXXX-{clean_aadhaar[-4:]}"
        return {
            "verified": True,
            "masked_aadhaar": masked,
            "ekyc_ref": f"UIDAI-EKYC-{random.randint(100000, 999999)}",
            "biometric_auth_status": "AUTHENTICATED",
            "timestamp": "2026-09-29T10:00:00Z"
        }

    @staticmethod
    def fetch_digilocker_credentials(aadhaar_masked: str) -> Dict[str, Any]:
        """Pulls verified caste and domicile documents from state repository"""
        return {
            "caste_certificate": {
                "issuer": "Revenue Dept, Sub-Divisional Officer",
                "category": "Scheduled Tribe (ST)",
                "cert_number": f"JH/SDO/ST/2024/{random.randint(10000, 99999)}",
                "authenticity_hash": hashlib.sha256(b"digilocker_caste_valid").hexdigest()[:16],
                "verified": True
            },
            "domicile_certificate": {
                "issuer": "State Govt Resident Portal",
                "verified": True
            }
        }

    @staticmethod
    def validate_pfms_npci_account(account_no: str, ifsc: str) -> Dict[str, Any]:
        """Validates Aadhaar Payment Bridge System (APBS) mandate"""
        return {
            "account_valid": True,
            "aadhaar_seeded": True,
            "npci_mapper_status": "ACTIVE_MAPPED",
            "bank_name": "Verified Scheduled Commercial Bank",
            "dbt_ready": True
        }

    @classmethod
    def register_otr_student(cls, req: OTRRegistrationRequest) -> StudentProfile:
        """Executes full OTR workflow and generates a Golden Profile"""
        kyc = cls.verify_aadhaar_ekyc(req.aadhaar_number)
        if not kyc["verified"]:
            raise ValueError(kyc["error"])
        
        # Generate Unique Student ID (USI)
        student_id = f"MOTA-2026-ST-{random.randint(100000, 999999)}"
        apaar_id = f"APAAR-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        
        profile = StudentProfile(
            student_id=student_id,
            full_name=req.full_name,
            father_name=f"Shri {req.full_name.split()[-1]} Senior",
            dob="2002-05-10",
            gender="Applicant",
            aadhaar_masked=kyc["masked_aadhaar"],
            is_aadhaar_verified=True,
            caste_category="ST",
            is_pvtg=req.is_pvtg,
            pvtg_community_name=req.pvtg_community,
            state_of_domicile=req.state_of_domicile,
            district=req.district,
            family_annual_income=req.annual_income,
            apaar_abc_id=apaar_id,
            bank_account=BankAccountInfo(
                account_number_masked=f"XXXXXX{req.bank_account_number[-4:] if len(req.bank_account_number) >= 4 else '1234'}",
                ifsc_code=req.ifsc_code,
                bank_name=req.bank_name,
                is_aadhaar_seeded=True,
                npci_status="ACTIVE"
            )
        )
        return profile
