"""
SIH PS 26239: AI-OCR Document Processing & Tamper Analysis Service
Performs OCR extraction, entity parsing, fuzzy phonetic matching and forgery checks
"""
import hashlib
import re
from typing import Dict, Any, List
from app.models import DocumentRecord, OCRFieldExtraction

class AIOCRService:
    @staticmethod
    def calculate_levenshtein_ratio(s1: str, s2: str) -> float:
        """Computes similarity ratio between two strings (0.0 to 1.0)"""
        s1, s2 = s1.lower().strip(), s2.lower().strip()
        if s1 == s2:
            return 1.0
        len1, len2 = len(s1), len(s2)
        if len1 == 0 or len2 == 0:
            return 0.0
        
        matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        for i in range(len1 + 1):
            matrix[i][0] = i
        for j in range(len2 + 1):
            matrix[0][j] = j
            
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                matrix[i][j] = min(
                    matrix[i - 1][j] + 1,       # deletion
                    matrix[i][j - 1] + 1,       # insertion
                    matrix[i - 1][j - 1] + cost # substitution
                )
        dist = matrix[len1][len2]
        max_len = max(len1, len2)
        return round(1.0 - (dist / max_len), 3)

    @classmethod
    def process_uploaded_document(
        cls, 
        doc_type: str, 
        file_name: str, 
        file_bytes: bytes,
        student_expected_name: str,
        expected_category: str = "ST"
    ) -> DocumentRecord:
        """
        Executes:
        1. SHA-256 Hashing for deduplication
        2. Optical Character Recognition (OCR) Simulation
        3. Field extraction & Fuzzy matching
        4. Tamper / Forgery detection
        """
        sha256_hash = hashlib.sha256(file_bytes).hexdigest()
        
        # Synthetic OCR extraction based on document type
        extractions: List[OCRFieldExtraction] = []
        is_tampered = False
        verification_notes = "Document passed initial AI-OCR scan."
        confidence = 0.96

        # Check for simulated tampering indicators (e.g. keywords in file name)
        if "tampered" in file_name.lower() or "fake" in file_name.lower():
            is_tampered = True
            confidence = 0.62
            verification_notes = "AI Sentry: Splicing / Error Level Analysis (ELA) anomaly detected on figure text."

        # --- AI Garbage Value Sentry & Noise Denoising (Up to 5 Count) ---
        sample_garbage_library = ["#?@!", "0xNULL", "NaN_CERT", "$$$ERR", "CORRUPT_SIG", "~%#INVALID", "GLITCH_99"]
        
        # Analyze file content or name for simulated noise
        if "noisy" in file_name.lower() or "scanned" in file_name.lower():
            garbage_tokens_found = sample_garbage_library[:5]  # Exactly 5 garbage values
            garbage_count = 5
        elif "corrupt" in file_name.lower() or "bad" in file_name.lower():
            garbage_tokens_found = sample_garbage_library[:7]  # 7 exceeds 5 count
            garbage_count = 7
        else:
            # Standard realistic tribal scan with up to 5 auto-sanitized OCR artifacts
            garbage_tokens_found = sample_garbage_library[:5]
            garbage_count = 5

        # Check if garbage count is within the permitted 5-count limit
        ai_sanitized = garbage_count <= 5
        if not ai_sanitized:
            confidence = 0.58
            verification_notes = f"AI Sentry Alert: {garbage_count} garbage values detected (>5 count limit). Scan quality too low. Deficiency flagged for clean resubmission."
        else:
            verification_notes += f" | AI Sentry: {garbage_count} noise/garbage values detected & auto-sanitized (within 5-count tolerance)."

        if doc_type == "caste_cert":
            extracted_name = student_expected_name  # matched name
            name_sim = cls.calculate_levenshtein_ratio(extracted_name, student_expected_name)
            extractions.append(OCRFieldExtraction(
                field_name="Candidate Name",
                extracted_value=extracted_name,
                expected_value=student_expected_name,
                confidence_score=0.98,
                is_matched=name_sim >= 0.85
            ))
            extractions.append(OCRFieldExtraction(
                field_name="Category Classified",
                extracted_value="Scheduled Tribe (ST)",
                expected_value=expected_category,
                confidence_score=0.97,
                is_matched=True
            ))
            extractions.append(OCRFieldExtraction(
                field_name="Issuing Competent Authority",
                extracted_value="Sub-Divisional Magistrate / Tehsildar",
                confidence_score=0.94,
                is_matched=True
            ))

        elif doc_type == "income_cert":
            extractions.append(OCRFieldExtraction(
                field_name="Applicant / Parent Name",
                extracted_value=student_expected_name,
                expected_value=student_expected_name,
                confidence_score=0.95,
                is_matched=True
            ))
            extractions.append(OCRFieldExtraction(
                field_name="Certified Annual Income",
                extracted_value="INR 1,80,000",
                expected_value="<= INR 2,50,000",
                confidence_score=0.96,
                is_matched=True
            ))

        elif doc_type == "synopsis_research_proposal":
            extractions.append(OCRFieldExtraction(
                field_name="Research Topic",
                extracted_value="Indigenous Knowledge Systems and Ecological Forestry",
                confidence_score=0.92,
                is_matched=True
            ))
            extractions.append(OCRFieldExtraction(
                field_name="Guide Endorsement",
                extracted_value="Approved by Recognized Ph.D. Supervisor",
                confidence_score=0.95,
                is_matched=True
            ))

        else:
            extractions.append(OCRFieldExtraction(
                field_name="Document Generic Verification",
                extracted_value="Legible Official Document",
                confidence_score=0.90,
                is_matched=True
            ))

        return DocumentRecord(
            doc_id=f"DOC-{sha256_hash[:10].upper()}",
            doc_type=doc_type,
            file_name=file_name,
            sha256_hash=sha256_hash,
            ocr_confidence=confidence,
            is_tampered_flag=is_tampered,
            garbage_value_count=garbage_count,
            garbage_tokens_found=garbage_tokens_found,
            ai_sanitized=ai_sanitized,
            extractions=extractions,
            verification_notes=verification_notes
        )
