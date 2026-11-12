"""Recommendations and interventions API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List, Any, Dict
from pydantic import BaseModel
from app.core.database import get_db_session
from app.core.dependencies import require_user
from app.models.data import StudentPrediction
from app.models.academic import Student, Course
from app.models.recommendation import Intervention
router = APIRouter()

RULES=[
 {'id':'R1','condition':'Low attendance or declining engagement','action':'Advisor contact and engagement check-in','responsible_role':'Academic Advisor','priority':'High'},
 {'id':'R2','condition':'Weak early assessment performance','action':'Tutoring referral / subject workshop','responsible_role':'Lecturer','priority':'High'},
 {'id':'R3','condition':'Heavy course load vs prior performance','action':'Review course load with authorised staff','responsible_role':'Academic Advisor','priority':'Medium'},
 {'id':'R4','condition':'Late/missing submissions','action':'Study-skills and time-management support','responsible_role':'Lecturer / Student Support','priority':'Medium'},
 {'id':'R5','condition':'High risk with normal engagement / non-academic concern','action':'Appropriate student support referral','responsible_role':'Academic Advisor','priority':'High'},
]

@router.get("/rules")
async def get_rules(current_user=Depends(require_user)):
    
    return {'rules':RULES,'note':'Transparent rules; reviewed and approved by institutional staff.'}

@router.get("/generated")
async def get_generated(period_id: int = Query(2), checkpoint: str = Query('week_4'), current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    
    q=select(StudentPrediction,Student,Course).join(Student,Student.id==StudentPrediction.student_id).join(Course,Course.id==StudentPrediction.course_id).where(StudentPrediction.period_id==period_id, StudentPrediction.checkpoint==checkpoint, StudentPrediction.risk_band.in_(['high','medium'])).order_by(StudentPrediction.risk_probability.desc()).limit(200)
    rows=(await session.execute(q)).all()
    out=[]
    for p,s,c in rows:
        rule=RULES[0] if p.risk_probability>=0.7 else (RULES[1] if p.risk_probability>=0.55 else RULES[3])
        out.append({'student_pseudonym':s.pseudonym,'student_id':s.id,'course_code':c.code,'course_id':c.id,'risk_probability':p.risk_probability,'risk_band':p.risk_band,'rule':rule['id'],'action':rule['action'],'responsible_role':rule['responsible_role'],'priority':rule['priority'],'status':'pending_review'})
    return {'items':out,'count':len(out)}

class InterventionIn(BaseModel):
    student_id:int; recommendation_id:Optional[int]=None; intervention_type:str; description:str; action_taken:Optional[str]=None; status:Optional[str]='planned'; notes:Optional[str]=None

@router.get("/interventions")
async def list_interventions(current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    
    rows=(await session.execute(select(Intervention).order_by(Intervention.id.desc()).limit(200))).scalars().all()
    return [{'id':i.id,'student_id':i.student_id,'intervention_type':i.intervention_type,'description':i.description,'action_taken':i.action_taken,'status':i.status,'notes':i.notes} for i in rows]

@router.post("/interventions")
async def create_intervention(data: InterventionIn, current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    
    obj=Intervention(student_id=data.student_id,recommendation_id=data.recommendation_id,staff_id=current_user['id'],intervention_type=data.intervention_type,description=data.description,action_taken=data.action_taken,status=data.status or 'planned',notes=data.notes)
    session.add(obj); await session.commit(); await session.refresh(obj)
    return {'id':obj.id,'status':obj.status,'message':'Intervention recorded.'}
