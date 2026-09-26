from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.blog import Blog
from app.schemas.blog import BlogResponse

router = APIRouter()


@router.get("", response_model=list[BlogResponse])
async def list_blogs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Blog).where(Blog.status == "published").order_by(Blog.published_at.desc()))
    return result.scalars().all()


@router.get("/{slug}", response_model=BlogResponse)
async def get_blog(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Blog).where(Blog.slug == slug, Blog.status == "published"))
    blog = result.scalar_one_or_none()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog
