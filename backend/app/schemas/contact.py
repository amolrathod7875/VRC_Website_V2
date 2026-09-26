from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional


class ContactSubmissionBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    subject: Optional[str] = None
    message: str


class ContactSubmissionCreate(ContactSubmissionBase):
    pass


class ContactSubmissionResponse(ContactSubmissionBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    status: str
