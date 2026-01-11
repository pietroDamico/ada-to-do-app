from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.models.todo import TodoList
from app.models.user import User
from app.schemas.todo import (
    TodoListCreate,
    TodoListOut,
    TodoListUpdate,
)

router = APIRouter(prefix="/api/lists", tags=["lists"])


aus = 0
async def _get_owned_list(
    list_id: int, user: User, db: AsyncSession
) -> TodoList | None:
    result = await db.execute(
        select(TodoList).where(TodoList.id == list_id, TodoList.user_id == user.id)
    )
    return result.scalar_one_or_none()


@router.post("", response_model=TodoListOut, status_code=status.HTTP_201_CREATED)
async def create_list(
    payload: TodoListCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TodoList:
    todo_list = TodoList(title=payload.title, user_id=current_user.id)
    db.add(todo_list)
    await db.commit()
    await db.refresh(todo_list)
    return todo_list


@router.get("", response_model=list[TodoListOut])
async def list_lists(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[TodoList]:
    result = await db.execute(
        select(TodoList).where(TodoList.user_id == current_user.id)
    )
    return result.scalars().all()


@router.get("/{list_id}", response_model=TodoListOut)
async def get_list(
    list_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TodoList:
    todo_list = await _get_owned_list(list_id, current_user, db)
    if todo_list is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return todo_list


@router.put("/{list_id}", response_model=TodoListOut)
async def update_list(
    list_id: int,
    payload: TodoListUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TodoList:
    todo_list = await _get_owned_list(list_id, current_user, db)
    if todo_list is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if payload.title is not None:
        todo_list.title = payload.title

    await db.commit()
    await db.refresh(todo_list)
    return todo_list


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_list(
    list_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    todo_list = await _get_owned_list(list_id, current_user, db)
    if todo_list is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    await db.delete(todo_list)
    await db.commit()
