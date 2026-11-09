"""Data import and quality models"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base, TimestampMixin


class DataImport(Base, TimestampMixin):
    """Track data import operations"""
    __tablename__ = "data_imports"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(20), nullable=False)  # csv, excel
    file_size = Column(Integer, default=0)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="processing")  # processing, completed, failed
    total_rows = Column(Integer, default=0)
    accepted_rows = Column(Integer, default=0)
    rejected_rows = Column(Integer, default=0)
    warning_rows = Column(Integer, default=0)
    error_message = Column(Text)
    data_quality_report = Column(JSON)

    uploader = relationship("User")
    quality_issues = relationship("DataQualityIssue", back_populates="data_import")


class DataQualityIssue(Base, TimestampMixin):
    """Track data quality issues found during import"""
    __tablename__ = "data_quality_issues"

    id = Column(Integer, primary_key=True, index=True)
    data_import_id = Column(Integer, ForeignKey("data_imports.id"), nullable=False)
    row_number = Column(Integer, nullable=False)
    column_name = Column(String(100))
    issue_type = Column(String(50), nullable=False)  # invalid_format, missing_value, duplicate, out_of_range, etc.
    severity = Column(String(20), nullable=False)  # error, warning
    description = Column(Text, nullable=False)
    suggested_fix = Column(Text)
    is_resolved = Column(Boolean, default=False)

    data_import = relationship("DataImport", back_populates="quality_issues")


class PredictionRun(Base, TimestampMixin):
    """Track prediction model runs"""
    __tablename__ = "prediction_runs"

    id = Column(Integer, primary_key=True, index=True)
    model_version = Column(String(50), nullable=False)
    checkpoint = Column(String(20), nullable=False)  # week_0, week_4, week_8, week_12
    period_id = Column(Integer, ForeignKey("academic_periods.id"), nullable=False)
    status = Column(String(20), default="running")  # running, completed, failed
    total_predictions = Column(Integer, default=0)
    high_risk_count = Column(Integer, default=0)
    medium_risk_count = Column(Integer, default=0)
    low_risk_count = Column(Integer, default=0)
    execution_time_seconds = Column(Integer, default=0)
    error_message = Column(Text)
    run_metadata = Column("metadata", JSON)

    predictions = relationship("StudentPrediction", back_populates="prediction_run")


class StudentPrediction(Base, TimestampMixin):
    """Individual student risk predictions"""
    __tablename__ = "student_predictions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    prediction_run_id = Column(Integer, ForeignKey("prediction_runs.id"), nullable=False)
    period_id = Column(Integer, ForeignKey("academic_periods.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    checkpoint = Column(String(20), nullable=False)
    risk_probability = Column(Float, nullable=False)
    risk_band = Column(String(20), nullable=False)  # high, medium, low
    predicted_outcome = Column(String(20))  # pass, fail
    confidence_score = Column(Float, default=0.0)
    model_version = Column(String(50), nullable=False)

    student = relationship("Student", back_populates="predictions")
    prediction_run = relationship("PredictionRun", back_populates="predictions")
    period = relationship("AcademicPeriod", back_populates="predictions")
    course = relationship("Course")
    explanations = relationship("PredictionExplanation", back_populates="prediction")
    recommendations = relationship("Recommendation", back_populates="prediction")


class PredictionExplanation(Base, TimestampMixin):
    """SHAP-based explanations for predictions"""
    __tablename__ = "prediction_explanations"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, ForeignKey("student_predictions.id"), nullable=False)
    feature_name = Column(String(100), nullable=False)
    feature_value = Column(Float)
    shap_value = Column(Float, nullable=False)
    impact = Column(String(20))  # positive, negative, neutral
    description = Column(Text)

    prediction = relationship("StudentPrediction", back_populates="explanations")