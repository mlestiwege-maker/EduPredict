# EduPredict — Run Guide (Kali, local)

## Quick start
```bash
cd ~/Desktop/EduPredict
./START_EDUPREDICT.sh
```
Open: http://localhost:3000

## Manual start
Backend (must run from `backend/` because default DB is `sqlite:///./edupredict.db`):
```bash
cd ~/Desktop/EduPredict/backend
./venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
Frontend:
```bash
cd ~/Desktop/EduPredict/frontend
npm run dev -- --host 127.0.0.1 --port 3000
```

## Demo accounts (all roles)
| Role | Email | Password |
|---|---|---|
| System Administrator | admin@edupredict.com | admin123 |
| Lecturer | lecturer@edupredict.com | lecturer123 |
| Academic Advisor | advisor@edupredict.com | advisor123 |
| Head of Department | hod@edupredict.com | hod123 |
| Dean | dean@edupredict.com | dean123 |
| Registry Staff | registry@edupredict.com | registry123 |

## First-use workflow (makes buttons/features active)
1. **Data Imports** → `Load Synthetic BUSE Dataset` (loads `ml/data/sample/buse/*`).
2. **Model Management** → `Run Predictions (week_4, period 2)` (trains/selects ML model and persists predictions).
3. **Risk Monitoring** → view at-risk students (High/Medium/Low).
4. **Recommendations** → view rule-based actions; staff reviews/approves in real deployment.
5. **Reports** → `Generate Excel` → `Download` (downloads Excel file with predictions).
6. **Student Records / Academic Analytics** → populated from loaded synthetic data.

## Report download fix
Reports now download correctly. Click **Download** on any generated report; the browser will save an Excel (`.xlsx`) file. All reports include a disclaimer that predictions are decision-support estimates, not verdicts.

## Data
- Synthetic BUSE demo data: `ml/data/sample/buse/` (300 students, 696 enrolments, attendance/assessments/LMS, training outcomes). **Not real BUSE data.**
- Public datasets considered (see `docs/datasets/DATASETS.md`): OULAD, UCI Student Performance (Cortez & Silva), UCI Higher Education Students Performance, xAPI-Edu-Data/Kaggle sets. Use only under license/ethics and schema mapping.

## ML
- `ml/run_ml.py` trains/compares 6 classifiers (Logistic Regression, Decision Tree, Random Forest, SVM, Gradient Boosting, MLP) using checkpoint-safe features, group split, recall-oriented threshold, and saves reports in `ml/reports/`.
- XGBoost/SHAP libraries are not installed in the backend venv on this machine; the runtime uses sklearn Gradient Boosting and lightweight importance-based explanations. Install XGBoost/SHAP in the venv for the full stack when disk space is available.
- Results are **synthetic-demo decision support**, not verdicts. Validate on approved BUSE data (temporal holdout, no leakage, calibration, fairness).

## Notes
- Backend default DB: `sqlite:///./edupredict.db` (run backend from `backend/`). For pilot/production, move to PostgreSQL + Alembic + HTTPS + hardened secrets/RBAC scoping.
- Disk is ~95% full; avoid large Docker/model downloads until space is freed.
- Downloads work through the frontend API with proper authentication headers.
