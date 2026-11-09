"""API route definitions"""

from fastapi import APIRouter, Depends

from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.academic import router as academic_router
from app.api.routes.data_import import router as data_import_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.predictions import router as predictions_router
from app.api.routes.recommendations import router as recommendations_router
from app.api.routes.reports import router as reports_router
from app.api.routes.audit import router as audit_router
from app.api.routes.dashboard import router as dashboard_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(academic_router, prefix="/academic", tags=["Academic Structure"])
api_router.include_router(data_import_router, prefix="/data-import", tags=["Data Import"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(predictions_router, prefix="/predictions", tags=["Predictions"])
api_router.include_router(recommendations_router, prefix="/recommendations", tags=["Recommendations"])
api_router.include_router(reports_router, prefix="/reports", tags=["Reports"])
api_router.include_router(audit_router, prefix="/audit", tags=["Audit"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])