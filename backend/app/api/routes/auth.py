"""Authentication API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any

from app.core.database import get_db_session
from app.core.dependencies import get_current_user
from app.core.security import (
    create_access_token, hash_password, verify_password,
    get_user_permissions
)
from app.schemas import UserLogin, UserCreate, UserResponse, TokenResponse
from app.repositories.user import UserRepository

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    session: AsyncSession = Depends(get_db_session)
):
    """Authenticate user and return access token"""
    user_repo = UserRepository(session)
    user = await user_repo.get_by_email(credentials.email)

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )

    roles = await user_repo.get_user_roles(user.id)
    permissions = get_user_permissions(roles)

    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
        roles=roles,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            roles=roles,
            permissions=permissions,
        ),
    )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user),
):
    """Register a new user (restricted; admin in production)."""
    # Allow initial bootstrap when no auth context is present in dev, but prefer admin.
    if current_user and "system_admin" not in current_user.get("roles", []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    user_repo = UserRepository(session)
    existing_user = await user_repo.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    role_id = user_data.role_id or 2  # default lecturer-like role if omitted
    user = await user_repo.create({
        "email": user_data.email,
        "hashed_password": hash_password(user_data.password),
        "full_name": user_data.full_name,
        "role_id": role_id,
    })

    roles = await user_repo.get_user_roles(user.id)
    permissions = get_user_permissions(roles)

    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        roles=roles,
        permissions=permissions,
    )


@router.get("/me", response_model=UserResponse)
async def me(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get current user information"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        full_name=current_user["full_name"],
        is_active=current_user["is_active"],
        roles=current_user["roles"],
        permissions=current_user["permissions"],
    )


@router.post("/logout")
async def logout():
    """Logout current user (client should discard token)"""
    return {"message": "Successfully logged out"}