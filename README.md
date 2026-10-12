# MoTA AI-Enabled Scholarship & Fellowship Management System
### Smart India Hackathon (SIH PS 26239)

> **Ministry of Tribal Affairs (MoTA), Government of India**  
> An end-to-end AI-powered digital ecosystem integrating One-Time Registration (OTR), AI-OCR document forensics, a Configurable Business Rules Engine (BRE), 3-Tier Multi-Level Verification, Algorithmic Merit Ranking, Digital Sanction Orders, Direct Benefit Transfer (DBT) via PFMS/NPCI, and 24/7 vernacular assistance via the JAGO AI Chatbot.

---

## 🌟 Key Architecture & Capabilities

1. **Phase 1: Registration & Profile Creation (OTR)**
   - Aadhaar e-KYC demo integration
   - Automated DigiLocker caste & domicile verification (ST/PVTG classification)
   - APAAR / ABC (Academic Bank of Credits) and UDISE+ school verification
   - PFMS bank account & NPCI Aadhaar-seeding validation
   - Unique Student Identifier (USI) generation

2. **Phase 2: Smart Application & AI-OCR Processing**
   - Scheme support: Pre-Matric, Post-Matric, Top Class Premier Institutes, NFST (Ph.D.), NOS (Overseas)
   - 80% form fields auto-populated from Golden Profile
   - AI-OCR extraction (PaddleOCR / TrOCR simulation)
   - SHA-256 document hashing and Error Level Analysis (ELA) tamper detection
   - Phonetic/Fuzzy string distance matching (Levenshtein $\ge 0.85$)

3. **Phase 3: Rules Engine & 3-Tier Verification**
   - Configurable Business Rules Engine (BRE) evaluating income ceilings, quotas, and marks
   - **Tier 1 – AI Audit**: Immediate instant check for duplicate certs, inconsistencies, and synthetic identities
   - **Tier 2 – Educational Institution (INO Desk)**: College validates admission, roll number, and tuition fees
   - **Tier 3 – State Agency / MoTA (SNO Desk)**: Quota and final statutory approval
   - **Deficiency Loop**: Non-blocking correction cycle; multi-channel alerts (SMS/WhatsApp/JAGO Bot)

4. **Phase 4: Selection & Merit List Generation**
   - Scheme-specific scoring:
     - **NFST**: Research proposal rubric + NET/GATE percentile
     - **NOS**: QS World University Rank tiering + IELTS/GRE score
     - **Post/Pre-Matric**: Income inverse weighting + Academic score + PVTG priority
   - Digital Sanction Order generation with cryptographic signature and QR verification

5. **Phase 5: DBT & Payment Processing**
   - Direct Benefit Transfer pipeline: $\text{Digital Sanction} \rightarrow \text{PFMS} \rightarrow \text{NPCI APBS} \rightarrow \text{Student Bank Account}$
   - UTR number issuance and real-time status tracking

6. **Cross-Cutting Engines**
   - **JAGO AI Chatbot**: Multilingual vernacular assistance (Hindi, English, Santhali, Gondi, Odia, etc.)
   - **Anti-Fraud Sentry**: Cross-NSP dual benefit check, duplicate hash collision scanner
   - **Executive Analytics**: Real-time KPI aggregation, processing velocity, and disbursement tracking

---

## 🚀 How to Run the Application

### 1. Prerequisites
- Python 3.10+ installed
- Dependencies: `pip install -r requirements.txt`

### 2. Start the Server
Run the runner script:
```bash
python run_server.py
```

### 3. Open the UI Frame
Open your browser at:
- **Interactive Portal Frame**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc API Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📂 Project Directory Structure

```
sih_scholarship_portal/
├── app/
│   ├── api/
│   │   ├── routes.py             # 13 REST API endpoints covering all 5 phases
│   ├── services/
│   │   ├── federated_service.py  # Aadhaar, DigiLocker, APAAR, PFMS simulator
│   │   ├── ocr_service.py        # AI-OCR, fuzzy matching & ELA tamper analysis
│   │   ├── rules_engine.py       # Configurable scheme eligibility engine
│   │   ├── verification_service.py # 3-Tier verification & deficiency loop
│   │   ├── merit_service.py      # Scheme-specific merit scoring algorithms
│   │   ├── dbt_service.py        # Digital sanction & PFMS/NPCI payment
│   │   ├── jago_bot_service.py   # JAGO multilingual AI chatbot service
│   │   ├── antifraud_service.py  # Fraud sentry & hash collision detector
│   │   └── analytics_service.py  # Real-time analytics KPI aggregation
│   ├── static/
│   │   └── index.html            # Complete Single-Page UI Application Frame
│   ├── config.py                 # Scheme parameters, income limits & languages
│   ├── database.py               # Memory/JSON store pre-seeded with demo records
│   ├── models.py                 # Pydantic data schemas
│   └── main.py                   # FastAPI application initialization
├── run_server.py                 # Server startup script
├── requirements.txt              # Project dependencies
└── README.md                     # Documentation
```
