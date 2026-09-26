from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.application import Application
from app.schemas.application import ApplicationResponse

router = APIRouter()


@router.get("", response_model=list[ApplicationResponse])
async def list_applications(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Application).order_by(Application.display_order))
    return result.scalars().all()


@router.get("/{slug}", response_model=ApplicationResponse)
async def get_application(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Application).where(Application.slug == slug))
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app
