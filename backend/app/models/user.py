"""User model definition."""

from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class User(Base):
    """User model for authentication.

    Attributes:
        id: Primary key.
        username: Unique username for the user.
        hashed_password: Bcrypt-hashed password (never store plain passwords).
        created_at: Timestamp when the user was created.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        """String representation of User."""
        return f"<User(id={self.id}, username={self.username!r})>"
