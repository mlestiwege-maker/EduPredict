"""Pydantic schemas for API requests and responses"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


# Authentication schemas
class UserLogin(BaseModel):
    email: str
    password: str


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    role_id: Optional[int] = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    roles: List[str] = []
    permissions: Dict[str, bool] = {}

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# Academic structure schemas
class DepartmentResponse(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class ProgrammeResponse(BaseModel):
    id: int
    name: str
    code: str
    department_id: int
    level: Optional[str] = None
    duration_years: int = 4
    is_active: bool = True

    class Config:
        from_attributes = True


class CourseResponse(BaseModel):
    id: int
    code: str
    name: str
    department_id: int
    credits: int = 5
    level: Optional[str] = None
    is_active: bool = True

    class Config:
        from_attributes = True


class AcademicPeriodResponse(BaseModel):
    id: int
    year: int
    semester: str
    term_start: Optional[datetime] = None
    term_end: Optional[datetime] = None
    is_active: bool = False

    class Config:
        from_attributes = True


# Student schemas
class StudentResponse(BaseModel):
    id: int
    pseudonym: str
    programme_id: int
    year_of_study: int = 1
    enrollment_status: str = "Active"
    age_band: Optional[str] = None
    gender: Optional[str] = None
    residence_type: Optional[str] = None
    funding_type: Optional[str] = None

    class Config:
        from_attributes = True


class StudentProfileResponse(BaseModel):
    student: StudentResponse
    academic_history: List[Dict[str, Any]] = []
    current_enrolments: List[Dict[str, Any]] = []
    predictions: List[Dict[str, Any]] = []
    interventions: List[Dict[str, Any]] = []


# Prediction schemas
class PredictionResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    period_id: int
    checkpoint: str
    risk_probability: float
    risk_band: str
    predicted_outcome: Optional[str] = None
    confidence_score: float = 0.0
    model_version: str
    explanations: List[Dict[str, Any]] = []

    class Config:
        from_attributes = True


class RiskSummary(BaseModel):
    total_students: int
    high_risk: int
    medium_risk: int
    low_risk: int
    risk_distribution: Dict[str, int]


# Recommendation schemas
class RecommendationResponse(BaseModel):
    id: int
    student_id: int
    prediction_id: int
    action: str
    responsible_role: Optional[str] = None
    priority: str = "medium"
    status: str = "pending"
    staff_notes: Optional[str] = None

    class Config:
        from_attributes = True


class InterventionCreate(BaseModel):
    student_id: int
    recommendation_id: Optional[int] = None
    intervention_type: str
    description: str
    action_taken: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    notes: Optional[str] = None


class InterventionResponse(BaseModel):
    id: int
    student_id: int
    recommendation_id: Optional[int] = None
    staff_id: int
    intervention_type: str
    description: str
    action_taken: Optional[str] = None
    status: str = "planned"
    start_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    follow_up_date: Optional[datetime] = None
    outcome: Optional[str] = None
    effectiveness_rating: Optional[int] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


# Report schemas
class ReportRequest(BaseModel):
    report_type: str
    report_format: str
    period_id: Optional[int] = None
    department_id: Optional[int] = None
    course_id: Optional[int] = None
    programme_id: Optional[int] = None
    year_of_study: Optional[int] = None


class ReportResponse(BaseModel):
    id: int
    report_type: str
    report_format: str
    title: str
    status: str
    file_path: Optional[str] = None
    generated_at: Optional[datetime] = None


# Data import schemas
class DataImportResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    status: str
    total_rows: int
    accepted_rows: int
    rejected_rows: int
    warning_rows: int
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


class DataQualityIssueResponse(BaseModel):
    id: int
    data_import_id: int
    row_number: int
    column_name: Optional[str] = None
    issue_type: str
    severity: str
    description: str
    suggested_fix: Optional[str] = None
    is_resolved: bool = False

    class Config:
        from_attributes = True


# Analytics schemas
class CourseAnalytics(BaseModel):
    course_id: int
    course_code: str
    course_name: str
    total_enrolled: int
    average_mark: Optional[float] = None
    pass_rate: Optional[float] = None
    fail_rate: Optional[float] = None
    average_attendance: Optional[float] = None
    high_risk_count: int = 0
    medium_risk_count: int = 0
    low_risk_count: int = 0


class DashboardSummary(BaseModel):
    total_students: int
    total_courses: int
    total_predictions: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    overall_pass_rate: Optional[float] = None
    courses: List[CourseAnalytics] = []