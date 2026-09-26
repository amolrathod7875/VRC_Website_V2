from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.media_asset import MediaAsset
from app.schemas.media import MediaAssetResponse

router = APIRouter()


@router.get("/{asset_id}", response_model=MediaAssetResponse)
async def get_media_asset(asset_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MediaAsset).where(MediaAsset.id == asset_id))
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Media asset not found")
    return asset
