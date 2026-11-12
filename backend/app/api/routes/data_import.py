"""Data import API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import json
from pathlib import Path
from app.core.database import get_db_session
from app.core.dependencies import require_user
from app.services.data_import_service import DataImportService
from app.schemas import DataImportResponse, DataQualityIssueResponse
router = APIRouter()

@router.get('/datasets')
async def list_datasets(current_user=Depends(require_user)):
    
    base=Path(__file__).resolve().parents[4]/'ml/data/sample/buse'
    meta=json.loads((base/'README.json').read_text()) if (base/'README.json').exists() else {}
    return {'institutional_datasets':[{'name':'BUSE institutional','path':str(base),'files':[p.name for p in base.glob('*.csv')],'meta':meta}],'recommended_public_datasets':[{'name':'Open University Learning Analytics Dataset (OULAD)','why':'LMS + assessments + outcomes; strong EDM benchmark'},{'name':'UCI Student Performance (Cortez & Silva)','why':'Small benchmark for pass/fail/regression'},{'name':'UCI Higher Education Students Performance','why':'Tertiary-oriented attributes (verify version/provenance)'},{'name':'xAPI-Edu-Data / Kaggle education sets','why':'Quick prototyping; check licenses and schema fit'}]}

@router.post('/load-demo')
async def load_demo(current_user=Depends(require_user)):
    
    import subprocess, sys
    root=Path(__file__).resolve().parents[4]
    p=subprocess.run([sys.executable, str(root/'backend/scripts/load_buse_demo.py')], capture_output=True, text=True, cwd=str(root))
    if p.returncode!=0: return {'status':'error','error':(p.stderr or p.stdout)[-1200:]}
    try: return json.loads(p.stdout.strip().splitlines()[-1])
    except Exception: return {'status':'ok','raw':p.stdout[-800:]}

@router.post('/upload', response_model=DataImportResponse)
async def upload_file(file: UploadFile = File(...), file_type: str = Form(...), current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    
    result = await DataImportService(session).upload_and_process(file, file_type, current_user['id'])
    return DataImportResponse(id=result.id, filename=result.filename, file_type=result.file_type, status=result.status, total_rows=result.total_rows, accepted_rows=result.accepted_rows, rejected_rows=result.rejected_rows, warning_rows=result.warning_rows, error_message=result.error_message)

@router.get('/', response_model=list[DataImportResponse])
async def list_imports(skip: int = 0, limit: int = 50, current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    
    imports = await DataImportService(session).list_imports(skip=skip, limit=limit)
    return [DataImportResponse(id=i.id, filename=i.filename, file_type=i.file_type, status=i.status, total_rows=i.total_rows, accepted_rows=i.accepted_rows, rejected_rows=i.rejected_rows, warning_rows=i.warning_rows, error_message=i.error_message) for i in imports]
