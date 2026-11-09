"""User data access layer"""

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.models.user import User, Role, UserRole


class UserRepository:
    """Data access for users and roles"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create(self, user_data: dict) -> User:
        """Create a new user"""
        user = User(**user_data)
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def update(self, user_id: int, user_data: dict) -> User:
        """Update a user"""
        await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(**user_data)
        )
        user = await self.get_by_id(user_id)
        return user

    async def delete(self, user_id: int) -> None:
        """Delete a user"""
        await self.session.execute(
            delete(User).where(User.id == user_id)
        )

    async def list(self, skip: int = 0, limit: int = 100) -> List[User]:
        """List users with pagination"""
        result = await self.session.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_user_roles(self, user_id: int) -> List[str]:
        """Get role names for a user"""
        result = await self.session.execute(
            select(Role.name)
            .join(User, User.role_id == Role.id)
            .where(User.id == user_id)
        )
        return [row[0] for row in result.all()]