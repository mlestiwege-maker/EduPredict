"""User management API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.core.security import get_user_permissions
from app.core.dependencies import require_user
from app.repositories.user import UserRepository
from app.schemas import UserResponse
router = APIRouter()

@router.get('/', response_model=list[UserResponse])
async def list_users(skip: int = Query(0, ge=0), limit: int = Query(200, ge=1, le=1000), current_user=Depends(require_user), session: AsyncSession = Depends(get_db_session)):
    user_repo = UserRepository(session); users = await user_repo.list(skip=skip, limit=limit)
    result=[]
    for user in users:
        roles = await user_repo.get_user_roles(user.id); perms = get_user_permissions(roles)
        result.append(UserResponse(id=user.id,email=user.email,full_name=user.full_name,is_active=user.is_active,roles=roles,permissions=perms))
    return result
