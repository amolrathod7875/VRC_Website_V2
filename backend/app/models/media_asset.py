from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, Numeric, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.base import UUIDMixin, TimestampMixin


class MediaAsset(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "media_assets"

    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    media_type = Column(String(50), nullable=False, index=True)
    mime_type = Column(String(100), nullable=False)
    storage_path = Column(String(512), nullable=False)
    public_url = Column(String(512), nullable=False)
    alt_text = Column(String(255))
    title = Column(String(255))
    size_bytes = Column(Integer)
    checksum = Column(String(64))
