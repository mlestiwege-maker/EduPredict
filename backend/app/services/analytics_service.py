"""Analytics service for academic performance analysis"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any, List

from app.repositories.academic import AcademicRepository


class AnalyticsService:
    """Handle academic analytics and reporting"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = AcademicRepository(session)

    async def get_dashboard_summary(
        self,
        period_id: Optional[int] = None,
        department_id: Optional[int] = None,
        course_id: Optional[int] = None,
        user: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Get dashboard summary with key metrics"""
        # Get courses analytics
        courses = await self.get_course_analytics(period_id, department_id)

        # Calculate totals
        total_students = sum(c.total_enrolled for c in courses)
        total_high_risk = sum(c.high_risk_count for c in courses)
        total_medium_risk = sum(c.medium_risk_count for c in courses)
        total_low_risk = sum(c.low_risk_count for c in courses)

        # Calculate overall pass rate
        marks = [c.average_mark for c in courses if c.average_mark is not None]
        overall_pass_rate = sum(marks) / len(marks) if marks else None

        return {
            "total_students": total_students,
            "total_courses": len(courses),
            "total_predictions": total_high_risk + total_medium_risk + total_low_risk,
            "high_risk_count": total_high_risk,
            "medium_risk_count": total_medium_risk,
            "low_risk_count": total_low_risk,
            "overall_pass_rate": overall_pass_rate,
            "courses": [
                {
                    "course_id": c.course_id,
                    "course_code": c.course_code,
                    "course_name": c.course_name,
                    "total_enrolled": c.total_enrolled,
                    "average_mark": c.average_mark,
                    "pass_rate": c.pass_rate,
                    "fail_rate": c.fail_rate,
                    "average_attendance": c.average_attendance,
                    "high_risk_count": c.high_risk_count,
                    "medium_risk_count": c.medium_risk_count,
                    "low_risk_count": c.low_risk_count,
                }
                for c in courses
            ],
        }

    async def get_course_analytics(
        self,
        period_id: Optional[int] = None,
        department_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get analytics for all courses"""
        # This is a simplified implementation
        # In production, this would query actual data from the database
        courses = await self.repo.list_courses(department_id=department_id)

        analytics = []
        for course in courses:
            # Calculate metrics (simplified - would use actual data in production)
            analytics.append({
                "course_id": course.id,
                "course_code": course.code,
                "course_name": course.name,
                "total_enrolled": 0,  # Would query actual enrollment
                "average_mark": None,
                "pass_rate": None,
                "fail_rate": None,
                "average_attendance": None,
                "high_risk_count": 0,
                "medium_risk_count": 0,
                "low_risk_count": 0,
            })

        return analytics

    async def get_performance_trends(
        self,
        period_ids: Optional[List[int]] = None,
        department_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get performance trends over time"""
        periods = await self.repo.list_periods()

        trends = {
            "periods": [
                {"year": p.year, "semester": p.semester, "id": p.id}
                for p in periods
            ],
            "pass_rates": [],
            "average_marks": [],
            "attendance_rates": [],
        }

        return trends

    async def get_influencing_factors(self) -> Dict[str, Any]:
        """Get factors that influence academic performance"""
        # Based on literature review, these are the key factors
        return {
            "factors": [
                {
                    "name": "Previous Academic Performance",
                    "importance": 0.85,
                    "description": "Prior GPA and admission scores are strong predictors",
                },
                {
                    "name": "Attendance",
                    "importance": 0.72,
                    "description": "Regular attendance correlates with better outcomes",
                },
                {
                    "name": "Continuous Assessment",
                    "importance": 0.78,
                    "description": "Early assessment performance indicates likely outcomes",
                },
                {
                    "name": "LMS Engagement",
                    "importance": 0.65,
                    "description": "Online learning activity reflects engagement levels",
                },
                {
                    "name": "Course Load",
                    "importance": 0.58,
                    "description": "Heavy workload relative to prior performance increases risk",
                },
                {
                    "name": "Demographic Factors",
                    "importance": 0.45,
                    "description": "Age, residence, and funding provide context",
                },
            ],
            "note": "Importance scores are illustrative and based on academic literature. Actual values depend on trained models.",
        }