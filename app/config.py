"""
SIH PS 26239: AI-Enabled Scholarship and Fellowship Management System
Ministry of Tribal Affairs (MoTA), Government of India
Core Configuration & Scheme Definitions
"""
from typing import Dict, Any

APP_NAME = "ShikshaKendra - MoTA AI-Enabled Scholarship & Fellowship Management System"
VERSION = "2.1.0"
API_PREFIX = "/api/v1"

# AI Garbage Value Detection Thresholds
MAX_GARBAGE_VALUE_COUNT = 5  # Tolerates up to 5 garbage/noisy tokens before rejection
SAMPLE_GARBAGE_TOKENS = ["#?@!", "0xNULL", "NaN_CERT", "$$$ERR", "CORRUPT_SIG"]

SCHEMES_CONFIG: Dict[str, Dict[str, Any]] = {
    "PRE_MATRIC": {
        "id": "PRE_MATRIC",
        "name": "Pre-Matric Scholarship for ST Students (Classes IX & X)",
        "min_class": 9,
        "max_class": 10,
        "max_income": 250000.0,  # INR 2.5 Lakhs
        "required_docs": ["income_cert", "caste_cert", "marksheet_prev_year", "school_bonafide"],
        "base_amount": 3500.0,
        "pvtg_priority_weight": 1.25,
    },
    "POST_MATRIC": {
        "id": "POST_MATRIC",
        "name": "Post-Matric Scholarship for ST Students (XI to Post-Graduation)",
        "min_class": 11,
        "max_class": 16,
        "max_income": 250000.0,  # INR 2.5 Lakhs
        "required_docs": ["income_cert", "caste_cert", "marksheet_prev_year", "college_fee_receipt", "hostel_cert"],
        "base_amount": 12000.0,
        "pvtg_priority_weight": 1.20,
    },
    "TOP_CLASS": {
        "id": "TOP_CLASS",
        "name": "National Fellowship / Top Class Education in Premier Institutes",
        "eligible_institutes": ["IIT", "IIM", "NIT", "AIIMS", "NLSIU", "IISc"],
        "max_income": 600000.0,  # INR 6.0 Lakhs
        "required_docs": ["income_cert", "caste_cert", "admission_letter", "tuition_fee_schedule"],
        "full_tuition_covered": True,
        "annual_living_allowance": 45000.0,
    },
    "NFST": {
        "id": "NFST",
        "name": "National Fellowship for Higher Education of ST Students (M.Phil / Ph.D.)",
        "qualifying_exams": ["UGC-NET", "CSIR-NET", "GATE"],
        "max_income": 800000.0,  # INR 8.0 Lakhs
        "required_docs": ["caste_cert", "synopsis_research_proposal", "net_scorecard", "guide_consent_letter"],
        "monthly_stipend": 31000.0,
        "contingency_annual": 25000.0,
        "scoring_weights": {
            "proposal_quality": 0.40,
            "net_percentile": 0.30,
            "pg_academic_marks": 0.30
        }
    },
    "NOS": {
        "id": "NOS",
        "name": "National Overseas Scholarship for ST Candidates (Foreign Masters / Ph.D.)",
        "max_qs_rank": 500,
        "max_income": 800000.0,  # INR 8.0 Lakhs
        "required_docs": ["caste_cert", "foreign_offer_letter", "gre_ielts_scorecard", "visa_copy"],
        "annual_stipend_usd": 15400.0,
        "covers_airfare": True,
        "scoring_weights": {
            "qs_rank_weight": 0.50,
            "language_academic_score": 0.30,
            "socio_economic_index": 0.20
        }
    }
}

# Supported Indian Vernacular Languages for JAGO AI Chatbot
SUPPORTED_LANGUAGES = [
    {"code": "hi", "name": "Hindi (हिंदी)"},
    {"code": "en", "name": "English"},
    {"code": "sat", "name": "Santhali (ᱥᱟᱱᱛᱟᱲᱤ)"},
    {"code": "gon", "name": "Gondi (गोण्डी)"},
    {"code": "or", "name": "Odia (ଓଡ଼ିଆ)"},
    {"code": "bn", "name": "Bengali (বাংলা)"},
    {"code": "te", "name": "Telugu (తెలుగు)"},
    {"code": "mr", "name": "Marathi (मराठी)"},
    {"code": "gu", "name": "Gujarati (ગુજરાતી)"}
]
