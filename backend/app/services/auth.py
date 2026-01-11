"""Authentication service for user operations."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    """Get a user by username.

    Args:
        db: Database session.
        username: Username to search for.

    Returns:
        User if found, None otherwise.
    """
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    """Create a new user with hashed password.

    Args:
        db: Database session.
        user_data: User registration data.

    Returns:
        Created user object.
    """
    hashed_pwd = hash_password(user_data.password)
    user = User(
        username=user_data.username,
        hashed_password=hashed_pwd,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, username: str, password: str) -> User | None:
    """Authenticate a user by username and password.

    Args:
        db: Database session.
        username: Username to authenticate.
        password: Plain text password to verify.

    Returns:
        User if credentials are valid, None otherwise.
    """
    user = await get_user_by_username(db, username)
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

