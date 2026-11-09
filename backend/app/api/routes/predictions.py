"""Predictions API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db_session
from app.core.dependencies import require_user
from app.services.prediction_service import PredictionService
router = APIRouter()

@router.get('/status')
async def prediction_status(current_user=Depends(require_user)):
    from app.services.ml_runtime import status as ml_status_fn
    return ml_status_fn()

@router.post('/train/{checkpoint}')
async def train_models(checkpoint: str, current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    return await PredictionService(session).train_models(checkpoint)

@router.post('/run/{period_id}/{checkpoint}')
async def run_prediction(period_id: int, checkpoint: str, current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    try:
        return await PredictionService(session).run_prediction(period_id=period_id, checkpoint=checkpoint, user_id=current_user['id'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/at-risk')
async def get_at_risk_students(period_id: int = Query(2), course_id: Optional[int] = Query(None), risk_band: Optional[str] = Query(None), checkpoint: Optional[str] = Query('week_4'), current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    return await PredictionService(session).get_at_risk_students(period_id=period_id, course_id=course_id, risk_band=risk_band, checkpoint=checkpoint)

@router.get('/student/{student_id}')
async def get_student_predictions(student_id: int, period_id: Optional[int] = Query(None), current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    preds = await PredictionService(session).get_student_predictions(student_id, period_id=period_id)
    return [{'id':p.id,'student_id':p.student_id,'course_id':p.course_id,'period_id':p.period_id,'checkpoint':p.checkpoint,'risk_probability':p.risk_probability,'risk_band':p.risk_band,'predicted_outcome':p.predicted_outcome,'confidence_score':p.confidence_score,'model_version':p.model_version} for p in preds]
