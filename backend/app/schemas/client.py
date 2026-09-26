from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional


class ClientBase(BaseModel):
    name: str
    industry: str
    website: Optional[str] = None
    display_order: int = 0
    is_active: bool = True


class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    logo_asset_id: Optional[UUID] = None
