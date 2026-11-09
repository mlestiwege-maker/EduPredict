"""Academic API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.core.database import get_db_session
from app.core.dependencies import require_user
from app.models.academic import Student, Course, Programme, Department, AcademicPeriod
router = APIRouter()

@router.get('/students')
async def list_students(skip:int=0, limit:int=200, programme_id: Optional[int]=Query(None), current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    
    q=select(Student)
    if programme_id: q=q.where(Student.programme_id==programme_id)
    q=q.offset(skip).limit(limit)
    rows=(await session.execute(q)).scalars().all()
    return [{'id':s.id,'pseudonym':s.pseudonym,'programme_id':s.programme_id,'year_of_study':s.year_of_study,'enrollment_status':s.enrollment_status,'age_band':s.age_band,'gender':s.gender,'residence_type':s.residence_type,'funding_type':s.funding_type} for s in rows]

@router.get('/courses')
async def list_courses(current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    
    rows=(await session.execute(select(Course))).scalars().all()
    return [{'id':c.id,'code':c.code,'name':c.name,'department_id':c.department_id,'credits':c.credits,'level':c.level} for c in rows]

@router.get('/periods')
async def list_periods(current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    
    rows=(await session.execute(select(AcademicPeriod))).scalars().all()
    return [{'id':p.id,'year':p.year,'semester':p.semester,'is_active':p.is_active} for p in rows]
