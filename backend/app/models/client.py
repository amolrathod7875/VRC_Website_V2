from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, Numeric, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.base import UUIDMixin, TimestampMixin


class Client(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "clients"

    name = Column(String(255), nullable=False)
    industry = Column(String(255), nullable=False, index=True)
    logo_asset_id = Column(UUID(as_uuid=True), ForeignKey("media_assets.id"))
    website = Column(String(512))
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True, nullable=False)
