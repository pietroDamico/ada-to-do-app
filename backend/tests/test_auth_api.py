import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_creates_user(async_client: AsyncClient):
    response = await async_client.post(
        "/api/auth/register", json={"username": "alice", "password": "password123"}
    )

    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "alice"
    assert "id" in body


@pytest.mark.asyncio
async def test_register_duplicate_username_returns_conflict(async_client: AsyncClient):
    first = await async_client.post(
        "/api/auth/register", json={"username": "bob", "password": "password123"}
    )
    assert first.status_code == 201

    duplicate = await async_client.post(
        "/api/auth/register", json={"username": "bob", "password": "password123"}
    )
    assert duplicate.status_code == 409


@pytest.mark.asyncio
async def test_login_returns_token(async_client: AsyncClient):
    await async_client.post(
        "/api/auth/register", json={"username": "carol", "password": "password123"}
    )

    response = await async_client.post(
        "/api/auth/login", json={"username": "carol", "password": "password123"}
    )

    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token

    me = await async_client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["username"] == "carol"


@pytest.mark.asyncio
async def test_login_invalid_credentials(async_client: AsyncClient):
    await async_client.post(
        "/api/auth/register", json={"username": "dave", "password": "password123"}
    )

    response = await async_client.post(
        "/api/auth/login", json={"username": "dave", "password": "wrongpassword"}
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_requires_valid_token(async_client: AsyncClient):
    response = await async_client.get("/api/auth/me")
    assert response.status_code == 401

    response = await async_client.get(
        "/api/auth/me", headers={"Authorization": "Bearer invalid-token"}
    )
    assert response.status_code == 401

