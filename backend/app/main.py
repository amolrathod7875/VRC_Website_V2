import re
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

_configured_media_root = Path(settings.MEDIA_ROOT)
_default_media_root = Path(__file__).resolve().parent.parent.parent / "storage"
media_root = _configured_media_root if _configured_media_root.exists() else _default_media_root

if media_root.exists():
    app.mount(settings.MEDIA_BASE_URL, StaticFiles(directory=str(media_root)), name="media")


_VERSIONED_QUERY_KEYS = ("v", "version", "hash")


def _is_versioned_media(path: str, query: str) -> bool:
    if any(f"{key}=" in query for key in _VERSIONED_QUERY_KEYS):
        return True
    filename = path.rsplit("/", 1)[-1]
    # Treat an 8+ character hexadecimal token in the filename as a content hash.
    return bool(re.search(r"(?<![0-9a-fA-F])[0-9a-fA-F]{8,}(?![0-9a-fA-F])", filename))


@app.middleware("http")
async def media_cache_headers(request, call_next):
    response = await call_next(request)
    if request.url.path.startswith(settings.MEDIA_BASE_URL):
        if _is_versioned_media(request.url.path, request.url.query):
            cache_control = "public, max-age=31536000, immutable"
        else:
            cache_control = "public, max-age=300, must-revalidate"
        response.headers["Cache-Control"] = cache_control
    return response


@app.get("/health")
async def health_check():
    return {"status": "ok"}
