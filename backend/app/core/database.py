from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator, Optional
from app.core.config import settings

_engine: Optional[object] = None
_async_session_factory: Optional[object] = None
Base = declarative_base()


def _get_engine():
    global _engine
    if _engine is None:
        if not settings.DATABASE_URL:
            raise RuntimeError("DATABASE_URL not configured")
        _engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
    return _engine


def _get_session_factory():
    global _async_session_factory
    if _async_session_factory is None:
        _async_session_factory = async_sessionmaker(_get_engine(), class_=AsyncSession, expire_on_commit=False)
    return _async_session_factory


class _LazySessionFactory:
    """Lazy callable that defers to _get_session_factory, allowing mock at import time."""
    def __call__(self):
        return _get_session_factory()


# Backward-compatible alias for legacy scripts/tests
async_session_factory = _LazySessionFactory()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    if not settings.DATABASE_URL:
        raise RuntimeError("DATABASE_URL not configured")
    async with _get_session_factory()() as session:
        yield session