from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, Numeric, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.base import UUIDMixin, TimestampMixin


class Job(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "jobs"

    slug = Column(String(255), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    department = Column(String(255), nullable=False, index=True)
    employment_type = Column(String(100))
    locations = Column(JSON)
    experience = Column(String(255))
    salary = Column(String(255))
    qualification = Column(Text)
    summary = Column(Text)
    description = Column(Text)
    skills = Column(JSON)
    sections = Column(JSON)
    posted_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True, nullable=False)

    applications = relationship("JobApplication", back_populates="job", cascade="all, delete-orphan")


class JobApplication(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "job_applications"

    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50))
    preferred_location = Column(String(255))
    experience = Column(String(255))
    message = Column(Text)
    resume_asset_id = Column(UUID(as_uuid=True), ForeignKey("media_assets.id"))
    status = Column(String(50), default="pending", nullable=False)

    job = relationship("Job", back_populates="applications")
