"""Prediction service: connects ML runtime + DB persistence."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import Optional, Dict, Any, List
from app.models.data import PredictionRun, StudentPrediction, PredictionExplanation
from app.models.academic import Student, Course, AcademicPeriod
from app.services.ml_runtime import train as ml_train, predict as ml_predict

class PredictionService:
    def __init__(self, session: AsyncSession): self.session = session

    async def _maps(self):
        s=(await self.session.execute(select(Student))).scalars().all()
        c=(await self.session.execute(select(Course))).scalars().all()
        p=(await self.session.execute(select(AcademicPeriod))).scalars().all()
        return ({x.pseudonym:x.id for x in s}, {x.code:x.id for x in c}, {(x.semester):x.id for x in p})

    async def run_prediction(self, period_id: int, checkpoint: str, model_version: Optional[str] = None, user_id: Optional[int] = None) -> Dict[str, Any]:
        out = ml_predict(checkpoint)
        if out.get('status')=='error': return out
        # persist
        run = PredictionRun(model_version=out['model_version'], checkpoint=checkpoint, period_id=period_id, status='completed', run_metadata={'model_name':out['model_name']})
        self.session.add(run); await self.session.flush(); await self.session.refresh(run)
        stu_map, course_map, period_map = await self._maps()
        # clear previous for checkpoint+period
        old = (await self.session.execute(select(StudentPrediction.id).where(StudentPrediction.period_id==period_id, StudentPrediction.checkpoint==checkpoint))).scalars().all()
        if old:
            await self.session.execute(delete(PredictionExplanation).where(PredictionExplanation.prediction_id.in_(old)))
            await self.session.execute(delete(StudentPrediction).where(StudentPrediction.id.in_(old)))
        hi=med=lo=0
        for r in out['rows']:
            sid=stu_map.get(r['student_pseudonym']); cid=course_map.get(r['course_code']); pid=period_map.get(r['period_code'], period_id)
            if not sid or not cid: continue
            band=r['risk_band']; hi+=band=='high'; med+=band=='medium'; lo+=band=='low'
            sp=StudentPrediction(student_id=sid,prediction_run_id=run.id,period_id=pid,course_id=cid,checkpoint=checkpoint,
                                 risk_probability=r['risk_probability'],risk_band=band,predicted_outcome=r['predicted_outcome'],
                                 confidence_score=r['confidence_score'],model_version=r['model_version'])
            self.session.add(sp); await self.session.flush()
            for e in r.get('explanations',[]):
                self.session.add(PredictionExplanation(prediction_id=sp.id,feature_name=e['feature_name'],feature_value=float(e.get('feature_value') or 0),shap_value=float(e.get('shap_value') or e.get('impact') or 0),impact=e.get('impact'),description=e.get('description')))
        run.total_predictions=hi+med+lo; run.high_risk_count=hi; run.medium_risk_count=med; run.low_risk_count=lo
        await self.session.commit()
        return {'status':'ok','run_id':run.id,'checkpoint':checkpoint,'model_version':out['model_version'],'model_name':out['model_name'],'total_predictions':run.total_predictions,'summary':{'high':hi,'medium':med,'low':lo}}

    async def train_models(self, checkpoint: str):
        return ml_train(checkpoint)

    async def ml_status(self):
        from app.services.ml_runtime import status as ml_status_fn
        return ml_status_fn()

    async def get_student_predictions(self, student_id: int, period_id: Optional[int] = None) -> List[StudentPrediction]:
        q = select(StudentPrediction).where(StudentPrediction.student_id == student_id)
        if period_id: q = q.where(StudentPrediction.period_id == period_id)
        q = q.order_by(StudentPrediction.id.desc())
        res = await self.session.execute(q); return list(res.scalars().all())

    async def get_course_risk_summary(self, course_id: int, period_id: int, checkpoint: str = "week_4") -> Dict[str, Any]:
        q = select(StudentPrediction).where(StudentPrediction.course_id==course_id, StudentPrediction.period_id==period_id, StudentPrediction.checkpoint==checkpoint)
        preds = list((await self.session.execute(q)).scalars().all())
        hi=sum(1 for p in preds if p.risk_band=='high'); me=sum(1 for p in preds if p.risk_band=='medium'); lo=sum(1 for p in preds if p.risk_band=='low')
        return {'course_id':course_id,'period_id':period_id,'checkpoint':checkpoint,'total_students':len(preds),'high_risk':hi,'medium_risk':me,'low_risk':lo,'risk_distribution':{'high':hi,'medium':me,'low':lo}}

    async def get_at_risk_students(self, period_id: int, course_id: Optional[int] = None, risk_band: Optional[str] = None, checkpoint: Optional[str]=None) -> List[Dict[str, Any]]:
        q = select(StudentPrediction, Student, Course).join(Student, Student.id==StudentPrediction.student_id).join(Course, Course.id==StudentPrediction.course_id).where(StudentPrediction.period_id==period_id)
        if course_id: q = q.where(StudentPrediction.course_id==course_id)
        if risk_band and risk_band!='all': q = q.where(StudentPrediction.risk_band==risk_band)
        if checkpoint: q = q.where(StudentPrediction.checkpoint==checkpoint)
        q=q.order_by(StudentPrediction.risk_probability.desc())
        rows=(await self.session.execute(q)).all()
        return [{'id':p.id,'student_id':p.student_id,'student_pseudonym':s.pseudonym,'course_id':p.course_id,'course_code':c.code,'course_name':c.name,'risk_probability':p.risk_probability,'risk_band':p.risk_band,'predicted_outcome':p.predicted_outcome,'confidence_score':p.confidence_score,'checkpoint':p.checkpoint,'model_version':p.model_version} for p,s,c in rows]
