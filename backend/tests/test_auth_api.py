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


class TestLogin:
    """Test cases for user login endpoint."""

    @pytest.mark.asyncio
    async def test_login_success(self, client):
        """Test successful login returns JWT token."""
        # First register a user
        await client.post(
            "/api/auth/register",
            json={"username": "loginuser", "password": "testpass123"},
        )

        # Then login
        response = await client.post(
            "/api/auth/login",
            json={"username": "loginuser", "password": "testpass123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0

    @pytest.mark.asyncio
    async def test_login_invalid_username(self, client):
        """Test login with non-existent username returns 401."""
        response = await client.post(
            "/api/auth/login",
            json={"username": "nonexistent", "password": "testpass123"},
        )
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_login_invalid_password(self, client):
        """Test login with wrong password returns 401."""
        # First register a user
        await client.post(
            "/api/auth/register",
            json={"username": "wrongpassuser", "password": "correctpass"},
        )

        # Try to login with wrong password
        response = await client.post(
            "/api/auth/login",
            json={"username": "wrongpassuser", "password": "wrongpass"},
        )
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_login_token_contains_user_id(self, client):
        """Test that login token contains user_id claim."""
        from app.core.security import decode_access_token

        # Register and login
        register_response = await client.post(
            "/api/auth/register",
            json={"username": "tokenuser", "password": "testpass123"},
        )
        user_id = register_response.json()["id"]

        login_response = await client.post(
            "/api/auth/login",
            json={"username": "tokenuser", "password": "testpass123"},
        )
        token = login_response.json()["access_token"]

        # Decode and verify token
        payload = decode_access_token(token)
        assert payload is not None
        assert payload["sub"] == str(user_id)


class TestGetCurrentUser:
    """Test cases for JWT auth dependency (get_current_user) via /me endpoint."""

    @pytest.mark.asyncio
    async def test_get_me_with_valid_token(self, client):
        """Test /me endpoint returns current user with valid JWT."""
        # Register and login to get token
        register_response = await client.post(
            "/api/auth/register",
            json={"username": "meuser", "password": "testpass123"},
        )
        user_id = register_response.json()["id"]

        login_response = await client.post(
            "/api/auth/login",
            json={"username": "meuser", "password": "testpass123"},
        )
        token = login_response.json()["access_token"]

        # Call /me with valid token
        response = await client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == "meuser"

    @pytest.mark.asyncio
    async def test_get_me_missing_token(self, client):
        """Test /me endpoint returns 403 without Authorization header."""
        response = await client.get("/api/auth/me")
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_get_me_invalid_token(self, client):
        """Test /me endpoint returns 401 with invalid JWT."""
        response = await client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalidtoken123"},
        )
        assert response.status_code == 401
        assert "credentials" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_get_me_expired_token(self, client):
        """Test /me endpoint returns 401 with expired JWT."""
        from datetime import timedelta
        from app.core.security import create_access_token

        # Create an already expired token
        expired_token = create_access_token(
            data={"sub": "1"},
            expires_delta=timedelta(seconds=-1),  # Already expired
        )

        response = await client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {expired_token}"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_me_token_for_nonexistent_user(self, client):
        """Test /me endpoint returns 401 when user_id in token doesn't exist."""
        from app.core.security import create_access_token

        # Create a token for a user ID that doesn't exist
        fake_token = create_access_token(data={"sub": "99999"})

        response = await client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {fake_token}"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_me_token_missing_sub_claim(self, client):
        """Test /me endpoint returns 401 when token has no 'sub' claim."""
        from app.core.security import create_access_token

        # Create a token without user_id claim
        bad_token = create_access_token(data={"foo": "bar"})

        response = await client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {bad_token}"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_me_token_invalid_sub_format(self, client):
        """Test /me endpoint returns 401 when sub claim is not a valid int."""
        from app.core.security import create_access_token

        # Create a token with non-integer sub claim
        bad_token = create_access_token(data={"sub": "not-a-number"})

        response = await client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {bad_token}"},
        )
        assert response.status_code == 401

