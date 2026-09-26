from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.partner import Partner
from app.schemas.partner import PartnerResponse

router = APIRouter()


@router.get("", response_model=list[PartnerResponse])
async def list_partners(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Partner).order_by(Partner.display_order))
    return result.scalars().all()


@router.get("/{slug}", response_model=PartnerResponse)
async def get_partner(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Partner).where(Partner.slug == slug))
    partner = result.scalar_one_or_none()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    return partner
