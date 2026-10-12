"""
SIH PS 26239: Pydantic Data Models & Schemas
Defines core data structures for all lifecycle entities
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class ApplicationStatus(str, Enum):
    DRAFT = "DRAFT"
    PROFILE_VERIFIED = "PROFILE_VERIFIED"
    SUBMITTED = "SUBMITTED"
    TIER1_AI_AUDIT = "TIER1_AI_AUDIT"
    TIER2_INSTITUTION = "TIER2_INSTITUTION"
    TIER3_MOTA_STATE = "TIER3_MOTA_STATE"
    DEFICIENCY_RAISED = "DEFICIENCY_RAISED"
    VERIFIED_POOL = "VERIFIED_POOL"
    MERIT_RANKED = "MERIT_RANKED"
    SANCTIONED = "SANCTIONED"
    PAYMENT_INITIATED = "PAYMENT_INITIATED"
    DISBURSED = "DISBURSED"
    REJECTED = "REJECTED"

class VerificationTier(str, Enum):
    TIER_1_AI = "TIER_1_AI"
    TIER_2_INSTITUTE = "TIER_2_INSTITUTE"
    TIER_3_MOTA = "TIER_3_MOTA"

# --- Phase 1: OTR & Student Profile ---
class BankAccountInfo(BaseModel):
    account_number_masked: str
    ifsc_code: str
    bank_name: str
    is_aadhaar_seeded: bool = True
    npci_status: str = "ACTIVE"

class StudentProfile(BaseModel):
    student_id: str = Field(..., description="Unique Student ID e.g. MOTA-2026-ST-...")
    full_name: str
    father_name: str
    dob: str
    gender: str
    aadhaar_masked: str
    is_aadhaar_verified: bool = True
    caste_category: str = "ST"  # ST or PVTG
    is_pvtg: bool = False
    pvtg_community_name: Optional[str] = None
    state_of_domicile: str
    district: str
    disability_status: bool = False
    disability_percentage: float = 0.0
    family_annual_income: float
    apaar_abc_id: Optional[str] = None
    udise_school_code: Optional[str] = None
    bank_account: BankAccountInfo
    created_at: datetime = Field(default_factory=datetime.utcnow)

class OTRRegistrationRequest(BaseModel):
    full_name: str
    aadhaar_number: str
    mobile_number: str
    state_of_domicile: str
    district: str
    is_pvtg: bool = False
    pvtg_community: Optional[str] = None
    annual_income: float
    bank_account_number: str
    ifsc_code: str
    bank_name: str

# --- Phase 2: Document Processing & AI OCR ---
class OCRFieldExtraction(BaseModel):
    field_name: str
    extracted_value: str
    expected_value: Optional[str] = None
    confidence_score: float = 0.95
    is_matched: bool = True

class DocumentRecord(BaseModel):
    doc_id: str
    doc_type: str  # income_cert, caste_cert, marksheet, research_proposal, etc.
    file_name: str
    sha256_hash: str
    upload_timestamp: datetime = Field(default_factory=datetime.utcnow)
    ocr_confidence: float = 0.96
    is_tampered_flag: bool = False
    garbage_value_count: int = 5  # Tracks garbage/noise tokens up to 5 count
    garbage_tokens_found: List[str] = Field(default_factory=lambda: ["#?@!", "0xNULL", "NaN_CERT", "$$$ERR", "CORRUPT_SIG"])
    ai_sanitized: bool = True
    extractions: List[OCRFieldExtraction] = []
    verification_notes: Optional[str] = None

class AISchemeRecommendationRequest(BaseModel):
    education_level: str
    annual_income: float
    is_pvtg: bool = False
    academic_marks_percent: float = 85.0
    field_of_study: Optional[str] = None
    target_institution: Optional[str] = None
    wants_foreign_study: bool = False

class AISchemeRecommendationResponse(BaseModel):
    recommended_scheme_id: str
    scheme_name: str
    confidence_score: float
    entitlement_summary: str
    matching_reasons: List[str]
    ai_rationale: str


# --- Phase 3: Application Submission & 3-Tier Verification ---
class SchemeApplicationRequest(BaseModel):
    student_id: str
    scheme_id: str  # PRE_MATRIC, POST_MATRIC, TOP_CLASS, NFST, NOS
    institution_name: str
    course_name: str
    current_year_of_study: int
    course_duration_years: int
    tuition_fees_claimed: float = 0.0
    is_hosteller: bool = False
    uploaded_docs: List[DocumentRecord] = []
    # Scheme specific extras
    research_proposal_title: Optional[str] = None
    net_score: Optional[float] = None
    foreign_univ_qs_rank: Optional[int] = None
    gre_ielts_score: Optional[float] = None

class DeficiencyRecord(BaseModel):
    deficiency_id: str
    tier_raised_by: VerificationTier
    issue_description: str
    required_action: str
    flagged_document: Optional[str] = None
    raised_at: datetime = Field(default_factory=datetime.utcnow)
    is_resolved: bool = False
    resolution_timestamp: Optional[datetime] = None
    student_response_comment: Optional[str] = None

class ApplicationRecord(BaseModel):
    application_id: str
    student_id: str
    scheme_id: str
    institution_name: str
    course_name: str
    status: ApplicationStatus = ApplicationStatus.SUBMITTED
    submission_timestamp: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    # Financial breakdown
    claimed_amount: float
    approved_amount: float = 0.0
    
    # Multi-Tier checks
    tier1_ai_audit_score: float = 0.0
    tier1_ai_audit_passed: bool = False
    tier2_institute_verified: bool = False
    tier2_verifier_name: Optional[str] = None
    tier3_mota_approved: bool = False
    tier3_approver_name: Optional[str] = None
    
    # Deficiency tracking
    deficiencies: List[DeficiencyRecord] = []
    
    # Merit & Sanction
    merit_score: Optional[float] = None
    merit_rank: Optional[int] = None
    sanction_order_id: Optional[str] = None
    sanction_date: Optional[str] = None
    
    # DBT & Payment
    pfms_transaction_id: Optional[str] = None
    utr_number: Optional[str] = None
    payment_status: str = "PENDING"
    disbursement_date: Optional[str] = None

class TierVerificationActionRequest(BaseModel):
    action: str  # "APPROVE", "REJECT", "RAISE_DEFICIENCY"
    tier: VerificationTier
    verifier_name: str
    comments: str
    deficiency_doc_flag: Optional[str] = None
    deficiency_instructions: Optional[str] = None

class DeficiencyResolutionRequest(BaseModel):
    deficiency_id: str
    student_comment: str
    corrected_document: Optional[DocumentRecord] = None

# --- Phase 4 & 5: Sanction & DBT ---
class DigitalSanctionOrder(BaseModel):
    sanction_order_id: str
    application_id: str
    student_id: str
    student_name: str
    scheme_name: str
    institution_name: str
    sanctioned_amount: float
    academic_year: str = "2026-2027"
    digital_signature_hash: str
    qr_code_data: str
    sanction_date: str

class DBTPaymentBatch(BaseModel):
    batch_id: str
    total_beneficiaries: int
    total_amount: float
    pfms_ref_number: str
    apbs_status: str
    settled_at: str

# --- Cross-Cutting: JAGO Chatbot ---
class JAGOChatRequest(BaseModel):
    student_id: Optional[str] = None
    user_query: str
    language_code: str = "en"

class JAGOChatResponse(BaseModel):
    query: str
    bot_reply: str
    language_code: str
    identified_intent: str
    suggested_actions: List[str] = []
    source_citation: Optional[str] = None
    card_type: Optional[str] = None
    card_data: Optional[Dict[str, Any]] = None
    interactive_actions: Optional[List[Dict[str, str]]] = None

# --- Cross-Cutting: Analytics Dashboard ---
class AnalyticsSummary(BaseModel):
    total_applications: int
    under_verification: int
    approved_applications: int
    deficiency_cases: int
    disbursed_count: int
    total_amount_disbursed_inr: float
    scheme_breakdown: Dict[str, int]
    avg_processing_time_days: float
    fraud_prevention_stats: Dict[str, Any]
