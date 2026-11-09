# Datasets for EduPredict (BUSE tertiary project)

## 1) Synthetic BUSE demo dataset (used now)
- **Location:** `ml/data/sample/buse/`
- **Type:** Synthetic, generated for this prototype (no real students).
- **Files:** `departments.csv`, `programmes.csv`, `courses.csv`, `academic_periods.csv`, `students.csv`, `enrolments.csv`, `attendance.csv`, `assessments.csv`, `lms_activity.csv`, `outcomes_training.csv`.
- **Target use:** end-to-end demo of import, validation, analytics, ML training/prediction, recommendations, and reports.
- **Important:** Do **not** present as real Bindura University of Science Education data. Real use requires institutional permission, ethics clearance (if required), and data-protection compliance.

## 2) Datasets we could have used (public / research)
Use only with license/ethics compliance; most require mapping to BUSE’s schema.

| Dataset | Source | What it contains | Why useful | Limitations |
|---|---|---|---|---|
| **Open University Learning Analytics Dataset (OULAD)** | Open University / UCI/Kaggle mirrors | VLE clicks, assessments, registrations, demographics, final results (~32k students, 7 courses) | Strong for LMS engagement + assessment + pass/fail; widely used in EDM/LA research (and similar to Choi et al. 2026 context) | UK distance-learning context; schema differs from BUSE SIS; anonymized/public release terms apply |
| **UCI Student Performance** (Cortez & Silva) | UCI ML Repository | Portuguese secondary school students, grades G1-G3, demographics, study/social factors | Good small benchmark for regression/classification; easy to prototype | Secondary school (not tertiary), Portugal context, small, includes sensitive attributes—use fairness care |
| **UCI Higher Education Students Performance** / related variants | UCI / community | Tertiary/college performance attributes (varies by version) | Closer to higher-ed setting | Verify provenance/version, missing LMS/attendance richness, context mismatch |
| **Kaggle “Students Performance in Exams” / “xAPI-Edu-Data”** | Kaggle | Exam scores/demographics or xAPI classroom features | Quick demos, feature engineering practice | Often small/synthetic-like, limited institutional process fields, license/quality varies |
| **ASSISTments** (selected releases) | ASSISTments / learning platforms | Tutoring/assignment interactions and outcomes | Rich behavioral/interaction data | K-12/tutoring focus; access terms may apply |
| **Institutional SIS/LMS extracts (BUSE)** | BUSE (authorized) | Real demographics, enrolment, attendance, CA, LMS, outcomes | Best validity for BUSE deployment | Requires permission, ethics, privacy safeguards, data-sharing agreement |

## 3) Recommended approach
1. **Now (tertiary project):** synthetic BUSE-shaped data + transparent evaluation.
2. **Benchmarking (optional):** replicate pipeline on **OULAD** or **UCI Student Performance** with clear schema mapping and licensing notes.
3. **Pilot/production:** approved BUSE historical extracts, temporal validation, fairness monitoring, and staff-reviewed intervention rules.
