"""Audit logging model"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base, TimestampMixin


class AuditLog(Base, TimestampMixin):
    """Security audit trail"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(Integer)
    ip_address = Column(String(50))
    user_agent = Column(Text)
    details = Column(JSON)
    severity = Column(String(20), default="info")  # info, warning, error
    status = Column(String(20), default="success")  # success, failed

    user = relationship("User", back_populates="audit_logs")