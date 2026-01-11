from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.models.todo import TodoItem, TodoList
from app.models.user import User
from app.schemas.todo import TodoItemCreate, TodoItemOut, TodoItemUpdate

router = APIRouter(prefix="/api", tags=["items"])


async def _get_owned_list(
    list_id: int, user: User, db: AsyncSession
) -> TodoList | None:
    result = await db.execute(
        select(TodoList).where(TodoList.id == list_id, TodoList.user_id == user.id)
    )
    return result.scalar_one_or_none()


async def _get_owned_item(
    item_id: int, user: User, db: AsyncSession
) -> TodoItem | None:
    stmt = (
        select(TodoItem)
        .join(TodoList)
        .where(TodoItem.id == item_id, TodoList.user_id == user.id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


@router.post(
    "/lists/{list_id}/items",
    response_model=TodoItemOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_item(
    list_id: int,
    payload: TodoItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TodoItem:
    todo_list = await _get_owned_list(list_id, current_user, db)
    if todo_list is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")

    item = TodoItem(
        title=payload.title,
        list_id=todo_list.id,
        completed=False,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.get("/lists/{list_id}/items", response_model=list[TodoItemOut])
async def list_items(
    list_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[TodoItem]:
    todo_list = await _get_owned_list(list_id, current_user, db)
    if todo_list is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")

    result = await db.execute(
        select(TodoItem).where(TodoItem.list_id == todo_list.id)
    )
    return result.scalars().all()


@router.put("/items/{item_id}", response_model=TodoItemOut)
async def update_item(
    item_id: int,
    payload: TodoItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TodoItem:
    item = await _get_owned_item(item_id, current_user, db)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if payload.title is not None:
        item.title = payload.title
    if payload.completed is not None:
        item.completed = payload.completed

    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    item = await _get_owned_item(item_id, current_user, db)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    await db.delete(item)
    await db.commit()

