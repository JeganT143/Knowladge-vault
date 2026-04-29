from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    echo=settings.debug,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


class Base(DeclarativeBase):
    pass
