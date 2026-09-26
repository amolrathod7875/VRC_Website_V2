from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.faq import Faq
from app.schemas.faq import FaqResponse

router = APIRouter()


@router.get("", response_model=list[FaqResponse])
async def list_faqs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Faq).where(Faq.is_active == True).order_by(Faq.display_order))
    return result.scalars().all()


@router.get("/category/{category}", response_model=list[FaqResponse])
async def list_faqs_by_category(category: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Faq).where(Faq.category == category, Faq.is_active == True).order_by(Faq.display_order))
    return result.scalars().all()
