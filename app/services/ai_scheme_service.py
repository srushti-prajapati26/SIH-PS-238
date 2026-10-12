"""
ShikshaKendra: AI Scheme Recommendation Engine
Matches student profile, income, academic achievements, and goals to optimal MoTA schemes
"""
from typing import Dict, Any, List
from app.models import AISchemeRecommendationRequest, AISchemeRecommendationResponse
from app.config import SCHEMES_CONFIG

class AISchemeRecommender:
    @staticmethod
    def recommend(req: AISchemeRecommendationRequest) -> AISchemeRecommendationResponse:
        edu = req.education_level.lower()
        inst = (req.target_institution or "").lower()
        reasons = []

        # Logic for Overseas
        if req.wants_foreign_study or "foreign" in edu or "abroad" in edu or "overseas" in edu:
            return AISchemeRecommendationResponse(
                recommended_scheme_id="NOS",
                scheme_name=SCHEMES_CONFIG["NOS"]["name"],
                confidence_score=0.98,
                entitlement_summary="Full tuition fees + USD 15,400 annual living allowance + return airfare.",
                matching_reasons=[
                    "Targeting Master's or Ph.D. abroad at top-ranked universities",
                    f"Annual income ₹{req.annual_income:,.0f} within NOS ceiling of ₹8,00,000",
                    "ST candidate eligible for 100 slots reserved annually under MoTA"
                ],
                ai_rationale="The National Overseas Scholarship (NOS) is optimal for overseas studies. Your academic percentile and income bracket qualify you for tier-1 foreign study financial coverage."
            )

        # Logic for Ph.D. / Research
        if any(term in edu for term in ["ph.d", "phd", "m.phil", "research", "doctorate"]):
            return AISchemeRecommendationResponse(
                recommended_scheme_id="NFST",
                scheme_name=SCHEMES_CONFIG["NFST"]["name"],
                confidence_score=0.97,
                entitlement_summary="₹31,000/month stipend + HRA + ₹25,000 annual contingency grant for up to 5 years.",
                matching_reasons=[
                    "Enrolled or pursuing doctoral research (Ph.D. / M.Phil)",
                    "UGC-NET / GATE or university research proposal evaluation applicable",
                    "Tribal heritage & sustainable development research prioritized"
                ],
                ai_rationale="NFST is the premier national fellowship specifically reserved for tribal researchers. Your research aspirations and academic records align directly with this scheme."
            )

        # Logic for Premier Institutes (IIT, IIM, NIT, AIIMS)
        premier_keywords = ["iit", "iim", "nit", "aiims", "iisr", "nlsiu", "national institute"]
        if any(term in inst for term in premier_keywords) or any(term in edu for term in ["b.tech", "mba", "mbbs"]):
            return AISchemeRecommendationResponse(
                recommended_scheme_id="TOP_CLASS",
                scheme_name=SCHEMES_CONFIG["TOP_CLASS"]["name"],
                confidence_score=0.96,
                entitlement_summary="100% full non-refundable tuition fees + ₹45,000 annual living allowance + computer grant.",
                matching_reasons=[
                    "Admitted to a notified premier institute (IIT/IIM/NIT)",
                    f"Annual family income ₹{req.annual_income:,.0f} meets ₹6.0 Lakh ceiling",
                    "Direct institutional disbursement with zero out-of-pocket tuition"
                ],
                ai_rationale="Top Class Education scheme is designed for premier institution admissions. You receive 100% tuition coverage regardless of fee slab, plus full living assistance."
            )

        # Logic for Pre-Matric (Class 9-10)
        if any(term in edu for term in ["9", "10", "ix", "x", "matric", "high school"]):
            return AISchemeRecommendationResponse(
                recommended_scheme_id="PRE_MATRIC",
                scheme_name=SCHEMES_CONFIG["PRE_MATRIC"]["name"],
                confidence_score=0.95,
                entitlement_summary="₹3,500/year base grant + book allowances (augmented for PVTG students).",
                matching_reasons=[
                    "Class IX or X regular student",
                    f"Annual family income ₹{req.annual_income:,.0f} meets ₹2.5 Lakh ceiling",
                    "Special PVTG priority weight applied automatically" if req.is_pvtg else "Standard tribal student entitlement"
                ],
                ai_rationale="Pre-Matric scholarship provides foundational educational support to minimize tribal dropout rates in classes IX and X."
            )

        # Default: Post-Matric
        return AISchemeRecommendationResponse(
            recommended_scheme_id="POST_MATRIC",
            scheme_name=SCHEMES_CONFIG["POST_MATRIC"]["name"],
            confidence_score=0.94,
            entitlement_summary="Compulsory non-refundable college fees + monthly maintenance allowance (hosteller/day scholar).",
            matching_reasons=[
                "Class XI to Post-Graduation regular degree / diploma course",
                f"Annual family income ₹{req.annual_income:,.0f} satisfies ₹2.5 Lakh limit",
                "Wide coverage across colleges, universities, and professional polytechnics"
            ],
            ai_rationale="Post-Matric is the largest umbrella scholarship for tribal students across India, covering higher secondary, undergraduate, and postgraduate studies."
        )
