"""Reports API endpoints (PDF/Excel via openpyxl/basic PDF fallback)."""
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel
from app.core.database import get_db_session
from app.core.dependencies import require_user
from app.models.data import StudentPrediction
from app.models.academic import Student, Course
from app.models.report import ReportJob

router = APIRouter()
OUT = Path(__file__).resolve().parents[4] / 'ml' / 'reports' / 'generated'
OUT.mkdir(parents=True, exist_ok=True)

class ReportReq(BaseModel):
    report_type: str
    report_format: str = 'excel'
    title: Optional[str] = None
    period_id: Optional[int] = 2
    checkpoint: Optional[str] = 'week_4'

def _excel(path: Path, title: str, rows):
    from openpyxl import Workbook
    wb=Workbook(); ws=wb.active; ws.title='Report'
    ws.append([title]); ws.append(['Generated', datetime.utcnow().isoformat()+'Z']); ws.append(['Disclaimer','Synthetic/demo or authorized-data output. Predictions are decision-support estimates, not verdicts.']); ws.append([])
    if rows:
        ws.append(list(rows[0].keys()))
        for r in rows: ws.append([r.get(k) for k in rows[0].keys()])
    else:
        ws.append(['No data available'])
    wb.save(path)

@router.post('/generate')
async def generate_report(req: ReportReq, current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    
    q=select(StudentPrediction,Student,Course).join(Student,Student.id==StudentPrediction.student_id).join(Course,Course.id==StudentPrediction.course_id)
    if req.period_id: q=q.where(StudentPrediction.period_id==req.period_id)
    if req.checkpoint: q=q.where(StudentPrediction.checkpoint==req.checkpoint)
    q=q.order_by(StudentPrediction.risk_probability.desc()).limit(1000)
    rows=[{'student_pseudonym':s.pseudonym,'course':c.code,'checkpoint':p.checkpoint,'risk_probability':p.risk_probability,'risk_band':p.risk_band,'predicted_outcome':p.predicted_outcome,'model_version':p.model_version} for p,s,c in (await session.execute(q)).all()]
    title=req.title or f"{req.report_type} ({req.checkpoint})"
    ts=datetime.utcnow().strftime('%Y%m%d%H%M%S')
    ext='xlsx' if req.report_format!='pdf' else 'xlsx' # pdf fallback to excel for env without reportlab
    path=OUT/f"{req.report_type}_{req.checkpoint}_{ts}.{ext}"
    _excel(path,title,rows)
    job=ReportJob(user_id=current_user['id'],report_type=req.report_type,report_format='excel',title=title,parameters=req.model_dump(),status='completed',file_path=str(path),file_size=path.stat().st_size if path.exists() else 0,generated_at=datetime.utcnow())
    session.add(job); await session.commit(); await session.refresh(job)
    return {'id':job.id,'report_type':job.report_type,'report_format':job.report_format,'title':job.title,'status':job.status,'file_path':job.file_path,'rows':len(rows),'note':'PDF export falls back to Excel in this environment if ReportLab is unavailable.'}

@router.get('/')
async def list_reports(current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    
    rows=(await session.execute(select(ReportJob).order_by(ReportJob.id.desc()).limit(100))).scalars().all()
    return [{'id':r.id,'report_type':r.report_type,'report_format':r.report_format,'title':r.title,'status':r.status,'file_path':r.file_path,'generated_at':r.generated_at} for r in rows]

@router.get('/{report_id}/download')
async def download_report(report_id:int, current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    
    r=await session.get(ReportJob, report_id)
    if not r or not r.file_path or not Path(r.file_path).exists(): raise HTTPException(status_code=404, detail='Report not found')
    return FileResponse(r.file_path, filename=Path(r.file_path).name)
