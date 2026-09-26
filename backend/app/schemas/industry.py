from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional, Any


class IndustryBase(BaseModel):
    slug: str
    name: str
    description: Optional[str] = None
    content: Optional[dict[str, Any] | list[Any]] = None
    display_order: int = 0


class IndustryCreate(IndustryBase):
    pass


class IndustryResponse(IndustryBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    hero_media_id: Optional[UUID] = None
