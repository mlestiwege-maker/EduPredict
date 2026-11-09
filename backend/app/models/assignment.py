"""Staff-course and advisor-student assignment models"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base, TimestampMixin


class CourseStaffAssignment(Base, TimestampMixin):
    """Assign lecturers to courses"""
    __tablename__ = "course_staff_assignments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    period_id = Column(Integer, ForeignKey("academic_periods.id"), nullable=False, index=True)
    role = Column(String(50), default="lecturer")
    is_primary = Column(Boolean, default=True)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "course_id", "period_id", name="uq_course_staff"),
    )


class AdvisorAssignment(Base, TimestampMixin):
    """Assign academic advisors to students"""
    __tablename__ = "advisor_assignments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    period_id = Column(Integer, ForeignKey("academic_periods.id"), nullable=False, index=True)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "student_id", "period_id", name="uq_advisor_assignment"),
    )