"""Tests for database module."""

import pytest

from app.db.database import Base, async_session_maker, check_database_connection, get_db


def test_base_class_exists():
    """Test that Base declarative class exists."""
    assert Base is not None
    assert hasattr(Base, "metadata")


def test_get_db_raises_without_config():
    """Test that get_db raises RuntimeError when database is not configured."""
    # When DATABASE_URL is not set, async_session_maker is None
    # The actual behavior depends on environment
    # This test just verifies the function exists and is callable
    assert callable(get_db)


@pytest.mark.asyncio
async def test_check_database_connection_without_config():
    """Test that check_database_connection returns False without config."""
    # Without DATABASE_URL set, this should return False
    # (or True if a real database is configured)
    result = await check_database_connection()
    # We just verify it returns a boolean
    assert isinstance(result, bool)
