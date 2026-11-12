"""Analytics API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from app.core.database import get_db_session
from app.core.dependencies import require_user
from app.services.analytics_service import AnalyticsService
from app.models.academic import Student
from app.models.engagement import AttendanceRecord, AssessmentRecord, LMSActivity
router = APIRouter()

@router.get("/summary")
async def get_dashboard_summary(period_id: Optional[int] = Query(None), department_id: Optional[int] = Query(None), current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    
    # institutional aggregates
    total = (await session.execute(select(func.count()).select_from(Student))).scalar() or 0
    att = (await session.execute(select(func.avg(AttendanceRecord.attendance_rate)))).scalar()
    mark = (await session.execute(select(func.avg(AssessmentRecord.percentage)))).scalar()
    sub = (await session.execute(select(func.avg(AssessmentRecord.is_submitted)))).scalar()
    return {'total_students': total, 'total_courses': (await session.execute(select(func.count()).select_from(__import__('app.models.academic',fromlist=['Course']).Course))).scalar() or 0,
            'overall_attendance_rate': round(float(att or 0),1), 'overall_average_mark': round(float(mark or 0),1), 'overall_submission_rate': round(float(sub or 0)*100,1)}

@router.get("/factors")
async def get_influencing_factors(current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    
    return await AnalyticsService(session).get_influencing_factors()
