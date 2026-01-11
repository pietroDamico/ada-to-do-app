"""Authentication API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.db.database import get_db
from app.schemas.user import Token, UserCreate, UserLogin, UserResponse
from app.services.auth import authenticate_user, create_user, get_user_by_username


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Register a new user.

    Args:
        user_data: User registration data (username, password).
        db: Database session.

    Returns:
        Created user data (id, username).

    Raises:
        HTTPException: 409 if username already exists.
        HTTPException: 422 for invalid input.
    """
    # Check if username already exists
    existing_user = await get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered",
        )

    # Create new user
    user = await create_user(db, user_data)
    return UserResponse.model_validate(user)


@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> Token:
    """Authenticate user and return JWT token.

    Args:
        credentials: User login credentials (username, password).
        db: Database session.

    Returns:
        JWT access token.

    Raises:
        HTTPException: 401 if credentials are invalid.
    """
    user = await authenticate_user(db, credentials.username, credentials.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token with user_id claim
    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token)

