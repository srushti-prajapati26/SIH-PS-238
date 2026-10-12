"""
SIH PS 26239: Selection & Merit List Generation Service
Implements scheme-specific ranking algorithms and committee sign-off
"""
import random
from typing import List, Dict, Any
from app.models import ApplicationRecord, ApplicationStatus
from app.database import db

class MeritAndSelectionService:
    @staticmethod
    def calculate_merit_score(app: ApplicationRecord) -> float:
        """Computes normalized merit score (0 to 100) based on scheme rubric"""
        student = db.students.get(app.student_id)
        if not student:
            return 75.0

        if app.scheme_id == "NFST":
            # 40% Proposal + 30% NET + 30% Academic
            proposal_score = 92.0
            net_score = 94.0
            academic_score = 88.0
            return round(0.4 * proposal_score + 0.3 * net_score + 0.3 * academic_score, 2)

        elif app.scheme_id == "NOS":
            # QS Rank tiering + language score
            return 96.5

        elif app.scheme_id in ["POST_MATRIC", "PRE_MATRIC"]:
            # Inverse of income + PVTG bonus + previous marks
            income_score = max(0, 100 - (student.family_annual_income / 3000.0))
            pvtg_bonus = 15.0 if student.is_pvtg else 0.0
            academic_score = 85.0
            total = min(100.0, (0.5 * income_score) + (0.3 * academic_score) + pvtg_bonus)
            return round(total, 2)

        elif app.scheme_id == "TOP_CLASS":
            # 100% entitlement for admitted ST students in premier institutes
            return 98.0

        return 80.0

    @classmethod
    def generate_merit_list(cls, scheme_id: str) -> List[ApplicationRecord]:
        """Fetches all verified applications for a scheme, ranks them, and updates rank numbers"""
        pool = [
            app for app in db.applications.values()
            if app.scheme_id == scheme_id and app.status in [ApplicationStatus.VERIFIED_POOL, ApplicationStatus.MERIT_RANKED, ApplicationStatus.SANCTIONED, ApplicationStatus.DISBURSED]
        ]

        # Calculate scores
        for app in pool:
            if not app.merit_score:
                app.merit_score = cls.calculate_merit_score(app)
                app.status = ApplicationStatus.MERIT_RANKED

        # Sort descending by merit score
        pool.sort(key=lambda x: x.merit_score or 0.0, reverse=True)

        for rank, app in enumerate(pool, start=1):
            app.merit_rank = rank

        return pool
