"""Recommendation and intervention service"""

from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional, List, Dict, Any

from app.models.recommendation import (
    RecommendationRule, Recommendation, Intervention, InterventionFollowup
)
from app.models.data import StudentPrediction


class RecommendationService:
    """Handle recommendations and interventions"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_student_recommendations(
        self,
        student_id: int,
        status: Optional[str] = None
    ) -> List[Recommendation]:
        """Get recommendations for a student"""
        from sqlalchemy import select
        query = select(Recommendation).where(Recommendation.student_id == student_id)

        if status:
            query = query.where(Recommendation.status == status)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_intervention(
        self,
        intervention_data: dict,
        staff_id: int
    ) -> Intervention:
        """Create a new intervention"""
        intervention = Intervention(
            student_id=intervention_data["student_id"],
            recommendation_id=intervention_data.get("recommendation_id"),
            staff_id=staff_id,
            intervention_type=intervention_data["intervention_type"],
            description=intervention_data["description"],
            action_taken=intervention_data.get("action_taken"),
            follow_up_date=intervention_data.get("follow_up_date"),
            notes=intervention_data.get("notes"),
            status="planned",
            start_date=datetime.utcnow(),
        )
        self.session.add(intervention)
        await self.session.flush()
        await self.session.refresh(intervention)
        return intervention

    async def get_student_interventions(self, student_id: int) -> List[Intervention]:
        """Get interventions for a student"""
        from sqlalchemy import select
        result = await self.session.execute(
            select(Intervention).where(Intervention.student_id == student_id)
        )
        return result.scalars().all()

    async def update_intervention(
        self,
        intervention_id: int,
        update_data: dict
    ) -> Intervention:
        """Update an intervention"""
        from sqlalchemy import update
        await self.session.execute(
            update(Intervention)
            .where(Intervention.id == intervention_id)
            .values(**update_data)
        )

        intervention = await self.session.get(Intervention, intervention_id)
        return intervention

    async def get_active_rules(self) -> List[Dict[str, Any]]:
        """Get active recommendation rules"""
        from sqlalchemy import select
        result = await self.session.execute(
            select(RecommendationRule).where(RecommendationRule.is_active == True)
        )
        rules = result.scalars().all()

        return [
            {
                "id": r.id,
                "rule_code": r.rule_code,
                "name": r.name,
                "description": r.description,
                "action": r.action,
                "responsible_role": r.responsible_role,
                "priority": r.priority,
            }
            for r in rules
        ]