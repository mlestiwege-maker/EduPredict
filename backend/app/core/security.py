"""Security utilities for authentication and authorization"""
from datetime import datetime, timedelta, timezone
from typing import Optional, List
from jose import JWTError, jwt
from passlib.hash import argon2
from pydantic import BaseModel
from app.core.config import settings

def hash_password(password: str) -> str:
    return argon2.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return argon2.verify(password, hashed)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: int
    email: str
    roles: List[str] = []
    exp: Optional[datetime] = None

def create_access_token(user_id: int, email: str, roles: List[str], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expires_minutes)
    exp = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": str(user_id), "email": email, "roles": roles, "exp": exp}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def decode_token(token: str) -> Optional[TokenPayload]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        sub = payload.get("sub")
        return TokenPayload(sub=int(sub), email=payload.get("email",""), roles=payload.get("roles", []) or [], exp=payload.get("exp"))
    except Exception:
        return None

ROLE_PERMISSIONS = {
    "system_admin": {"can_upload_data": True,"can_view_all_students": True,"can_view_aggregate_reports": True,"can_manage_users": True,"can_manage_models": True,"can_view_audit_logs": True,"can_record_interventions": True},
    "lecturer": {"can_upload_data": False,"can_view_all_students": False,"can_view_aggregate_reports": False,"can_manage_users": False,"can_manage_models": False,"can_view_audit_logs": False,"can_record_interventions": True,"can_view_assigned_courses": True},
    "academic_advisor": {"can_upload_data": False,"can_view_all_students": False,"can_view_aggregate_reports": False,"can_manage_users": False,"can_manage_models": False,"can_view_audit_logs": False,"can_record_interventions": True,"can_view_assigned_advisees": True},
    "head_of_department": {"can_upload_data": False,"can_view_all_students": False,"can_view_aggregate_reports": True,"can_manage_users": False,"can_manage_models": False,"can_view_audit_logs": False,"can_record_interventions": True,"can_view_department": True},
    "dean": {"can_upload_data": False,"can_view_all_students": False,"can_view_aggregate_reports": True,"can_manage_users": False,"can_manage_models": False,"can_view_audit_logs": False,"can_record_interventions": False,"can_view_faculty": True},
    "registry": {"can_upload_data": True,"can_view_all_students": False,"can_view_aggregate_reports": True,"can_manage_users": False,"can_manage_models": False,"can_view_audit_logs": True,"can_record_interventions": False,"can_view_institutional": True},
}

def has_permission(user_roles: List[str], permission: str) -> bool:
    for role in user_roles:
        if ROLE_PERMISSIONS.get(role, {}).get(permission, False): return True
    return False

def get_user_permissions(user_roles: List[str]) -> dict:
    permissions = {}
    for role in user_roles:
        for k,v in ROLE_PERMISSIONS.get(role, {}).items():
            permissions[k] = permissions.get(k, False) or v
    return permissions
