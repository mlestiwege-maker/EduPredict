"""Core dependencies"""
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
import logging
from app.core.database import get_db_session
from app.core.security import decode_token, get_user_permissions
from app.repositories.user import UserRepository

logger = logging.getLogger(__name__)
security_scheme = HTTPBearer(auto_error=False)

async def get_current_user(request: Request, credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme), session=Depends(get_db_session)) -> Optional[Dict[str, Any]]:
    token = None
    if credentials and credentials.credentials:
        token = credentials.credentials
    elif "authorization" in request.headers:
        h = request.headers["authorization"]
        if h.lower().startswith("bearer "): token = h.split(" ",1)[1].strip()
    if not token: return None
    payload = decode_token(token)
    if not payload: return None
    try:
        user_id = int(payload.sub) if getattr(payload,'sub',None) is not None else None
    except Exception:
        user_id = None
    if not user_id: return None
    user_repo = UserRepository(session)
    user = await user_repo.get_by_id(user_id)
    if not user or not getattr(user,'is_active',True): return None
    roles = await user_repo.get_user_roles(user.id)
    permissions = get_user_permissions(roles)
    return {"id": user.id, "email": user.email, "full_name": user.full_name, "is_active": user.is_active, "roles": roles, "permissions": permissions}

async def require_user(current_user: Optional[Dict[str, Any]] = Depends(get_current_user)) -> Dict[str, Any]:
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return current_user

def require_permission(permission: str):
    async def dep(current_user: Dict[str, Any] = Depends(require_user)):
        if not current_user.get('permissions',{}).get(permission):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Missing permission: {permission}")
        return current_user
    return dep
