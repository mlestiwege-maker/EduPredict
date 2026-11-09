"""Dashboard service for role-specific views"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any, List

from app.core.security import has_permission
from app.services.analytics_service import AnalyticsService


class DashboardService:
    """Provide role-specific dashboard data"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.analytics = AnalyticsService(session)

    async def get_overview(
        self,
        user: Dict[str, Any],
        period_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get role-specific dashboard overview"""
        roles = user.get("roles", [])

        if "system_admin" in roles:
            return await self._get_admin_overview(user, period_id)
        elif "lecturer" in roles:
            return await self._get_lecturer_overview(user, period_id)
        elif "academic_advisor" in roles:
            return await self._get_advisor_overview(user, period_id)
        elif "head_of_department" in roles:
            return await self._get_hod_overview(user, period_id)
        elif "dean" in roles:
            return await self._get_dean_overview(user, period_id)
        elif "registry" in roles:
            return await self._get_registry_overview(user, period_id)
        else:
            return {"message": "No role assigned", "dashboard": {}}

    async def _get_admin_overview(self, user: Dict[str, Any], period_id: Optional[int]) -> Dict[str, Any]:
        """Get system administrator overview"""
        summary = await self.analytics.get_dashboard_summary(period_id=period_id, user=user)
        return {
            "role": "System Administrator",
            "summary": summary,
            "sections": {
                "system_status": {
                    "users": 0,  # Would query actual count
                    "active_sessions": 0,
                    "system_health": "healthy",
                },
                "recent_imports": [],
                "model_status": {
                    "current_version": "1.0.0",
                    "last_trained": None,
                    "status": "ready",
                },
            },
        }

    async def _get_lecturer_overview(self, user: Dict[str, Any], period_id: Optional[int]) -> Dict[str, Any]:
        """Get lecturer overview"""
        summary = await self.analytics.get_dashboard_summary(period_id=period_id, user=user)
        return {
            "role": "Lecturer",
            "summary": summary,
            "sections": {
                "my_courses": await self.get_assigned_courses(user["id"], period_id),
                "at_risk_students": [],
                "recent_interventions": [],
            },
        }

    async def _get_advisor_overview(self, user: Dict[str, Any], period_id: Optional[int]) -> Dict[str, Any]:
        """Get academic advisor overview"""
        return {
            "role": "Academic Advisor",
            "summary": {
                "total_advisees": 0,
                "high_risk_count": 0,
                "medium_risk_count": 0,
                "low_risk_count": 0,
            },
            "sections": {
                "my_advisees": await self.get_assigned_advisees(user["id"], period_id),
                "upcoming_followups": [],
                "recent_interventions": [],
            },
        }

    async def _get_hod_overview(self, user: Dict[str, Any], period_id: Optional[int]) -> Dict[str, Any]:
        """Get HOD overview"""
        summary = await self.analytics.get_dashboard_summary(period_id=period_id, user=user)
        return {
            "role": "Head of Department",
            "summary": summary,
            "sections": {
                "department_courses": [],
                "risk_trends": [],
                "intervention_summary": {
                    "total": 0,
                    "completed": 0,
                    "in_progress": 0,
                },
            },
        }

    async def _get_dean_overview(self, user: Dict[str, Any], period_id: Optional[int]) -> Dict[str, Any]:
        """Get dean overview"""
        summary = await self.analytics.get_dashboard_summary(period_id=period_id, user=user)
        return {
            "role": "Dean",
            "summary": summary,
            "sections": {
                "faculty_programmes": [],
                "comparative_analytics": {},
                "resource_allocation": {},
            },
        }

    async def _get_registry_overview(self, user: Dict[str, Any], period_id: Optional[int]) -> Dict[str, Any]:
        """Get registry overview"""
        summary = await self.analytics.get_dashboard_summary(period_id=period_id, user=user)
        return {
            "role": "Registry Staff",
            "summary": summary,
            "sections": {
                "cohort_summary": {},
                "progression_metrics": {},
                "data_quality": {
                    "last_import": None,
                    "status": "good",
                },
            },
        }

    async def get_assigned_courses(self, user_id: int, period_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get courses assigned to a lecturer"""
        # Placeholder - would query actual assignments
        return []

    async def get_assigned_advisees(self, user_id: int, period_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get students assigned to an advisor"""
        # Placeholder - would query actual assignments
        return []

    async def get_department_summary(self, user: Dict[str, Any], period_id: Optional[int]) -> Dict[str, Any]:
        """Get department summary for HOD"""
        return await self._get_hod_overview(user, period_id)

    async def get_faculty_summary(self, user: Dict[str, Any], period_id: Optional[int]) -> Dict[str, Any]:
        """Get faculty summary for Dean"""
        return await self._get_dean_overview(user, period_id)

    async def get_institutional_summary(self, user: Dict[str, Any], period_id: Optional[int]) -> Dict[str, Any]:
        """Get institutional summary for Registry"""
        return await self._get_registry_overview(user, period_id)