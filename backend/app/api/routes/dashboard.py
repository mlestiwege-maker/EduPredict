"""Dashboard API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db_session
from app.core.dependencies import require_user
from app.services.dashboard_service import DashboardService
router = APIRouter()

@router.get("/overview")
async def get_overview(period_id: Optional[int] = Query(None), current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    
    return await DashboardService(session).get_overview(current_user, period_id=period_id)

@router.get("/my-courses")
async def get_my_courses(period_id: Optional[int] = Query(None), current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    
    return await DashboardService(session).get_assigned_courses(current_user["id"], period_id=period_id)

@router.get("/my-advisees")
async def get_my_advisees(period_id: Optional[int] = Query(None), current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    
    return await DashboardService(session).get_assigned_advisees(current_user["id"], period_id=period_id)
