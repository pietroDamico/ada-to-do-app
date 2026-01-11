"""Tests for User model."""

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.models.user import User


# Use synchronous SQLite for testing model definitions
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create database tables and provide a session for testing."""
    Base.metadata.create_all(bind=engine)
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


class TestUserModel:
    """Test cases for User model."""

    def test_user_model_instantiation(self, db_session):
        """Test that User model can be instantiated with required fields."""
        user = User(
            username="testuser",
            hashed_password="$2b$12$hashedpasswordexample",
        )
        assert user.username == "testuser"
        assert user.hashed_password == "$2b$12$hashedpasswordexample"

    def test_user_model_persistence(self, db_session):
        """Test that User can be persisted to the database."""
        user = User(
            username="persisteduser",
            hashed_password="$2b$12$hashedpasswordexample",
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.id is not None
        assert user.id > 0
        assert user.created_at is not None

    def test_user_model_repr(self, db_session):
        """Test User __repr__ method."""
        user = User(
            username="repruser",
            hashed_password="$2b$12$hashedpasswordexample",
        )
        db_session.add(user)
        db_session.commit()

        repr_str = repr(user)
        assert "User" in repr_str
        assert "repruser" in repr_str

    def test_user_username_unique_constraint(self, db_session):
        """Test that username has unique constraint."""
        user1 = User(
            username="uniqueuser",
            hashed_password="$2b$12$hashedpasswordexample1",
        )
        db_session.add(user1)
        db_session.commit()

        user2 = User(
            username="uniqueuser",  # Same username
            hashed_password="$2b$12$hashedpasswordexample2",
        )
        db_session.add(user2)

        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()


class TestUsersTable:
    """Test cases for users table structure."""

    def test_users_table_created(self, db_session):
        """Test that the users table exists after migration."""
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        assert "users" in tables

    def test_users_table_columns(self, db_session):
        """Test that users table has the expected columns."""
        inspector = inspect(engine)
        columns = {col["name"] for col in inspector.get_columns("users")}
        expected_columns = {"id", "username", "hashed_password", "created_at"}
        assert expected_columns == columns

    def test_users_table_indexes(self, db_session):
        """Test that users table has the expected indexes."""
        inspector = inspect(engine)
        indexes = inspector.get_indexes("users")
        index_names = {idx["name"] for idx in indexes}

        # Check for username unique index
        username_indexes = [idx for idx in indexes if "username" in idx["column_names"]]
        assert len(username_indexes) > 0
        assert any(idx.get("unique", False) for idx in username_indexes)

