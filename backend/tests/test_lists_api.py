import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.db.database import AsyncSessionLocal
from app.models.todo import TodoList
from app.models.user import User


@pytest.mark.asyncio
async def test_create_list(async_client: AsyncClient, auth_headers: dict[str, str]):
    response = await async_client.post(
        "/api/lists", json={"title": "Chores"}, headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Chores"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_only_returns_owned_lists(
    async_client: AsyncClient, auth_headers: dict[str, str], user: User
):
    async with AsyncSessionLocal() as session:
        other_user = User(username="other", hashed_password="pw")
        session.add(other_user)
        await session.flush()
        session.add(TodoList(title="Other list", user_id=other_user.id))
        await session.commit()

    await async_client.post(
        "/api/lists", json={"title": "Mine"}, headers=auth_headers
    )

    response = await async_client.get("/api/lists", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Mine"


@pytest.mark.asyncio
async def test_get_list_respects_ownership(
    async_client: AsyncClient, auth_headers: dict[str, str]
):
    create_resp = await async_client.post(
        "/api/lists", json={"title": "Private"}, headers=auth_headers
    )
    list_id = create_resp.json()["id"]

    response = await async_client.get(f"/api/lists/{list_id}", headers=auth_headers)
    assert response.status_code == 200

    other_headers = {"Authorization": "Bearer 999"}
    response_other = await async_client.get(
        f"/api/lists/{list_id}", headers=other_headers
    )
    assert response_other.status_code == 401


@pytest.mark.asyncio
async def test_update_list(async_client: AsyncClient, auth_headers: dict[str, str]):
    create_resp = await async_client.post(
        "/api/lists", json={"title": "Temp"}, headers=auth_headers
    )
    list_id = create_resp.json()["id"]

    response = await async_client.put(
        f"/api/lists/{list_id}",
        json={"title": "Updated"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


@pytest.mark.asyncio
async def test_delete_list(async_client: AsyncClient, auth_headers: dict[str, str]):
    create_resp = await async_client.post(
        "/api/lists", json={"title": "To Delete"}, headers=auth_headers
    )
    list_id = create_resp.json()["id"]

    delete_resp = await async_client.delete(
        f"/api/lists/{list_id}", headers=auth_headers
    )
    assert delete_resp.status_code == 204

    # Ensure it is gone
    async with AsyncSessionLocal() as session:
        missing = await session.get(TodoList, list_id)
        assert missing is None
