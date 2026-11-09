"""Database models for EduPredict"""

from app.models.base import Base, TimestampMixin
from app.models.user import User, Role, UserRole
from app.models.academic import (
    Programme, Department, Course, AcademicPeriod,
    Student, CourseEnrolment, AcademicHistory,
)
from app.models.engagement import (
    AttendanceRecord, AssessmentRecord, LMSActivity
)
from app.models.data import (
    DataImport, DataQualityIssue, PredictionRun,
    StudentPrediction, PredictionExplanation
)
from app.models.recommendation import (
    RecommendationRule, Recommendation, Intervention,
    InterventionFollowup
)
from app.models.report import ReportJob
from app.models.audit import AuditLog
from app.models.assignment import CourseStaffAssignment, AdvisorAssignment

__all__ = [
    "Base", "TimestampMixin",
    "User", "Role", "UserRole",
    "Programme", "Department", "Course", "AcademicPeriod",
    "Student", "CourseEnrolment", "AcademicHistory",
    "AttendanceRecord", "AssessmentRecord", "LMSActivity",
    "DataImport", "DataQualityIssue", "PredictionRun",
    "StudentPrediction", "PredictionExplanation",
    "RecommendationRule", "Recommendation", "Intervention",
    "InterventionFollowup", "ReportJob", "AuditLog",
    "CourseStaffAssignment", "AdvisorAssignment"
]