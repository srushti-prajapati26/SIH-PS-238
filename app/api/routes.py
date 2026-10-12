"""
SIH PS 26239: REST API Router
Exposes clean endpoints for all stages of the scholarship management system
"""
from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Form
from typing import List, Optional, Dict, Any
import uuid

from app.models import (
    OTRRegistrationRequest, StudentProfile, SchemeApplicationRequest,
    ApplicationRecord, TierVerificationActionRequest, DeficiencyResolutionRequest,
    DigitalSanctionOrder, JAGOChatRequest, JAGOChatResponse, AnalyticsSummary,
    AISchemeRecommendationRequest, AISchemeRecommendationResponse
)
from app.config import SCHEMES_CONFIG, SUPPORTED_LANGUAGES
from app.database import db
from app.services.federated_service import FederatedIntegrationService
from app.services.ocr_service import AIOCRService
from app.services.rules_engine import BusinessRulesEngine
from app.services.verification_service import MultiTierVerificationService
from app.services.merit_service import MeritAndSelectionService
from app.services.dbt_service import DBTPaymentService
from app.services.jago_bot_service import JAGOChatbotService
from app.services.antifraud_service import AntiFraudSentryService
from app.services.analytics_service import AnalyticsService
from app.services.ai_scheme_service import AISchemeRecommender

router = APIRouter()

# --- Config & Schemes ---
@router.get("/schemes", response_model=Dict[str, Any])
def get_supported_schemes():
    return {
        "schemes": SCHEMES_CONFIG,
        "supported_languages": SUPPORTED_LANGUAGES
    }

# --- Stage 1: OTR & Student Profile ---
@router.post("/otr/register", response_model=StudentProfile)
def register_student_otr(req: OTRRegistrationRequest):
    try:
        profile = FederatedIntegrationService.register_otr_student(req)
        db.students[profile.student_id] = profile
        db.save_to_json()
        return profile
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/students/{student_id}", response_model=StudentProfile)
def get_student_profile(student_id: str):
    if student_id not in db.students:
        raise HTTPException(status_code=404, detail="Student not found.")
    return db.students[student_id]

# --- Stage 2: Smart Application & OCR Upload ---
@router.post("/applications/apply", response_model=ApplicationRecord)
def submit_scholarship_application(req: SchemeApplicationRequest):
    if req.student_id not in db.students:
        raise HTTPException(status_code=404, detail="Student profile not found. Please complete OTR first.")

    profile = db.students[req.student_id]

    # Evaluate Rules Engine
    is_eligible, reasons, approved_amount = BusinessRulesEngine.evaluate_scheme_eligibility(profile, req)
    if not is_eligible:
        raise HTTPException(status_code=400, detail={"message": "Ineligible based on Scheme Rules", "violations": reasons})

    # Create Application Record
    app_id = f"APP-MOTA-{req.scheme_id.upper()}-{uuid.uuid4().hex[:4].upper()}"
    app = ApplicationRecord(
        application_id=app_id,
        student_id=req.student_id,
        scheme_id=req.scheme_id,
        institution_name=req.institution_name,
        course_name=req.course_name,
        claimed_amount=approved_amount,
        approved_amount=approved_amount
    )

    # Automatically execute Tier 1 AI Audit
    MultiTierVerificationService.run_tier1_ai_audit(app)

    db.applications[app_id] = app
    db.save_to_json()
    return app

@router.post("/documents/ocr-scan")
async def ocr_scan_document(
    doc_type: str = Form(...),
    student_name: str = Form(...),
    file: UploadFile = File(...)
):
    content = await file.read()
    result = AIOCRService.process_uploaded_document(
        doc_type=doc_type,
        file_name=file.filename,
        file_bytes=content,
        student_expected_name=student_name
    )
    return result

@router.get("/applications", response_model=List[ApplicationRecord])
def list_applications(scheme_id: Optional[str] = None):
    apps = list(db.applications.values())
    if scheme_id:
        apps = [a for a in apps if a.scheme_id == scheme_id.upper()]
    return apps

@router.get("/applications/{app_id}", response_model=ApplicationRecord)
def get_application(app_id: str):
    if app_id not in db.applications:
        raise HTTPException(status_code=404, detail="Application not found.")
    return db.applications[app_id]

# --- Stage 3: Verification & Deficiency Loop ---
@router.post("/verification/{app_id}/tier-action", response_model=ApplicationRecord)
@router.post("/verification/{app_id}/action", response_model=ApplicationRecord)
def take_tier_verification_action(app_id: str, action_req: TierVerificationActionRequest):
    try:
        updated = MultiTierVerificationService.process_tier_action(app_id, action_req)
        db.save_to_json()
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/deficiency/{app_id}/resolve", response_model=ApplicationRecord)
def resolve_student_deficiency(app_id: str, req: DeficiencyResolutionRequest):
    try:
        updated = MultiTierVerificationService.resolve_deficiency(app_id, req.deficiency_id, req.student_comment)
        db.save_to_json()
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Stage 4: Merit & Sanction ---
@router.post("/merit/{scheme_id}/rank", response_model=List[ApplicationRecord])
def trigger_merit_ranking(scheme_id: str):
    ranked_list = MeritAndSelectionService.generate_merit_list(scheme_id.upper())
    db.save_to_json()
    return ranked_list

@router.post("/sanction/{app_id}/issue", response_model=DigitalSanctionOrder)
def issue_sanction_order(app_id: str):
    try:
        sanction = DBTPaymentService.issue_digital_sanction(app_id)
        db.save_to_json()
        return sanction
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/sanction/{sanction_id}", response_model=DigitalSanctionOrder)
def get_sanction_order(sanction_id: str):
    if sanction_id not in db.sanctions:
        raise HTTPException(status_code=404, detail="Sanction order not found.")
    return db.sanctions[sanction_id]

# --- Stage 5: DBT Payment ---
@router.post("/dbt/{app_id}/disburse", response_model=ApplicationRecord)
def execute_payment_disbursement(app_id: str):
    try:
        app = DBTPaymentService.execute_pfms_dbt_disbursement(app_id)
        db.save_to_json()
        return app
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Cross-Cutting: JAGO Chatbot, Anti-Fraud & Analytics ---
@router.post("/jago/chat", response_model=JAGOChatResponse)
def jago_chatbot_query(req: JAGOChatRequest):
    return JAGOChatbotService.process_chat_message(req)

@router.get("/antifraud/audit")
def get_antifraud_audit():
    return AntiFraudSentryService.audit_document_hashes()

@router.get("/analytics/summary", response_model=AnalyticsSummary)
def get_analytics_summary():
    return AnalyticsService.get_dashboard_summary()

@router.post("/ai/recommend-scheme", response_model=AISchemeRecommendationResponse)
def ai_recommend_scheme(req: AISchemeRecommendationRequest):
    return AISchemeRecommender.recommend(req)

# --- Cross-Cutting: Database State Persistence & Snapshots ---
@router.post("/admin/save-db")
def save_database_to_disk():
    return db.save_to_json()

@router.post("/admin/reload-db")
def reload_database_from_disk():
    success = db.load_from_json()
    return {
        "status": "SUCCESS" if success else "FAILED",
        "students_count": len(db.students),
        "applications_count": len(db.applications),
        "sanctions_count": len(db.sanctions)
    }

@router.get("/admin/db-status")
def get_database_status():
    return {
        "is_persisted": True,
        "students_count": len(db.students),
        "applications_count": len(db.applications),
        "sanctions_count": len(db.sanctions)
    }


