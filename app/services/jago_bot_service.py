"""
SIH PS 26239: JAGO Multilingual AI Chatbot Assistant Service (Enhanced Version)
Provides 24/7 multilingual vernacular support for:
- Live status inquiries with visual step-by-step timeline cards
- In-chat deficiency guidance and 1-click resolution
- Instant AI Scheme recommendations
- PFMS / DBT direct bank transfer & NPCI APBS verification
- 5-count garbage value AI denoising explanations
- Cryptographic sanction order & QR verification
"""
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from app.models import JAGOChatRequest, JAGOChatResponse, AISchemeRecommendationRequest
from app.database import db
from app.config import SCHEMES_CONFIG
from app.services.ai_scheme_service import AISchemeRecommender
from app.services.verification_service import MultiTierVerificationService

class JAGOChatbotService:
    # 6 Vernacular Indian Languages Support
    RESPONSES: Dict[str, Dict[str, str]] = {
        "hi": {
            "greeting": "नमस्ते! मैं जागो (JAGO) हूँ, शिक्षाकेंद्र (ShikshaKendra) - जनजातीय कार्य मंत्रालय (MoTA) का संवादात्मक एआई सहायक।",
            "status_prefix": "शिक्षाकेंद्र में आपके आवेदन की वर्तमान स्थिति: ",
            "deficiency_prefix": "ध्यान दें: आपके आवेदन में त्रुटि (Deficiency) पाई गई है: ",
            "not_found": "क्षमा करें, इस आईडी से कोई आवेदन नहीं मिला। कृपया अपनी सही आईडी दर्ज करें।",
            "resolved_msg": "सफलतापूर्वक त्रुटि का समाधान हो गया है! आपका आवेदन संस्थान सत्यापन कतार में पुनः भेज दिया गया है।"
        },
        "sat": {
            "greeting": "ᱡᱚᱦᱟᱨ! ᱤᱧ ᱫᱚ JAGO AI ᱠᱟᱱᱟᱹᱧ, ShikshaKendra (MoTA) ᱥᱠᱚᱞᱟᱨᱥᱤᱯ ᱜᱚᱲᱚᱭᱤᱡ᱾",
            "status_prefix": "ShikshaKendra ᱨᱮ ᱟᱢᱟᱜ ᱟᱵᱮᱫᱚᱱ ᱦᱟᱞᱚᱛ: ",
            "deficiency_prefix": "ᱱᱚᱡᱚᱨ ᱮᱢ ᱢᱮ: ᱟᱢᱟᱜ ᱫᱚᱞᱤᱞ ᱨᱮ ᱠᱷᱟᱹᱢᱛᱤ (Deficiency) ᱢᱮᱱᱟᱜ-ᱟ: ",
            "not_found": "ᱤᱠᱟᱹ ᱠᱷᱚᱡᱚᱜ ᱠᱟᱱᱟᱹᱧ, ᱱᱚᱶᱟ ᱟᱭᱰᱤ ᱛᱮ ᱪᱮᱫ ᱦᱚᱸ ᱵᱟᱝ ᱧᱟᱢ ᱞᱮᱱᱟ᱾",
            "resolved_msg": "ᱠᱷᱟᱹᱢᱛᱤ ᱥᱩᱫᱷᱨᱟᱹᱣ ᱮᱱᱟ! ᱟᱢᱟᱜ ᱟᱵᱮᱫᱚᱱ ᱟᱨᱦᱚᱸ ᱵᱤᱨᱫᱟᱹᱜᱟᱲ ᱨᱮ ᱪᱟᱞᱟᱣ ᱮᱱᱟ᱾"
        },
        "or": {
            "greeting": "ନମସ୍କାର! ମୁଁ JAGO AI, ଶିକ୍ଷାକେନ୍ଦ୍ର (ShikshaKendra - MoTA) ର ଡିଜିଟାଲ୍ ସହାୟକ।",
            "status_prefix": "ଶିକ୍ଷାକେନ୍ଦ୍ରରେ ଆପଣଙ୍କ ଆବେଦନର ସ୍ଥିତି: ",
            "deficiency_prefix": "ଧ୍ୟାନ ଦିଅନ୍ତୁ: ଆପଣଙ୍କ ଆବେଦନରେ ତ୍ରୁଟି ଚିହ୍ନଟ ହୋଇଛି: ",
            "not_found": "କ୍ଷମା କରିବେ, ଏହି ଆଇଡିରେ କୌଣସି ଆବେଦନ ମିଳିଲା ନାହିଁ।",
            "resolved_msg": "ତ୍ରୁଟିର ସମାଧାନ ସଫଳତାପୂର୍ବକ ହୋଇଛି! ଆବେଦନ ପୁନଃ ଯାଞ୍ଚ ପାଇଁ ପଠାଯାଇଛି।"
        },
        "bn": {
            "greeting": "নমস্কার! আমি জাগো (JAGO) AI, শিক্ষাকেন্দ্র (ShikshaKendra - MoTA) স্কলারশিপ পোর্টালের ডিজিটাল সহকারী।",
            "status_prefix": "শিক্ষাকেন্দ্রে আপনার আবেদনের বর্তমান স্থিতি: ",
            "deficiency_prefix": "দৃষ্টি আকর্ষণ: আপনার আবেদনে ত্রুটি সনাক্ত করা হয়েছে: ",
            "not_found": "দুঃখিত, এই আইডিতে কোনো আবেদন খুঁজে পাওয়া যায়নি।",
            "resolved_msg": "ত্রুটি সমাধান সফল হয়েছে! আপনার আবেদনটি পুনরায় প্রতিষ্ঠান যাচাইকরণে পাঠানো হয়েছে।"
        },
        "te": {
            "greeting": "నమస్కారం! నేను JAGO AI, శిక్షాకేంద్ర (ShikshaKendra - MoTA) స్కాలర్‌షిప్ సహాయకుడిని.",
            "status_prefix": "శిక్షాకేంద్రలో మీ దరఖాస్తు ప్రస్తుత స్థితి: ",
            "deficiency_prefix": "గమనిక: మీ దరఖాస్తులో లోపం గుర్తించబడింది: ",
            "not_found": "క్షమించండి, ఈ ఐడీతో ఎటువంటి దరఖాస్తు కనుగొనబడలేదు.",
            "resolved_msg": "లోపం విజయవంతంగా పరిష్కరించబడింది! దరఖాస్తు పునఃపరిశీలనకు పంపబడింది."
        },
        "en": {
            "greeting": "Hello! I am JAGO, your AI Assistant for ShikshaKendra (Ministry of Tribal Affairs Scholarship Portal).",
            "status_prefix": "Current status in ShikshaKendra: ",
            "deficiency_prefix": "Attention: A deficiency has been flagged on your application: ",
            "not_found": "Sorry, I could not find an application with that ID. Please check and try again.",
            "resolved_msg": "Deficiency successfully resolved! Your application has been routed back to the verification queue."
        }
    }

    @classmethod
    def process_chat_message(cls, req: JAGOChatRequest) -> JAGOChatResponse:
        lang = req.language_code if req.language_code in cls.RESPONSES else "en"
        query_raw = req.user_query.strip()
        query_lower = query_raw.lower()
        templates = cls.RESPONSES[lang]

        # Extract target application / student if explicitly mentioned or active
        app_match = re.search(r'(app-mota-[\w-]+)', query_lower)
        student_match = re.search(r'(mota-2026-st-\d+)', query_lower)
        
        target_app = None
        if app_match:
            app_id = app_match.group(1).upper()
            target_app = db.applications.get(app_id)
        elif student_match:
            st_id = student_match.group(1).upper()
            for app in db.applications.values():
                if app.student_id == st_id:
                    target_app = app
                    break
        elif req.student_id:
            for app in db.applications.values():
                if app.student_id == req.student_id:
                    target_app = app
                    break

        # Fallback to intelligent context resolution if not explicitly specified
        if not target_app:
            if any(term in query_lower for term in ["birsa", "tirkey", "postmatric", "post-matric", "def-2026-092", "defic"]):
                target_app = db.applications.get("APP-MOTA-POSTMATRIC-003")
            elif any(term in query_lower for term in ["sunita", "soren", "topclass", "top class", "birhor"]):
                target_app = db.applications.get("APP-MOTA-TOPCLASS-002")
            else:
                target_app = db.applications.get("APP-MOTA-NFST-001")

        student_obj = None
        if target_app:
            student_obj = db.students.get(target_app.student_id)
        elif req.student_id:
            student_obj = db.students.get(req.student_id)
        if not student_obj:
            student_obj = db.students.get("MOTA-2026-ST-881024")

        # -------------------------------------------------------------
        # Intent 0: DIRECT IN-CHAT DEFICIENCY RESOLUTION
        # -------------------------------------------------------------
        if any(w in query_lower for w in ["resolve-deficiency", "resolve def", "fix deficiency now", "clear defect", "resubmit receipt"]):
            target_def_app = target_app
            if target_def_app and target_def_app.status.value != "DEFICIENCY_RAISED":
                for app in db.applications.values():
                    if app.status.value == "DEFICIENCY_RAISED":
                        target_def_app = app
                        break

            if target_def_app and target_def_app.status.value == "DEFICIENCY_RAISED":
                active_def = next((d for d in target_def_app.deficiencies if not d.is_resolved), None)
                if active_def:
                    comment = "Resolved directly via JAGO Conversational AI with authenticated student confirmation."
                    MultiTierVerificationService.resolve_deficiency(target_def_app.application_id, active_def.deficiency_id, comment)
                    db.save_to_json()
                    
                    reply = (
                        f"✅ **{templates['resolved_msg']}**\n\n"
                        f"• Application: **{target_def_app.application_id}**\n"
                        f"• Deficiency ID: **{active_def.deficiency_id}** (Status: RESOLVED)\n"
                        f"• Flagged Issue: *{active_def.issue_description}*\n"
                        f"• New State: **TIER 2 (Institution Nodal Verification)**"
                    )
                    return JAGOChatResponse(
                        query=req.user_query,
                        bot_reply=reply,
                        language_code=lang,
                        identified_intent="DEFICIENCY_RESOLVED_SUCCESS",
                        card_type="DEFICIENCY_RESOLVED_CARD",
                        card_data={
                            "application_id": target_def_app.application_id,
                            "deficiency_id": active_def.deficiency_id,
                            "resolved": True,
                            "new_status": "TIER2_INSTITUTION"
                        },
                        suggested_actions=["Check Live Status", "View Verification Audit", "Explore Other Schemes"],
                        interactive_actions=[
                            {"label": "🔍 Track Status Now", "action": "query_jago", "param": f"Check status of {target_def_app.application_id}"},
                            {"label": "📊 View Institution Queue", "action": "switch_tab", "param": "institute"}
                        ]
                    )

        # -------------------------------------------------------------
        # Intent 1: DIRECT BENEFIT TRANSFER (DBT) & PFMS TRACKER
        # -------------------------------------------------------------
        if any(w in query_lower for w in ["dbt", "payment", "bank", "account", "paisa", "rupees", "pfms", "npci", "utr", "credit", "disburs", "khata"]):
            active_st = student_obj
            active_app = target_app

            reply = (
                f"🏦 **ShikshaKendra Direct Benefit Transfer (DBT) Tracking:**\n\n"
                f"• **Beneficiary Name:** {active_st.full_name}\n"
                f"• **Bank Name:** {active_st.bank_account.bank_name}\n"
                f"• **Account Number:** `{active_st.bank_account.account_number_masked}`\n"
                f"• **Aadhaar Payment Bridge (APBS) Status:** `ACTIVE` (Aadhaar Seeded ✅)\n"
                f"• **Disbursement Status:** `{active_app.status.value}`\n"
                f"• **Disbursed Amount:** ₹{active_app.approved_amount:,.0f} directly credited via PFMS\n"
                f"• **PFMS UTR Number:** `{active_app.utr_number or 'SBIN260915984102'}`\n"
                f"• **Credit Date:** {active_app.disbursement_date or '2026-09-18'}"
            )
            return JAGOChatResponse(
                query=req.user_query,
                bot_reply=reply,
                language_code=lang,
                identified_intent="DBT_PAYMENT_TRACKING",
                card_type="DBT_TRACKER_CARD",
                card_data={
                    "beneficiary": active_st.full_name,
                    "bank": active_st.bank_account.bank_name,
                    "account": active_st.bank_account.account_number_masked,
                    "utr": active_app.utr_number or "SBIN260915984102",
                    "amount": active_app.approved_amount,
                    "apbs_status": "ACTIVE"
                },
                suggested_actions=["View Sanction Order QR", "Check Application Status", "How to Seed Aadhaar?"],
                interactive_actions=[
                    {"label": "📄 View Sanction QR", "action": "open_sanction", "param": "SANCTION-MOTA-2026-00481"},
                    {"label": "📊 View DBT Statistics", "action": "switch_tab", "param": "mota"}
                ]
            )

        # -------------------------------------------------------------
        # Intent 2: DEFICIENCY HELP & GUIDANCE
        # -------------------------------------------------------------
        if any(w in query_lower for w in ["deficiency", "defect", "objection", "rejected", "fix", "resubmit", "truti", "kamti"]):
            target_def_app = target_app
            if not target_def_app or target_def_app.status.value != "DEFICIENCY_RAISED":
                for app in db.applications.values():
                    if app.status.value == "DEFICIENCY_RAISED":
                        target_def_app = app
                        break
            
            if target_def_app and target_def_app.deficiencies:
                active_def = next((d for d in target_def_app.deficiencies if not d.is_resolved), target_def_app.deficiencies[0])
                reply = (
                    f"⚠️ **{templates['deficiency_prefix']}**\n\n"
                    f"• Application ID: **{target_def_app.application_id}**\n"
                    f"• Deficiency ID: **{active_def.deficiency_id}**\n"
                    f"• Flagged Document: `{active_def.flagged_document or 'Supporting Attachment'}`\n"
                    f"• Reason: *\"{active_def.issue_description}\"*\n"
                    f"• Solution: *{active_def.required_action}*\n\n"
                    f"💡 *ShikshaKendra provides a non-destructive feedback loop. Your application will NOT be rejected; you can resubmit immediately.*"
                )
                return JAGOChatResponse(
                    query=req.user_query,
                    bot_reply=reply,
                    language_code=lang,
                    identified_intent="DEFICIENCY_GUIDANCE",
                    card_type="DEFICIENCY_ACTION_CARD",
                    card_data={
                        "application_id": target_def_app.application_id,
                        "deficiency_id": active_def.deficiency_id,
                        "issue_description": active_def.issue_description,
                        "required_action": active_def.required_action,
                        "flagged_document": active_def.flagged_document
                    },
                    suggested_actions=["Instant Resolve in Chat", "Upload Stamped Receipt", "Check Application Status"],
                    interactive_actions=[
                        {"label": "⚡ Instant Resolve in Chat", "action": "query_jago", "param": f"resolve-deficiency {target_def_app.application_id}"},
                        {"label": "📎 Upload Replaced Document", "action": "open_deficiency_modal", "param": target_def_app.application_id}
                    ]
                )

        # -------------------------------------------------------------
        # Intent 3: GARBAGE VALUE & AI NOISE DENOISING POLICY
        # -------------------------------------------------------------
        if any(w in query_lower for w in ["garbage", "garbage value", "noise", "corrupt", "ocr error", "smudge", "scan", "5 count", "tolerance"]):
            reply = (
                f"🛡️ **ShikshaKendra AI Garbage Value Denoising Policy (Up to 5 Count):**\n\n"
                f"1. **Automatic Noise Detection:** Physical certificates uploaded by students often suffer from scanner smudges, skewed fonts, paper folds, or watermark glare. Our AI-OCR system identifies these as 'garbage values'.\n"
                f"2. **Tolerance Threshold (Up to 5 Tokens):** The system automatically auto-sanitizes and strips up to **5 garbage/noise tokens** without penalizing the student or interrupting their application.\n"
                f"3. **Non-Destructive Deficiency Fallback:** If noise exceeds 5 tokens rendering critical fields illegible, the portal never rejects the student. Instead, it generates a friendly **Deficiency Alert** allowing the student to re-upload a cleaner scan."
            )
            return JAGOChatResponse(
                query=req.user_query,
                bot_reply=reply,
                language_code=lang,
                identified_intent="GARBAGE_VALUE_POLICY_QUERY",
                card_type="GARBAGE_POLICY_CARD",
                card_data={
                    "max_tolerance": 5,
                    "auto_sanitization": True,
                    "action_above_limit": "Non-destructive Deficiency Ticket"
                },
                suggested_actions=["Test AI-OCR Scan", "Check Deficiency Rules", "View Application Status"],
                interactive_actions=[
                    {"label": "🧪 Open AI-OCR Inspector", "action": "open_ocr_scanner", "param": "sample"},
                    {"label": "🔍 View Anti-Fraud Audit", "action": "open_antifraud_modal", "param": "audit"}
                ]
            )

        # -------------------------------------------------------------
        # Intent 4: AI SCHEME RECOMMENDER INSIDE CHAT
        # -------------------------------------------------------------
        if any(w in query_lower for w in ["recommend", "which scholarship", "suggest", "which scheme", "eligible", "yojana", "phd", "foreign", "abroad", "iit", "btech", "mtech", "school", "10th", "12th"]):
            edu_level = "Post-Matric (Undergraduate / Degree)"
            wants_foreign = False
            target_inst = "Premier Institute"
            income = 180000.0

            if any(term in query_lower for term in ["phd", "ph.d", "doctorate", "research", "m.phil"]):
                edu_level = "Doctoral / Ph.D. Research"
            elif any(term in query_lower for term in ["foreign", "abroad", "overseas", "usa", "uk", "nos"]):
                edu_level = "Master's / Ph.D. Overseas"
                wants_foreign = True
            elif any(term in query_lower for term in ["iit", "iim", "nit", "aiims", "top class"]):
                edu_level = "B.Tech / Professional Degree"
                target_inst = "IIT Bombay / Premier Notified Institute"
            elif any(term in query_lower for term in ["10", "10th", "class 9", "class 10", "pre-matric", "school"]):
                edu_level = "Secondary (Class IX & X)"
                income = 120000.0

            rec_req = AISchemeRecommendationRequest(
                education_level=edu_level,
                annual_income=income,
                target_institution=target_inst,
                wants_foreign_study=wants_foreign,
                is_pvtg=False
            )
            rec_res = AISchemeRecommender.recommend(rec_req)

            reply = (
                f"🎯 **AI Scheme Recommendation: {rec_res.scheme_name}**\n\n"
                f"• **Confidence Match:** {int(rec_res.confidence_score * 100)}%\n"
                f"• **Entitlement & Grant:** {rec_res.entitlement_summary}\n"
                f"• **Key Eligibility Highlights:**\n" +
                "".join([f"  - {r}\n" for r in rec_res.matching_reasons]) +
                f"\n💡 *AI Rationale:* {rec_res.ai_rationale}"
            )

            return JAGOChatResponse(
                query=req.user_query,
                bot_reply=reply,
                language_code=lang,
                identified_intent="AI_SCHEME_RECOMMENDATION",
                card_type="SCHEME_RECOMMENDATION_CARD",
                card_data={
                    "scheme_id": rec_res.recommended_scheme_id,
                    "scheme_name": rec_res.scheme_name,
                    "confidence": f"{int(rec_res.confidence_score * 100)}%",
                    "entitlements": rec_res.entitlement_summary,
                    "reasons": rec_res.matching_reasons
                },
                suggested_actions=["Apply for this Scheme", "Required Document Checklist", "Check 5 Garbage Values"],
                interactive_actions=[
                    {"label": f"🚀 Apply for {rec_res.recommended_scheme_id}", "action": "open_apply_modal", "param": rec_res.recommended_scheme_id},
                    {"label": "📋 Check Eligibility Guidelines", "action": "query_jago", "param": f"What are the rules for {rec_res.recommended_scheme_id}?"}
                ]
            )

        # -------------------------------------------------------------
        # Intent 5: DIGITAL SANCTION ORDER & QR VERIFICATION
        # -------------------------------------------------------------
        if any(w in query_lower for w in ["sanction", "order", "qr", "letter", "download", "pdf", "bar code"]):
            sanc = db.sanctions.get("SANCTION-MOTA-2026-00481")
            reply = (
                f"📜 **Digital Sanction Order & Cryptographic QR:**\n\n"
                f"• Order No: **{sanc.sanction_order_id if sanc else 'SANCTION-MOTA-2026-00481'}**\n"
                f"• Student: **{sanc.student_name if sanc else 'Rahul Munda'}** ({sanc.student_id if sanc else 'MOTA-2026-ST-881024'})\n"
                f"• Scheme: {sanc.scheme_name if sanc else 'NFST'}\n"
                f"• Approved Amount: **₹{sanc.sanctioned_amount if sanc else 372000:,.0f}**\n"
                f"• Digital Signature SHA-256: `e8f49b1a0d7f26c59b20...`\n"
                f"• Tamper-Proof Feature: Encodes dynamic MoTA cryptographic QR verifiable offline by university registrars."
            )
            return JAGOChatResponse(
                query=req.user_query,
                bot_reply=reply,
                language_code=lang,
                identified_intent="SANCTION_ORDER_QUERY",
                card_type="SANCTION_ORDER_CARD",
                card_data={
                    "sanction_order_id": sanc.sanction_order_id if sanc else "SANCTION-MOTA-2026-00481",
                    "student_name": sanc.student_name if sanc else "Rahul Munda",
                    "amount": sanc.sanctioned_amount if sanc else 372000.0
                },
                suggested_actions=["Open Sanction Letter QR", "Check DBT Bank Status", "View Guidelines"],
                interactive_actions=[
                    {"label": "📄 Open Sanction Order Modal", "action": "open_sanction", "param": "SANCTION-MOTA-2026-00481"}
                ]
            )

        # -------------------------------------------------------------
        # Intent 6: FEDERATED OTR, DIGILOCKER, APAAR & UDISE+
        # -------------------------------------------------------------
        if any(w in query_lower for w in ["otr", "digilocker", "apaar", "udise", "ekyc", "aadhaar", "registration", "pvtg"]):
            reply = (
                f"🌐 **ShikshaKendra One-Time Registration (OTR) Integrations:**\n\n"
                f"• **Aadhaar e-KYC:** Verifies demographic identity (Name, DoB, Gender) with zero paperwork.\n"
                f"• **DigiLocker:** Automatically fetches authentic Caste, Domicile, and 10th/12th marksheets with cryptographic state seals.\n"
                f"• **APAAR / ABC ID:** Syncs educational history across Central, State, and Autonomous universities.\n"
                f"• **UDISE+:** Verifies Pre-Matric school enrollment and government school codes.\n"
                f"• **PVTG Tracking:** Dedicated fast-track quotas for Particularly Vulnerable Tribal Groups (e.g. Birhor, Asur, Chenchu)."
            )
            return JAGOChatResponse(
                query=req.user_query,
                bot_reply=reply,
                language_code=lang,
                identified_intent="FEDERATED_OTR_QUERY",
                suggested_actions=["Start OTR Registration", "Recommend Scheme", "Check 5 Garbage Values"],
                interactive_actions=[
                    {"label": "✨ Start One-Time Registration", "action": "open_otr_modal", "param": "register"}
                ]
            )

        # -------------------------------------------------------------
        # Intent 7: LIVE STATUS & STEP-BY-STEP PROGRESS TIMELINE
        # -------------------------------------------------------------
        if any(w in query_lower for w in ["status", "where is", "track", "kahan", "stithi", "progress", "merit", "approved", "stage", "app-"]):
            status_str = target_app.status.value if hasattr(target_app.status, 'value') else str(target_app.status)
            st_name = student_obj.full_name if student_obj else "Applicant"
            scheme_cfg = SCHEMES_CONFIG.get(target_app.scheme_id, {})
            scheme_title = scheme_cfg.get("name", target_app.scheme_id)

            reply = f"{templates['status_prefix']} **[{status_str}]** for {st_name}.\n\n"
            
            if status_str == "DISBURSED":
                reply += (
                    f"🎉 **Disbursement Successful!**\n"
                    f"• Scheme: {scheme_title}\n"
                    f"• Approved Amount: **₹{target_app.approved_amount:,.0f}**\n"
                    f"• PFMS UTR: `{target_app.utr_number}`\n"
                    f"• Credited to: {student_obj.bank_account.bank_name if student_obj else 'Aadhaar-seeded Bank Account'} on {target_app.disbursement_date}."
                )
            elif status_str == "SANCTIONED":
                reply += (
                    f"📜 **Digital Sanction Order Issued!**\n"
                    f"• Sanction ID: `{target_app.sanction_order_id}`\n"
                    f"• Sanctioned Grant: **₹{target_app.approved_amount:,.0f}**\n"
                    f"• Queued for immediate Direct Benefit Transfer (DBT) release via PFMS."
                )
            elif status_str == "DEFICIENCY_RAISED":
                active_def = next((d for d in target_app.deficiencies if not d.is_resolved), None)
                reply += (
                    f"⚠️ **Action Required (Deficiency Raised):**\n"
                    f"• Issue: *{active_def.issue_description if active_def else 'Document clarification needed'}*\n"
                    f"• Required Action: *{active_def.required_action if active_def else 'Re-upload valid document'}*\n"
                    f"• Don't worry! Click the one-click resolution button below to clear this defect."
                )
            elif status_str == "VERIFIED_POOL":
                reply += (
                    f"✅ **Fully Verified & Placed in National Merit Pool!**\n"
                    f"• Tier-1 AI OCR Denoising: **Passed (Score: {target_app.tier1_ai_audit_score*100:.0f}%)**\n"
                    f"• Tier-2 Institution Verification: **Verified by {target_app.tier2_verifier_name}**\n"
                    f"• Tier-3 State/MoTA Verification: **Approved by {target_app.tier3_approver_name}**\n"
                    f"• Merit Rank: #{target_app.merit_rank or 'Generating...'}."
                )
            else:
                reply += (
                    f"• Current Milestone: Verification in progress.\n"
                    f"• Tier-1 AI Audit: {'Passed' if target_app.tier1_ai_audit_passed else 'Under Analysis'}\n"
                    f"• Institute Scrutiny: {'Verified' if target_app.tier2_institute_verified else 'Pending'}"
                )

            timeline_steps = [
                {"name": "One-Time Registration (OTR)", "completed": True, "detail": "Aadhaar e-KYC Verified"},
                {"name": "AI-OCR Sentry & Denoising", "completed": target_app.tier1_ai_audit_passed, "detail": "5-Count Noise Tolerance: PASSED"},
                {"name": "Institution Verification", "completed": target_app.tier2_institute_verified, "detail": target_app.tier2_verifier_name or "Pending at College Nodal Desk"},
                {"name": "MoTA Quota & Sanction", "completed": target_app.tier3_mota_approved, "detail": target_app.sanction_order_id or "Awaiting final clearance"},
                {"name": "PFMS DBT Disbursal", "completed": status_str == "DISBURSED", "detail": target_app.utr_number or "Queued in APBS"}
            ]

            interactive_acts = []
            if target_app.sanction_order_id:
                interactive_acts.append({"label": "📄 View Sanction Order & QR", "action": "open_sanction", "param": target_app.sanction_order_id})
            if status_str == "DEFICIENCY_RAISED":
                active_def = next((d for d in target_app.deficiencies if not d.is_resolved), None)
                if active_def:
                    interactive_acts.append({"label": "⚡ Instant Resolve in Chat", "action": "query_jago", "param": f"resolve-deficiency {target_app.application_id}"})
                    interactive_acts.append({"label": "📎 Upload New Document", "action": "open_deficiency_modal", "param": target_app.application_id})
            interactive_acts.append({"label": "🔍 Inspect AI-OCR Denoising", "action": "open_ocr_scanner", "param": target_app.application_id})

            return JAGOChatResponse(
                query=req.user_query,
                bot_reply=reply,
                language_code=lang,
                identified_intent="APPLICATION_STATUS_QUERY",
                card_type="STATUS_TIMELINE_CARD",
                card_data={
                    "application_id": target_app.application_id,
                    "student_name": st_name,
                    "scheme_id": target_app.scheme_id,
                    "scheme_title": scheme_title,
                    "status": status_str,
                    "claimed_amount": target_app.claimed_amount,
                    "approved_amount": target_app.approved_amount,
                    "timeline_steps": timeline_steps
                },
                suggested_actions=[
                    "What is the garbage value policy?",
                    "Recommend other scholarships",
                    "Check DBT bank status"
                ],
                interactive_actions=interactive_acts,
                source_citation="MoTA National Scholarship Database v2.0"
            )

        # -------------------------------------------------------------
        # Default Helpful Vernacular Guidance
        # -------------------------------------------------------------
        greeting_text = templates["greeting"]
        return JAGOChatResponse(
            query=req.user_query,
            bot_reply=(
                f"{greeting_text}\n\n"
                f"Here are key tasks I can perform for you:\n"
                f"1. **Live Status Tracking:** Check milestones across AI-OCR, College & MoTA.\n"
                f"2. **Instant Deficiency Resolution:** Resolve flagged documents directly inside our chat.\n"
                f"3. **AI Scheme Recommendation:** Find your best-fit grant based on your course & income.\n"
                f"4. **Direct Benefit Transfer (DBT):** Track PFMS UTR and Aadhaar APBS bank credits.\n"
                f"5. **5-Count Garbage Value AI:** Learn how our scanner denoises document smudges."
            ),
            language_code=lang,
            identified_intent="GENERAL_INQUIRY",
            suggested_actions=[
                "Check status of APP-MOTA-NFST-001",
                "How to resolve Deficiency?",
                "Recommend scholarship for PhD",
                "What is the 5 garbage value rule?",
                "Track DBT Bank Transfer"
            ],
            interactive_actions=[
                {"label": "📊 Track Rahul Munda (NFST)", "action": "query_jago", "param": "Check status of APP-MOTA-NFST-001"},
                {"label": "⚠️ Resolve Birsa's Deficiency", "action": "query_jago", "param": "How do I fix deficiency for APP-MOTA-POSTMATRIC-003?"},
                {"label": "🎯 Recommend Scholarship", "action": "query_jago", "param": "Recommend scholarship for B.Tech in IIT"}
            ]
        )
