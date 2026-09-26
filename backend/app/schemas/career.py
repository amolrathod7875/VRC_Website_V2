from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional, Any


class JobBase(BaseModel):
    slug: str
    title: str
    department: str
    employment_type: Optional[str] = None
    locations: Optional[list[str] | dict[str, Any]] = None
    experience: Optional[str] = None
    salary: Optional[str] = None
    qualification: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    skills: Optional[list[str] | dict[str, Any]] = None
    sections: Optional[dict[str, Any] | list[Any]] = None
    is_active: bool = True


class JobCreate(JobBase):
    pass


class JobResponse(JobBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    posted_at: Optional[datetime] = None


class JobApplicationBase(BaseModel):
    job_id: UUID
    name: str
    email: str
    phone: Optional[str] = None
    preferred_location: Optional[str] = None
    experience: Optional[str] = None
    message: Optional[str] = None


class JobApplicationCreate(JobApplicationBase):
    pass


class JobApplicationResponse(JobApplicationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    status: str
    resume_asset_id: Optional[UUID] = None
