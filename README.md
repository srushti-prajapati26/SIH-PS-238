Live Website: https://srushti-prajapati26.github.io/SIH-PS-238/

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
🚀 Method 1 — Flutter App Run Karna
Step 1: Project folder open karo
Sabse pehle apna Flutter project jis folder mein hai, usko locate karo.

Example:
C:\Users\YourName\Desktop\VidyaSetu
Project ke andar normally ye files/folders hone chahiye:
VidyaSetu/
├── android/
├── ios/
├── lib/
├── web/
├── pubspec.yaml
└── ...
Important: pubspec.yaml jis folder mein hai, wahi tumhara main Flutter project folder hai.

Step 2: VS Code mein project open karo
VS Code kholo
File → Open Folder
Aur apna project folder select karo.
Step 3: Terminal open karo
VS Code mein:
Terminal → New Terminal
Ya shortcut:
Ctrl + `
Terminal mein check karo ki tum project folder ke andar ho.

For example:
PS C:\Users\YourName\Desktop\VidyaSetu>
Agar project folder mein nahi ho, to:
cd "C:\Users\YourName\Desktop\VidyaSetu"

Step 4: Packages download karo
Terminal mein ye command run karo:
flutter pub get
Wait karo jab tak command complete nahi hoti.
Agar successful hua to Flutter dependencies/packages download ho jayenge.
Step 5: Flutter devices check karo
flutter devices
-----------------------------------------------------------------------------------------------
# Fetch packages
flutter pub get

# Run on connected device or emulator
flutter run
```
Step 7: Agar mobile mein run karna hai
Apna Android phone laptop se USB cable se connect karo.
Phone mein:
Settings → Developer Options → USB Debugging → ON
Phir terminal mein:
"flutter devices"
Agar tumhara phone list mein aa gaya, toh:
"flutter run"
Bas! App phone mein run ho jayegi. ✅
### 2. Standalone Interactive Live Simulation
You can open `web_preview/index.html` in any web browser to interactively test the complete 6-stage lifecycle, JAGO Chatbot, and Unreached Beneficiaries discovery engine immediately:
```bash
# Open directly in default browser on Windows
  
