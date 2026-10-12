"""
SIH PS 26239: Configurable Business Rules Engine (BRE)
Applies scheme eligibility rules, income limits, academic criteria, and required document checklists
"""
from typing import Dict, Any, List, Tuple
from app.config import SCHEMES_CONFIG
from app.models import StudentProfile, SchemeApplicationRequest

class BusinessRulesEngine:
    @staticmethod
    def evaluate_scheme_eligibility(
        profile: StudentProfile, 
        req: SchemeApplicationRequest
    ) -> Tuple[bool, List[str], float]:
        """
        Evaluates an application against scheme-specific rules.
        Returns: (is_eligible, list_of_deficiencies/reasons, calculated_entitlement_amount)
        """
        scheme_id = req.scheme_id.upper()
        if scheme_id not in SCHEMES_CONFIG:
            return False, [f"Unknown scheme identifier: {scheme_id}"], 0.0

        rules = SCHEMES_CONFIG[scheme_id]
        violations = []
        approved_amount = 0.0

        # 1. Category Requirement (Must be ST)
        if profile.caste_category != "ST":
            violations.append("Candidate does not belong to the Scheduled Tribe (ST) category.")

        # 2. Income Ceilings
        max_allowed_income = rules.get("max_income", 250000.0)
        if profile.family_annual_income > max_allowed_income:
            violations.append(
                f"Family income ₹{profile.family_annual_income:,.0f} exceeds maximum ceiling of ₹{max_allowed_income:,.0f} for scheme {scheme_id}."
            )

        # 3. Scheme-specific checks
        if scheme_id == "PRE_MATRIC":
            if req.current_year_of_study not in [9, 10]:
                violations.append("Pre-Matric scholarship is only applicable for Class IX and X students.")
            approved_amount = rules.get("base_amount", 3500.0)
            if profile.is_pvtg:
                approved_amount *= rules.get("pvtg_priority_weight", 1.25)

        elif scheme_id == "POST_MATRIC":
            base = rules.get("base_amount", 12000.0)
            # Add tuition claimed up to reasonable cap
            approved_amount = base + min(req.tuition_fees_claimed, 50000.0)
            if req.is_hosteller:
                approved_amount += 12000.0  # Hosteller maintenance allowance

        elif scheme_id == "TOP_CLASS":
            # Check institute accreditation
            eligible_insts = rules.get("eligible_institutes", [])
            is_valid_inst = any(inst.lower() in req.institution_name.lower() for inst in eligible_insts)
            if not is_valid_inst:
                violations.append(f"Institution '{req.institution_name}' is not in the notified Top Class premier institutes list.")
            approved_amount = req.tuition_fees_claimed + rules.get("annual_living_allowance", 45000.0)

        elif scheme_id == "NFST":
            # National Fellowship for ST Ph.D.
            if not req.research_proposal_title:
                violations.append("Research Proposal Synopsis title is mandatory for NFST fellowship.")
            approved_amount = (rules.get("monthly_stipend", 31000.0) * 12) + rules.get("contingency_annual", 25000.0)

        elif scheme_id == "NOS":
            # National Overseas Scholarship
            if req.foreign_univ_qs_rank and req.foreign_univ_qs_rank > rules.get("max_qs_rank", 500):
                violations.append(f"Foreign University QS Rank #{req.foreign_univ_qs_rank} exceeds maximum permissible rank of 500.")
            approved_amount = 1300000.0  # Approximate INR equivalent for foreign fellowship

        is_eligible = len(violations) == 0
        return is_eligible, violations, round(approved_amount, 2)
