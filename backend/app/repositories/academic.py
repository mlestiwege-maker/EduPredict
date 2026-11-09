"""Academic data access layer"""

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List, Dict, Any

from app.models.academic import (
    Department, Programme, Course, AcademicPeriod,
    Student, CourseEnrolment, AcademicHistory,
)


class AcademicRepository:
    """Data access for academic structure and records"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_departments(self) -> List[Department]:
        """List all departments"""
        result = await self.session.execute(select(Department))
        return result.scalars().all()

    async def list_programmes(self, department_id: Optional[int] = None) -> List[Programme]:
        """List programmes, optionally filtered"""
        query = select(Programme)
        if department_id:
            query = query.where(Programme.department_id == department_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def list_courses(self, department_id: Optional[int] = None) -> List[Course]:
        """List courses, optionally filtered"""
        query = select(Course)
        if department_id:
            query = query.where(Course.department_id == department_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def list_periods(self, is_active: Optional[bool] = None) -> List[AcademicPeriod]:
        """List academic periods"""
        query = select(AcademicPeriod)
        if is_active is not None:
            query = query.where(AcademicPeriod.is_active == is_active)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def list_students(
        self,
        programme_id: Optional[int] = None,
        year_of_study: Optional[int] = None
    ) -> List[Student]:
        """List students with optional filters"""
        query = select(Student)
        if programme_id:
            query = query.where(Student.programme_id == programme_id)
        if year_of_study:
            query = query.where(Student.year_of_study == year_of_study)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_student_profile(self, student_id: int) -> Optional[Dict[str, Any]]:
        """Get detailed student profile"""
        student = await self.session.get(Student, student_id)
        if not student:
            return None

        # Get academic history
        history_result = await self.session.execute(
            select(AcademicHistory).where(AcademicHistory.student_id == student_id)
        )
        academic_history = [
            {
                "period_id": h.period_id,
                "entry_qualification": h.entry_qualification,
                "admission_score": h.admission_score,
                "previous_gpa": h.previous_gpa,
                "first_year_average": h.first_year_average,
                "cumulative_gpa": h.cumulative_gpa,
                "credits_attempted": h.credits_attempted,
                "credits_passed": h.credits_passed,
            }
            for h in history_result.scalars().all()
        ]

        # Get current enrolments
        enrolments_result = await self.session.execute(
            select(CourseEnrolment)
            .join(Course, Course.id == CourseEnrolment.course_id)
            .where(CourseEnrolment.student_id == student_id)
        )
        current_enrolments = [
            {
                "enrolment_id": e.id,
                "course_id": e.course_id,
                "course_code": e.course.code if e.course else "",
                "course_name": e.course.name if e.course else "",
                "period_id": e.period_id,
                "credit_load": e.credit_load,
            }
            for e in enrolments_result.scalars().all()
        ]

        return {
            "student": student,
            "academic_history": academic_history,
            "current_enrolments": current_enrolments,
            "predictions": [],
            "interventions": [],
        }