from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title="VR Coatings API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

media_root = Path(settings.MEDIA_ROOT)
if media_root.exists():
    app.mount(settings.MEDIA_BASE_URL, StaticFiles(directory=str(media_root)), name="media")


@app.get("/health")
async def health_check():
    return {"status": "ok"}
