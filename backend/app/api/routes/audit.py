"""Audit log API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.core.dependencies import require_user
from app.repositories.audit import AuditLogRepository
router = APIRouter()

@router.get('/')
async def list_audit_logs(skip:int=Query(0,ge=0), limit:int=Query(100,ge=1,le=1000), current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    
    repo=AuditLogRepository(session); logs,total=await repo.list(skip=skip, limit=limit)
    return {'total':total,'items':[{'id':l.id,'user_id':l.user_id,'action':l.action,'resource_type':l.resource_type,'resource_id':l.resource_id,'details':l.details,'severity':l.severity,'status':l.status,'created_at':str(l.created_at) if l.created_at else None} for l in logs]}
