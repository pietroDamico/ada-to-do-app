import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.db.database import AsyncSessionLocal
from app.models.todo import TodoItem, TodoList
from app.models.user import User


async def _create_list(async_client: AsyncClient, headers: dict[str, str]) -> int:
    resp = await async_client.post("/api/lists", json={"title": "List"}, headers=headers)
    return resp.json()["id"]


@pytest.mark.asyncio
async def test_create_item(async_client: AsyncClient, auth_headers: dict[str, str]):
    list_id = await _create_list(async_client, auth_headers)
    response = await async_client.post(
        f"/api/lists/{list_id}/items",
        json={"title": "Buy eggs"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy eggs"
    assert data["completed"] is False
    assert data["list_id"] == list_id


@pytest.mark.asyncio
async def test_list_items(async_client: AsyncClient, auth_headers: dict[str, str]):
    list_id = await _create_list(async_client, auth_headers)
    await async_client.post(
        f"/api/lists/{list_id}/items",
        json={"title": "First"},
        headers=auth_headers,
    )
    await async_client.post(
        f"/api/lists/{list_id}/items",
        json={"title": "Second"},
        headers=auth_headers,
    )

    response = await async_client.get(
        f"/api/lists/{list_id}/items", headers=auth_headers
    )
    assert response.status_code == 200
    titles = [item["title"] for item in response.json()]
    assert titles == ["First", "Second"]


@pytest.mark.asyncio
async def test_update_item(async_client: AsyncClient, auth_headers: dict[str, str]):
    list_id = await _create_list(async_client, auth_headers)
    create_resp = await async_client.post(
        f"/api/lists/{list_id}/items",
        json={"title": "Toggle me"},
        headers=auth_headers,
    )
    item_id = create_resp.json()["id"]

    update_resp = await async_client.put(
        f"/api/items/{item_id}",
        json={"completed": True, "title": "Updated title"},
        headers=auth_headers,
    )
    assert update_resp.status_code == 200
    body = update_resp.json()
    assert body["completed"] is True
    assert body["title"] == "Updated title"


@pytest.mark.asyncio
async def test_delete_item(async_client: AsyncClient, auth_headers: dict[str, str]):
    list_id = await _create_list(async_client, auth_headers)
    create_resp = await async_client.post(
        f"/api/lists/{list_id}/items",
        json={"title": "Remove me"},
        headers=auth_headers,
    )
    item_id = create_resp.json()["id"]

    delete_resp = await async_client.delete(
        f"/api/items/{item_id}", headers=auth_headers
    )
    assert delete_resp.status_code == 204

    async with AsyncSessionLocal() as session:
        missing = await session.get(TodoItem, item_id)
        assert missing is None


@pytest.mark.asyncio
async def test_cannot_access_other_users_items(
    async_client: AsyncClient, user: User, auth_headers: dict[str, str]
):
    async with AsyncSessionLocal() as session:
        other_user = User(username="someone", hashed_password="pw")
        session.add(other_user)
        await session.flush()
        other_list = TodoList(title="Other list", user_id=other_user.id)
        session.add(other_list)
        await session.flush()
        other_item = TodoItem(title="Hidden", list_id=other_list.id)
        session.add(other_item)
        await session.commit()
        other_item_id = other_item.id

    response = await async_client.put(
        f"/api/items/{other_item_id}",
        json={"completed": True},
        headers=auth_headers,
    )
    assert response.status_code in (404, 401)

    response_delete = await async_client.delete(
        f"/api/items/{other_item_id}", headers=auth_headers
    )
    assert response_delete.status_code in (404, 401)

