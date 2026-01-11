from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


class UsernameAlreadyExists(Exception):
    """Raised when attempting to create a user with an existing username."""


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    result = await db.execute(select(User).where(User.username == user_in.username))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise UsernameAlreadyExists

    user = User(username=user_in.username, hashed_password=get_password_hash(user_in.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, username: str, password: str) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

