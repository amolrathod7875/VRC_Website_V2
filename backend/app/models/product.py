from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, Numeric, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.base import UUIDMixin, TimestampMixin


class Product(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "products"

    slug = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False, index=True)
    subcategory = Column(String(255))
    short_description = Column(Text)
    description = Column(Text)
    catalogue_asset_id = Column(UUID(as_uuid=True), ForeignKey("media_assets.id"))
    primary_image_asset_id = Column(UUID(as_uuid=True), ForeignKey("media_assets.id"))
    is_active = Column(Boolean, default=True, nullable=False)
    display_order = Column(Integer, default=0)

    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")


class ProductVariant(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "product_variants"

    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    model_number = Column(String(255))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    display_order = Column(Integer, default=0)
    technical_specs = Column(JSON)
    features = Column(JSON)
    applications = Column(JSON)
    image_asset_id = Column(UUID(as_uuid=True), ForeignKey("media_assets.id"))

    product = relationship("Product", back_populates="variants")
