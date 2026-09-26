from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional, Any


class PartnerBase(BaseModel):
    slug: str
    name: str
    country: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    products: Optional[list[str] | dict[str, Any]] = None
    highlights: Optional[list[str] | dict[str, Any]] = None
    display_order: int = 0


class PartnerCreate(PartnerBase):
    pass


class PartnerResponse(PartnerBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    logo_asset_id: Optional[UUID] = None
