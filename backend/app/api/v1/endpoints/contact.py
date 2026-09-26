from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.contact_submission import ContactSubmission
from app.schemas.contact import ContactSubmissionResponse, ContactSubmissionCreate

router = APIRouter()


@router.post("", response_model=ContactSubmissionResponse, status_code=201)
async def submit_contact(payload: ContactSubmissionCreate, db: AsyncSession = Depends(get_db)):
    submission = ContactSubmission(**payload.model_dump())
    db.add(submission)
    await db.commit()
    await db.refresh(submission)
    return submission
