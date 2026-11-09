"""Report generation models"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base, TimestampMixin


class ReportJob(Base, TimestampMixin):
    """Track report generation requests"""
    __tablename__ = "report_jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    report_type = Column(String(50), nullable=False)  # lecturer, advisor, hod, dean, registry
    report_format = Column(String(20), nullable=False)  # pdf, excel, dashboard
    title = Column(String(255), nullable=False)
    parameters = Column(JSON)  # filters like period_id, course_id, department_id
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    file_path = Column(String(500))
    file_size = Column(Integer, default=0)
    generated_at = Column(DateTime(timezone=True))
    error_message = Column(Text)

    user = relationship("User", back_populates="report_jobs")