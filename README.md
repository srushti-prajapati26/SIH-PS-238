# Vidya Setu: Scholarship Support for Tribal Students
### Ministry of Tribal Affairs (MoTA), Government of India
> **One App | Five Schemes | Single View | Seamless Verification | Direct Benefit Transfer**  
> *"Ensuring no ST student is left behind"*

---

## 🏛️ Project Architecture Overview

Vidya Setu brings scholarship discovery, applications, document guidance, and payment tracking together for tribal students across India:

```
                             ST STUDENT (Beneficiary)
                                        │
                  ┌─────────────────────┴─────────────────────┐
                  ▼                                           ▼
        [Mobile App Registration]                     [Proactive Outreach]
        • OTR / Aadhaar OTP                           • UDISE+ / APAAR / OTR
        • Biometric / eKYC                            • Unreached ST Identifier
                  │                                   • Targeted SMS / IVR
                  ▼                                           │
        [Unified Student Profile] ◄───────────────────────────┘
        • ST / PVTG Status
        • Academic (UDISE+ / APAAR / AISHE)
        • Income & Domicile
        • Bank Details (Aadhaar Seeded)
                  │
                  ▼
        [5-Scheme Eligibility Engine]
        • Pre-Matric (Class 9-10)
        • Post-Matric (Class 11 - PG)
        • Top Class (IITs/IIMs/AIIMS/NITs)
        • NFST (M.Phil / Ph.D. Fellowship)
        • NOS (Foreign Universities)
                  │
                  ▼
        [Digital Document Wallet] (DigiLocker)
        • Zero duplicate re-scans
        • Issuer cryptographic verification
                  │
                  ▼
        [Application Submission]
                  │
        ┌─────────┴───────────────────────────────────────┐
        ▼                                                 ▼
┌──────────────────────────────────────────┐ ┌──────────────────────────────────────┐
│  Unified Verification & Integration      │ │  JAGO Multilingual AI Assistant      │
│  Layer (7 Government API Connectors)     │ │  • Natural language voice & text     │
│  • UIDAI         • DigiLocker            │ │  • Scheme recommendations            │
│  • UDISE+        • APAAR / ABC ID        │ │  • Live status query & deficiencies  │
│  • AISHE         • State e-District      │ │  • Multilingual translation          │
│  • UGC-NTA       • PFMS                  │ └──────────────────────────────────────┘
└──────────────────┬───────────────────────┘
                   │
           ┌───────┴───────┐
           ▼               ▼
      [MATCH]         [MISMATCH / EXCEPTION]
      Automated       • Deficiency Notice
      Verification    • Correction / Manual Review
           │               │
           └───────┬───────┘
                   ▼
     [Institution Verification] (College/School)
                   │
                   ▼
     [Department / MoTA Review] (Final Approval)
                   │
                   ▼
     [Sanction Order Generation]
                   │
                   ▼
     [PFMS / DBT Payment Processing]
                   │
                   ▼
     [Student Bank Account Credit via DBT]
                   │
                   ▼
     [Consolidated Student Dashboard]
```

---

## 🌟 The 5 Flagship MoTA Schemes

1. **Pre-Matric Scholarship for ST Students**:
   - Classes 9 and 10 in recognized schools.
   - Income ceiling: $\le \text{₹2,50,000/yr}$.
   - Grants: ₹3,500 – ₹7,000/yr + ad-hoc allowance.
2. **Post-Matric Scholarship for ST Students**:
   - Class 11 through Post-Graduation.
   - Income ceiling: $\le \text{₹2,50,000/yr}$ (*Relaxable for PVTG*).
   - Covers compulsory course fees + maintenance allowances up to ₹13,500/yr.
3. **National Scholarship for Higher Education (Top Class Scheme)**:
   - For ST students admitted into notified premier institutes (IITs, IIMs, NITs, AIIMS, NLUs).
   - Income ceiling: $\le \text{₹6,00,000/yr}$.
   - Benefits: Full tuition fees + ₹3,000/month living + ₹45,000 one-time computer grant + ₹5,000/year books.
4. **National Fellowship for Higher Education of ST Students (NFST)**:
   - Regular M.Phil and Ph.D. research in Indian universities.
   - Requirement: UGC-NET / CSIR-NET / JRF qualified.
   - Benefits: JRF @ ₹37,000/mo + SRF @ ₹42,000/mo + HRA + contingency.
5. **National Overseas Scholarship (NOS)**:
   - Master’s and Ph.D. in accredited QS Top 500 foreign universities.
   - Income ceiling: $\le \text{₹8,00,000/yr}$.
   - Benefits: Full foreign tuition + annual maintenance (£9,900 / $15,400) + airfare + visa.

---

## 🛠️ Unified Verification Layer (7 API Connectors)

- **UIDAI**: Identity verification and demographic Aadhaar eKYC.
- **DigiLocker**: Verifiable credentials with digital signatures of issuers.
- **UDISE+**: School registration and pupil enrollment verification.
- **APAAR**: Academic Bank of Credits ID and verifiable academic transcripts.
- **AISHE**: Higher education institution recognition and course accreditation.
- **State e-District**: Real-time validation of ST/PVTG caste certificates and income certificates.
- **UGC-NTA**: Roll number validation for NET/JRF examination scores.
- **PFMS**: NPCI bank account Aadhaar-seeding mapper for Direct Benefit Transfer.

---

## 📱 How to Run

### 1. Flutter Mobile App (Android / iOS / Web / Desktop)
```bash
# Navigate to the project directory
cd "C:\Users\SHUBHAM JHA\.gemini\antigravity\scratch\mota_unified_scholarship"

# Fetch packages
flutter pub get

# Run on connected device or emulator
flutter run
```

### 2. Standalone Interactive Live Simulation
You can open `web_preview/index.html` in any web browser to interactively test the complete 6-stage lifecycle, JAGO Chatbot, and Unreached Beneficiaries discovery engine immediately:
```bash
# Open directly in default browser on Windows
Start-Process "C:\Users\SHUBHAM JHA\.gemini\antigravity\scratch\mota_unified_scholarship\web_preview\index.html"
```
