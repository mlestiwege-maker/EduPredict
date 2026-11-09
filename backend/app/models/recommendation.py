"""Recommendation and intervention models"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base, TimestampMixin


class RecommendationRule(Base, TimestampMixin):
    """Approved recommendation rules"""
    __tablename__ = "recommendation_rules"

    id = Column(Integer, primary_key=True, index=True)
    rule_code = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    condition_type = Column(String(50))  # attendance, assessment, engagement, workload, etc.
    condition_field = Column(String(100))
    condition_operator = Column(String(20))  # less_than, greater_than, between, etc.
    condition_value = Column(String(100))
    condition_value_2 = Column(String(100))
    action = Column(Text, nullable=False)
    responsible_role = Column(String(50))
    priority = Column(String(20), default="medium")  # high, medium, low
    is_active = Column(Boolean, default=True)
    requires_approval = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"))


class Recommendation(Base, TimestampMixin):
    """Recommendations generated for students"""
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    prediction_id = Column(Integer, ForeignKey("student_predictions.id"), nullable=False)
    rule_id = Column(Integer, ForeignKey("recommendation_rules.id"))
    action = Column(Text, nullable=False)
    responsible_role = Column(String(50))
    priority = Column(String(20), default="medium")
    status = Column(String(20), default="pending")  # pending, accepted, rejected, completed
    staff_notes = Column(Text)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="recommendations")
    prediction = relationship("StudentPrediction", back_populates="recommendations")
    rule = relationship("RecommendationRule")
    interventions = relationship("Intervention", back_populates="recommendation")


class Intervention(Base, TimestampMixin):
    """Academic interventions recorded by staff"""
    __tablename__ = "interventions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    recommendation_id = Column(Integer, ForeignKey("recommendations.id"))
    staff_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    intervention_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    action_taken = Column(Text)
    status = Column(String(20), default="planned")  # planned, in_progress, completed, cancelled
    start_date = Column(DateTime(timezone=True))
    completion_date = Column(DateTime(timezone=True))
    follow_up_date = Column(DateTime(timezone=True))
    outcome = Column(Text)
    effectiveness_rating = Column(Integer)  # 1-5 scale
    notes = Column(Text)

    student = relationship("Student")
    recommendation = relationship("Recommendation", back_populates="interventions")
    staff = relationship("User", back_populates="interventions")
    followups = relationship("InterventionFollowup", back_populates="intervention")


class InterventionFollowup(Base, TimestampMixin):
    """Follow-up records for interventions"""
    __tablename__ = "intervention_followups"

    id = Column(Integer, primary_key=True, index=True)
    intervention_id = Column(Integer, ForeignKey("interventions.id"), nullable=False)
    staff_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    follow_up_date = Column(DateTime(timezone=True), nullable=False)
    actual_date = Column(DateTime(timezone=True))
    status = Column(String(20), default="scheduled")  # scheduled, completed, missed
    notes = Column(Text)
    student_response = Column(Text)
    next_steps = Column(Text)

    intervention = relationship("Intervention", back_populates="followups")
    staff = relationship("User")