from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, constr


class TodoListBase(BaseModel):
    title: constr(min_length=1)


class TodoListCreate(TodoListBase):
    pass


class TodoListUpdate(BaseModel):
    title: Optional[constr(min_length=1)] = None


class TodoListOut(TodoListBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TodoItemBase(BaseModel):
    title: constr(min_length=1)


class TodoItemCreate(TodoItemBase):
    pass


class TodoItemUpdate(BaseModel):
    title: Optional[constr(min_length=1)] = None
    completed: Optional[bool] = None


class TodoItemOut(TodoItemBase):
    id: int
    completed: bool
    list_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

