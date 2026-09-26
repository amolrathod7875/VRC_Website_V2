from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.job import Job, JobApplication
from app.schemas.career import JobResponse, JobApplicationResponse, JobApplicationCreate

router = APIRouter()


@router.get("", response_model=list[JobResponse])
async def list_jobs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.is_active == True).order_by(Job.posted_at.desc()))
    return result.scalars().all()


@router.get("/{slug}", response_model=JobResponse)
async def get_job(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.slug == slug, Job.is_active == True))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/{job_id}/apply", response_model=JobApplicationResponse, status_code=201)
async def apply_job(job_id: str, payload: JobApplicationCreate, db: AsyncSession = Depends(get_db)):
    job = await db.get(Job, job_id)
    if not job or not job.is_active:
        raise HTTPException(status_code=404, detail="Job not found")
    application = JobApplication(**payload.model_dump())
    db.add(application)
    await db.commit()
    await db.refresh(application)
    return application
