"""Audit log data access layer"""

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional, List, Tuple

from app.models.audit import AuditLog


class AuditLogRepository:
    """Data access for audit logs"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, log_data: dict) -> AuditLog:
        """Create a new audit log entry"""
        log = AuditLog(**log_data)
        self.session.add(log)
        await self.session.flush()
        await self.session.refresh(log)
        return log

    async def list(
        self,
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[int] = None,
        action: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Tuple[List[AuditLog], int]:
        """List audit logs with filters and pagination"""
        query = select(AuditLog)

        conditions = []
        if user_id:
            conditions.append(AuditLog.user_id == user_id)
        if action:
            conditions.append(AuditLog.action.ilike(f"%{action}%"))
        if start_date:
            conditions.append(AuditLog.created_at >= start_date)
        if end_date:
            conditions.append(AuditLog.created_at <= end_date)

        if conditions:
            query = query.where(and_(*conditions))

        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar()

        # Get paginated results
        query = query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(query)
        logs = result.scalars().all()

        return logs, total