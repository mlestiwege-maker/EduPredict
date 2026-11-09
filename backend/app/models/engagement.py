"""Attendance, assessment, and LMS activity models"""

from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, Text, Time, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base, TimestampMixin


class AttendanceRecord(Base, TimestampMixin):
    """Student attendance records"""
    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    period_id = Column(Integer, ForeignKey("academic_periods.id"), nullable=False, index=True)
    sessions_scheduled = Column(Integer, default=0)
    sessions_attended = Column(Integer, default=0)
    attendance_rate = Column(Float, default=0.0)
    weekly_attendance = Column(Text)  # JSON array of weekly rates
    last_updated = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="attendance_records")
    course = relationship("Course", back_populates="attendance_records")
    period = relationship("AcademicPeriod", back_populates="attendance_records")

    __table_args__ = (
        UniqueConstraint("student_id", "course_id", "period_id", name="uq_attendance"),
    )


class AssessmentRecord(Base, TimestampMixin):
    """Tests, assignments, and coursework marks"""
    __tablename__ = "assessment_records"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    period_id = Column(Integer, ForeignKey("academic_periods.id"), nullable=False, index=True)
    assessment_type = Column(String(50))  # Test, Assignment, Exam, Coursework
    assessment_name = Column(String(255))
    max_score = Column(Float, default=100.0)
    score = Column(Float, nullable=False)
    percentage = Column(Float, default=0.0)
    submission_date = Column(Date)
    is_submitted = Column(Boolean, default=False)
    is_late = Column(Boolean, default=False)
    days_late = Column(Integer, default=0)
    assessment_date = Column(Date)

    student = relationship("Student", back_populates="assessment_records")
    course = relationship("Course", back_populates="assessment_records")
    period = relationship("AcademicPeriod", back_populates="assessment_records")

    __table_args__ = (
        UniqueConstraint("student_id", "course_id", "period_id", "assessment_name", name="uq_assessment"),
    )


class LMSActivity(Base, TimestampMixin):
    """Learning Management System activity logs"""
    __tablename__ = "lms_activity"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    period_id = Column(Integer, ForeignKey("academic_periods.id"), nullable=False, index=True)
    logins_count = Column(Integer, default=0)
    resources_accessed = Column(Integer, default=0)
    page_views = Column(Integer, default=0)
    assignment_submissions = Column(Integer, default=0)
    time_on_task_minutes = Column(Integer, default=0)
    weekly_activity = Column(Text)  # JSON array of weekly login counts
    last_login = Column(DateTime(timezone=True))

    student = relationship("Student", back_populates="lms_activity")
    course = relationship("Course", back_populates="lms_activity")
    period = relationship("AcademicPeriod", back_populates="lms_activity")

    __table_args__ = (
        UniqueConstraint("student_id", "course_id", "period_id", name="uq_lms_activity"),
    )