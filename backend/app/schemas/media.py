from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional


class MediaAssetBase(BaseModel):
    filename: str
    original_filename: str
    media_type: str
    mime_type: str
    storage_path: str
    public_url: str
    alt_text: Optional[str] = None
    title: Optional[str] = None
    size_bytes: Optional[int] = None
    checksum: Optional[str] = None


class MediaAssetCreate(MediaAssetBase):
    pass


class MediaAssetResponse(MediaAssetBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
