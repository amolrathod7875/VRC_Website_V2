from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.client import Client
from app.schemas.client import ClientResponse

router = APIRouter()


@router.get("", response_model=list[ClientResponse])
async def list_clients(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Client).where(Client.is_active == True).order_by(Client.display_order))
    return result.scalars().all()
