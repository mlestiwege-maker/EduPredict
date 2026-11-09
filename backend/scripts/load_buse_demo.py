"""Load synthetic BUSE demo dataset into the database (matches SQLAlchemy models)."""
import sys, json
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from sqlalchemy import create_engine, text
from app.core.config import settings
from app.models import Base

DATA = Path(__file__).resolve().parents[2] / 'ml/data/sample/buse'

def run():
    if not DATA.exists(): raise SystemExit(f'Missing dataset: {DATA}')
    url = settings.database_url.replace('sqlite+aiosqlite','sqlite')
    engine = create_engine(url, future=True)
    Base.metadata.create_all(engine)
    dep = pd.read_csv(DATA/'departments.csv')
    per = pd.read_csv(DATA/'academic_periods.csv')
    prog = pd.read_csv(DATA/'programmes.csv')
    crs = pd.read_csv(DATA/'courses.csv')
    stu = pd.read_csv(DATA/'students.csv')
    enr = pd.read_csv(DATA/'enrolments.csv')
    att = pd.read_csv(DATA/'attendance.csv')
    asm = pd.read_csv(DATA/'assessments.csv')
    lms = pd.read_csv(DATA/'lms_activity.csv')
    with engine.begin() as cx:
        for t in ['prediction_explanations','student_predictions','prediction_runs','recommendations','interventions','data_quality_issues','data_imports','lms_activity','assessment_records','attendance_records','course_enrolments','academic_history','students','courses','programmes','departments','academic_periods']:
            try: cx.execute(text(f'delete from {t}'))
            except Exception: pass
        cx.execute(text('insert into departments(name,code,description) values (:n,:c,:d)'), [dict(n=r.department_name,c=r.department_code,d=f'BUSE {r.department_name}') for r in dep.itertuples()])
        dep_map = {r.code:i for i,r in enumerate(cx.execute(text('select id,code from departments')).mappings(),1)}
        cx.execute(text('insert into academic_periods(year,semester,term_start,term_end,is_active) values (:y,:s,:ts,:te,:a)'), [dict(y=int(r.year),s=r.period_code,ts=str(r.term_start),te=str(r.term_end),a=int(r.is_active)) for r in per.itertuples()])
        per_map = {r.semester:r.id for r in cx.execute(text('select id,semester from academic_periods')).mappings()}
        cx.execute(text('insert into programmes(name,code,department_id,level,duration_years,is_active) values (:n,:c,:d,:l,:dur,:a)'), [dict(n=r.programme_name,c=r.programme_code,d=dep_map[r.department_code],l=r.level,dur=int(r.duration_years),a=1) for r in prog.itertuples()])
        prog_map = {r.code:r.id for r in cx.execute(text('select id,code from programmes')).mappings()}
        cx.execute(text('insert into courses(code,name,department_id,credits,level,is_active) values (:c,:n,:d,:cr,:l,:a)'), [dict(c=r.course_code,n=r.course_name,d=dep_map[r.department_code],cr=int(r.credits),l=str(r.level),a=1) for r in crs.itertuples()])
        crs_map = {r.code:r.id for r in cx.execute(text('select id,code from courses')).mappings()}
        cx.execute(text('insert into students(pseudonym,programme_id,year_of_study,enrollment_status,age_band,gender,residence_type,funding_type) values (:p,:pr,:y,:es,:ab,:g,:rt,:ft)'), [dict(p=r.student_pseudonym,pr=prog_map[r.programme_code],y=int(r.year_of_study),es=r.enrollment_status,ab=r.age_band,g=r.gender,rt=r.residence_type,ft=r.funding_type) for r in stu.itertuples()])
        stu_map = {r.pseudonym:r.id for r in cx.execute(text('select id,pseudonym from students')).mappings()}
        cx.execute(text('insert into academic_history(student_id,period_id,entry_qualification,admission_score,previous_gpa,first_year_average,cumulative_gpa,credits_attempted,credits_passed) values (:s,:p,:eq,:ad,:pg,:fy,:cg,:ca,:cp)'), [dict(s=stu_map[r.student_pseudonym],p=per_map.get('2025-S1',1),eq='A-Level',ad=float(r.admission_score),pg=float(r.previous_gpa),fy=float(r.admission_score),cg=float(r.previous_gpa),ca=30,cp=24) for r in stu.itertuples()])
        enr_rows=[dict(s=stu_map[r.student_pseudonym],c=crs_map[r.course_code],p=per_map[r.period_code],cl=int(r.credit_load),ed='2025-08-04') for r in enr.itertuples() if r.student_pseudonym in stu_map and r.course_code in crs_map and r.period_code in per_map]
        seen=set(); dedup=[]
        for r in enr_rows:
            k=(r['s'],r['c'],r['p']);
            if k in seen: continue
            seen.add(k); dedup.append(r)
        cx.execute(text('insert into course_enrolments(student_id,course_id,period_id,credit_load,enrollment_date) values (:s,:c,:p,:cl,:ed)'), dedup)
        cx.execute(text('insert into attendance_records(student_id,course_id,period_id,sessions_scheduled,sessions_attended,attendance_rate,weekly_attendance) values (:s,:c,:p,:ss,:sa,:ar,:wa)'), [dict(s=stu_map[r.student_pseudonym],c=crs_map[r.course_code],p=per_map[r.period_code],ss=int(r.sessions_scheduled),sa=int(r.sessions_attended),ar=float(r.attendance_rate),wa='[]') for r in att.itertuples() if r.student_pseudonym in stu_map and r.course_code in crs_map and r.period_code in per_map])
        asm_rows=[dict(s=stu_map[r.student_pseudonym],c=crs_map[r.course_code],p=per_map[r.period_code],at=r.assessment_type,an=r.assessment_name,ms=float(r.max_score),sc=float(r.score),pc=float(r.score),sd='2025-09-15',isub=int(r.is_submitted),il=int(r.is_late),dl=int(r.is_late)*2,ad='2025-09-15') for r in asm.itertuples() if r.student_pseudonym in stu_map and r.course_code in crs_map and r.period_code in per_map]
        seen=set(); dedup=[]
        for r in asm_rows:
            k=(r['s'],r['c'],r['p'],r['an'])
            if k in seen: continue
            seen.add(k); dedup.append(r)
        cx.execute(text('insert into assessment_records(student_id,course_id,period_id,assessment_type,assessment_name,max_score,score,percentage,submission_date,is_submitted,is_late,days_late,assessment_date) values (:s,:c,:p,:at,:an,:ms,:sc,:pc,:sd,:isub,:il,:dl,:ad)'), dedup)
        lms_rows=[dict(s=stu_map[r.student_pseudonym],c=crs_map[r.course_code],p=per_map[r.period_code],lc=int(r.logins_count),ra=int(r.resources_accessed),pv=int(r.page_views),asub=int(r.assignment_submissions),tm=int(r.time_on_task_minutes),wa='[]') for r in lms.itertuples() if r.student_pseudonym in stu_map and r.course_code in crs_map and r.period_code in per_map]
        seen=set(); dedup=[]
        for r in lms_rows:
            k=(r['s'],r['c'],r['p'])
            if k in seen: continue
            seen.add(k); dedup.append(r)
        cx.execute(text('insert into lms_activity(student_id,course_id,period_id,logins_count,resources_accessed,page_views,assignment_submissions,time_on_task_minutes,weekly_activity) values (:s,:c,:p,:lc,:ra,:pv,:asub,:tm,:wa)'), dedup)
        counts={t:cx.execute(text(f'select count(*) from {t}')).scalar() for t in ['departments','programmes','courses','academic_periods','students','course_enrolments','attendance_records','assessment_records','lms_activity','academic_history']}
    print(json.dumps({'status':'ok','dataset':'synthetic_buse_demo','counts':counts}, indent=2))

if __name__=='__main__': run()
