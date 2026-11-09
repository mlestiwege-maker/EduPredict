# EduPredict — Student Academic Performance Prediction System

An AI data-driven academic performance prediction and early-warning system for higher and tertiary education institutions, targeting Bindura University of Science Education (BUSE).

## Overview

EduPredict is a comprehensive system that:
- Imports and validates student academic records
- Analyzes academic performance patterns
- Predicts students at risk of underperformance using machine learning
- Explains predictions with SHAP
- Generates role-based recommendations and interventions
- Provides dashboards and reports for different institutional roles

## Features

### Core Modules
1. **Student Data Upload & Integration** - Secure file upload with validation
2. **Academic Performance Analysis** - Descriptive analytics and predictive modeling
3. **Management Dashboards & Reports** - Role-based reporting
4. **Recommendation & Intervention Management** - Actionable academic support

### User Roles
- System Administrator
- Lecturer
- Academic Advisor
- Head of Department
- Dean
- Registry Staff

## Technology Stack

- **Frontend**: React + TypeScript + Vite + Tailwind CSS
- **Backend**: Python + FastAPI
- **Database**: PostgreSQL
- **Machine Learning**: Scikit-learn, XGBoost, SHAP
- **Authentication**: Secure token-based auth
- **Reports**: ReportLab (PDF), openpyxl (Excel)

## Project Structure

```
EduPredict/
├── frontend/           # React application
├── backend/            # FastAPI application
├── ml/                 # Machine learning pipeline
├── docs/               # Documentation
├── scripts/            # Utility scripts
└── tests/              # Test files
```

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Docker (optional)

### Installation

1. **Backend Setup**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Frontend Setup**
```bash
cd ../frontend
npm install
```

3. **Database Setup**
```bash
docker-compose up -d
```

4. **Run the Application**
```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend
cd ../frontend
npm run dev

# Just One-Command Script
cd /home/mufutumari/Desktop/EduPredict
./START.sh
```


## Usage

See the documentation in `/docs` for detailed usage instructions.

## Important Notes

- This is a prototype using synthetic data for demonstration purposes
- Real institutional data requires appropriate permissions and ethical clearance
- The system supports human decision-making; predictions are estimates, not verdicts

## License

Academic project - see institutional guidelines for use.