from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, Numeric, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.base import UUIDMixin, TimestampMixin


class Blog(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "blogs"

    slug = Column(String(255), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    excerpt = Column(Text)
    content = Column(Text)
    hero_image_id = Column(UUID(as_uuid=True), ForeignKey("media_assets.id"))
    status = Column(String(50), default="draft", nullable=False, index=True)
    published_at = Column(DateTime(timezone=True))
