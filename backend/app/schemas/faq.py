from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional


class FaqBase(BaseModel):
    category: str
    question: str
    answer: str
    display_order: int = 0
    is_active: bool = True


class FaqCreate(FaqBase):
    pass


class FaqResponse(FaqBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
