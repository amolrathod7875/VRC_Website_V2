from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.media_asset import MediaAsset
from app.schemas.media import MediaAssetResponse
import os
from app.core.config import settings

router = APIRouter()


@router.get("/{asset_id}", response_model=MediaAssetResponse)
async def get_media_asset(asset_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MediaAsset).where(MediaAsset.id == asset_id))
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Media asset not found")
    return asset


@router.get("/serve/{path:path}")
async def serve_media(path: str):
    safe_path = os.path.normpath(path)
    if ".." in safe_path or safe_path.startswith("/"):
        raise HTTPException(status_code=403, detail="Invalid path")
    full_path = os.path.join(settings.MEDIA_ROOT, safe_path)
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(full_path)
