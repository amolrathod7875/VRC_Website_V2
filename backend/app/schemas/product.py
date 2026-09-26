from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional, List, Any


class ProductBase(BaseModel):
    slug: str
    name: str
    category: str
    subcategory: Optional[str] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    catalogue_asset_id: Optional[UUID] = None
    primary_image_asset_id: Optional[UUID] = None


class ProductVariantBase(BaseModel):
    product_id: UUID
    model_number: Optional[str] = None
    name: str
    description: Optional[str] = None
    display_order: int = 0
    technical_specs: Optional[dict[str, Any] | list[Any]] = None
    features: Optional[dict[str, Any] | list[Any]] = None
    applications: Optional[dict[str, Any] | list[Any]] = None
    image_asset_id: Optional[UUID] = None


class ProductVariantCreate(ProductVariantBase):
    pass


class ProductVariantResponse(ProductVariantBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime


class ProductDetailResponse(ProductResponse):
    model_config = ConfigDict(from_attributes=True)

    variants: List[ProductVariantResponse] = []
