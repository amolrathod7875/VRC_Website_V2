from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, Numeric, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.base import UUIDMixin, TimestampMixin


class Industry(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "industries"

    slug = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    hero_media_id = Column(UUID(as_uuid=True), ForeignKey("media_assets.id"))
    content = Column(JSON)
    display_order = Column(Integer, default=0)
