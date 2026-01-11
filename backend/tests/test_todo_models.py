import pytest
from sqlalchemy import select

from app.db.database import AsyncSessionLocal
from app.models.todo import TodoItem, TodoList
from app.models.user import User


@pytest.mark.asyncio
async def test_models_can_create_and_query():
    async with AsyncSessionLocal() as session:
        user = User(username="owner", hashed_password="pw")
        session.add(user)
        await session.flush()

        todo_list = TodoList(title="Groceries", user_id=user.id)
        session.add(todo_list)
        await session.flush()

        item = TodoItem(title="Buy milk", list_id=todo_list.id)
        session.add(item)
        await session.commit()

        result = await session.execute(select(TodoList).where(TodoList.user_id == user.id))
        lists = result.scalars().all()
        assert len(lists) == 1
        assert lists[0].items[0].title == "Buy milk"


@pytest.mark.asyncio
async def test_cascade_delete_removes_items():
    async with AsyncSessionLocal() as session:
        user = User(username="owner2", hashed_password="pw")
        session.add(user)
        await session.flush()

        todo_list = TodoList(title="Work", user_id=user.id)
        session.add(todo_list)
        await session.flush()

        item = TodoItem(title="Task", list_id=todo_list.id)
        session.add(item)
        await session.commit()

        await session.delete(todo_list)
        await session.commit()

        remaining_item = await session.get(TodoItem, item.id)
        assert remaining_item is None

