import logging
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings

logger = logging.getLogger("limi.db")

engine = None
async_session_factory = None


def _init_engine():
    global engine, async_session_factory
    if not settings.DATABASE_URL:
        logger.info("DATABASE_URL not set — running without database (seed data fallback)")
        return
    engine = create_async_engine(
        settings.DATABASE_URL,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        echo=settings.ENVIRONMENT == "development",
    )
    async_session_factory = async_sessionmaker(engine, expire_on_commit=False)
    logger.info("Database engine initialised")


_init_engine()


async def get_session() -> AsyncGenerator[AsyncSession | None, None]:
    """Yield a DB session, or None if no database is configured."""
    if async_session_factory is None:
        yield None
        return
    async with async_session_factory() as session:
        yield session


async def dispose_engine():
    """Dispose the engine on shutdown."""
    global engine
    if engine is not None:
        await engine.dispose()
        logger.info("Database engine disposed")
