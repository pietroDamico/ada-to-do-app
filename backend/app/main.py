"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.db.database import check_database_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup and shutdown events.

    Args:
        app: The FastAPI application instance.

    Yields:
        None: Control to the application.
    """
    # Startup
    logger.info("Starting up To-Do App API...")
    db_connected = await check_database_connection()
    if db_connected:
        logger.info("Database connection: SUCCESS")
    else:
        logger.warning("Database connection: FAILED (API will run but database operations will fail)")

    yield

    # Shutdown
    logger.info("Shutting down To-Do App API...")


app = FastAPI(
    title="To-Do App API",
    description="Backend API for the To-Do application",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health_check() -> dict:
    """Health check endpoint.

    Returns:
        dict: Status response indicating the API is operational.
    """
    return {"status": "ok"}
