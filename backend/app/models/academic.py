"""Academic structure models"""

from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy import Table, UniqueConstraint
from app.models.base import Base, TimestampMixin


class Department(Base, TimestampMixin):
    """Academic departments"""
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)

    programmes = relationship("Programme", back_populates="department")
    courses = relationship("Course", back_populates="department")


class Programme(Base, TimestampMixin):
    """Academic programmes"""
    __tablename__ = "programmes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    code = Column(String(20), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    level = Column(String(20))  # Bachelor, Masters, PhD
    duration_years = Column(Integer, default=4)
    is_active = Column(Boolean, default=True)

    department = relationship("Department", back_populates="programmes")
    students = relationship("Student", back_populates="programme")


class Course(Base, TimestampMixin):
    """Courses offered by departments"""
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    credits = Column(Integer, default=5)
    level = Column(String(10))  # 100, 200, 300, 400
    is_active = Column(Boolean, default=True)

    department = relationship("Department", back_populates="courses")
    enrolments = relationship("CourseEnrolment", back_populates="course")
    attendance_records = relationship("AttendanceRecord", back_populates="course")
    assessment_records = relationship("AssessmentRecord", back_populates="course")
    lms_activity = relationship("LMSActivity", back_populates="course")


class AcademicPeriod(Base, TimestampMixin):
    """Academic years and semesters"""
    __tablename__ = "academic_periods"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, index=True)
    semester = Column(String(20), nullable=False)  # First, Second, Summer
    term_start = Column(Date)
    term_end = Column(Date)
    is_active = Column(Boolean, default=False)

    enrolments = relationship("CourseEnrolment", back_populates="period")
    attendance_records = relationship("AttendanceRecord", back_populates="period")
    assessment_records = relationship("AssessmentRecord", back_populates="period")
    lms_activity = relationship("LMSActivity", back_populates="period")
    predictions = relationship("StudentPrediction", back_populates="period")


class Student(Base, TimestampMixin):
    """Student records (pseudonymous)"""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    pseudonym = Column(String(20), unique=True, nullable=False, index=True)  # e.g., STU-001
    programme_id = Column(Integer, ForeignKey("programmes.id"), nullable=False)
    year_of_study = Column(Integer, default=1)
    enrollment_status = Column(String(20), default="Active")
    age_band = Column(String(20))
    gender = Column(String(10))
    residence_type = Column(String(50))
    funding_type = Column(String(50))

    programme = relationship("Programme", back_populates="students")
    enrolments = relationship("CourseEnrolment", back_populates="student")
    academic_history = relationship("AcademicHistory", back_populates="student")
    attendance_records = relationship("AttendanceRecord", back_populates="student")
    assessment_records = relationship("AssessmentRecord", back_populates="student")
    lms_activity = relationship("LMSActivity", back_populates="student")
    predictions = relationship("StudentPrediction", back_populates="student")
    recommendations = relationship("Recommendation", back_populates="student")


class CourseEnrolment(Base, TimestampMixin):
    """Student enrollment in courses"""
    __tablename__ = "course_enrolments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    period_id = Column(Integer, ForeignKey("academic_periods.id"), nullable=False, index=True)
    credit_load = Column(Integer, default=5)
    enrollment_date = Column(Date)

    student = relationship("Student", back_populates="enrolments")
    course = relationship("Course", back_populates="enrolments")
    period = relationship("AcademicPeriod", back_populates="enrolments")

    __table_args__ = (
        UniqueConstraint("student_id", "course_id", "period_id", name="uq_enrollment"),
    )


class AcademicHistory(Base, TimestampMixin):
    """Previous academic performance"""
    __tablename__ = "academic_history"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    period_id = Column(Integer, ForeignKey("academic_periods.id"), nullable=False, index=True)
    entry_qualification = Column(String(50))
    admission_score = Column(Float)
    previous_gpa = Column(Float)
    first_year_average = Column(Float)
    cumulative_gpa = Column(Float)
    credits_attempted = Column(Integer, default=0)
    credits_passed = Column(Integer, default=0)

    student = relationship("Student", back_populates="academic_history")
    period = relationship("AcademicPeriod")