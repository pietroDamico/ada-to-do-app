import logging
import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

load_dotenv()

logger = logging.getLogger(__name__)

# Default to local SQLite for development/testing; override via DATABASE_URL.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./dev.db")
if DATABASE_URL.startswith("postgresql://"):
    # Ensure async driver is used even if a sync URL is provided.
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session for request-scoped usage."""
    async with AsyncSessionLocal() as session:
        yield session


async def test_connection() -> None:
    """Verify the database connection at startup."""
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        logger.info("Database connection successful")
    except Exception:
        logger.exception("Database connection failed")
        raise


async def close_engine() -> None:
    """Dispose the async engine on shutdown."""
    await engine.dispose()

