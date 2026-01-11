"""Tests for authentication API endpoints."""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.main import app


# Use async in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestAsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_db():
    """Override get_db dependency for testing."""
    async with TestAsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# Override the dependency
app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database():
    """Create tables before each test and drop after."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client():
    """Async test client fixture."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestRegistration:
    """Test cases for user registration endpoint."""

    @pytest.mark.asyncio
    async def test_register_success(self, client):
        """Test successful user registration."""
        response = await client.post(
            "/api/auth/register",
            json={"username": "testuser", "password": "testpass123"},
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["username"] == "testuser"
        assert "password" not in data
        assert "hashed_password" not in data

    @pytest.mark.asyncio
    async def test_register_duplicate_username(self, client):
        """Test registration with duplicate username returns 409."""
        # First registration
        response1 = await client.post(
            "/api/auth/register",
            json={"username": "duplicateuser", "password": "pass1"},
        )
        assert response1.status_code == 201

        # Second registration with same username
        response2 = await client.post(
            "/api/auth/register",
            json={"username": "duplicateuser", "password": "pass2"},
        )
        assert response2.status_code == 409
        assert "already registered" in response2.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_register_invalid_input_missing_username(self, client):
        """Test registration with missing username returns 422."""
        response = await client.post(
            "/api/auth/register",
            json={"password": "testpass123"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_invalid_input_missing_password(self, client):
        """Test registration with missing password returns 422."""
        response = await client.post(
            "/api/auth/register",
            json={"username": "testuser"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_username_too_short(self, client):
        """Test registration with username too short returns 422."""
        response = await client.post(
            "/api/auth/register",
            json={"username": "ab", "password": "testpass123"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_username_too_long(self, client):
        """Test registration with username too long returns 422."""
        long_username = "a" * 51
        response = await client.post(
            "/api/auth/register",
            json={"username": long_username, "password": "testpass123"},
        )
        assert response.status_code == 422

