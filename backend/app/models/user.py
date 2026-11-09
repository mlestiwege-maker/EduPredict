"""User and role models"""

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Role(Base, TimestampMixin):
    """System roles with specific permissions"""
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255))
    is_active = Column(Boolean, default=True)

    users = relationship("User", back_populates="role", cascade="all, delete-orphan")


class User(Base, TimestampMixin):
    """System users (staff members)"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, index=True)

    role = relationship("Role", back_populates="users")
    interventions = relationship("Intervention", back_populates="staff")
    audit_logs = relationship("AuditLog", back_populates="user")
    report_jobs = relationship("ReportJob", back_populates="user")


class UserRole(Base, TimestampMixin):
    """Many-to-many relationship for users with multiple roles"""
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    role_id = Column(Integer, nullable=False, index=True)
    is_primary = Column(Boolean, default=False)