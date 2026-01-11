"""Database connection and session management."""

import logging
import os
from collections.abc import AsyncGenerator
from typing import Any

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "")

if not DATABASE_URL:
    logger.warning("DATABASE_URL not set. Database operations will fail.")


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


def _create_engine() -> Any:
    """Create async engine if DATABASE_URL is set."""
    if not DATABASE_URL:
        return None

    return create_async_engine(
        DATABASE_URL,
        echo=os.getenv("ENVIRONMENT", "development") == "development",
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,  # Enable connection health checks
    )


# Create async engine with connection pool settings
engine = _create_engine()

# Create session factory
async_session_maker: async_sessionmaker[AsyncSession] | None = None
if engine is not None:
    async_session_maker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that yields a database session.

    Yields:
        AsyncSession: An async database session.

    Raises:
        RuntimeError: If database is not configured.
    """
    if async_session_maker is None:
        raise RuntimeError("Database is not configured. Set DATABASE_URL environment variable.")

    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def check_database_connection() -> bool:
    """Test the database connection.

    Returns:
        bool: True if connection successful, False otherwise.
    """
    if engine is None:
        logger.error("Database engine not configured. Set DATABASE_URL environment variable.")
        return False

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection successful.")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False
