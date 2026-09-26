from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.industry import Industry
from app.schemas.industry import IndustryResponse

router = APIRouter()


@router.get("", response_model=list[IndustryResponse])
async def list_industries(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Industry).order_by(Industry.display_order))
    return result.scalars().all()


@router.get("/{slug}", response_model=IndustryResponse)
async def get_industry(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Industry).where(Industry.slug == slug))
    industry = result.scalar_one_or_none()
    if not industry:
        raise HTTPException(status_code=404, detail="Industry not found")
    return industry
