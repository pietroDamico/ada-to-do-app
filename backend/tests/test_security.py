"""Tests for security utilities."""

from datetime import timedelta

import pytest

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


class TestPasswordHashing:
    """Test cases for password hashing functions."""

    def test_hash_password_returns_hashed_string(self):
        """Test that hash_password returns a hashed string."""
        password = "mysecretpassword"
        hashed = hash_password(password)
        
        assert hashed is not None
        assert isinstance(hashed, str)
        assert hashed != password
        assert len(hashed) > 0

    def test_hash_password_uses_bcrypt(self):
        """Test that hash_password uses bcrypt format."""
        password = "testpassword"
        hashed = hash_password(password)
        
        # Bcrypt hashes start with $2b$ or $2a$ or $2y$
        assert hashed.startswith("$2")

    def test_hash_password_different_for_same_password(self):
        """Test that hashing same password twice produces different hashes."""
        password = "samepassword"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Due to salting, hashes should be different
        assert hash1 != hash2

    def test_verify_password_correct(self):
        """Test verify_password with correct password."""
        password = "correctpassword"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test verify_password with incorrect password."""
        password = "correctpassword"
        hashed = hash_password(password)
        
        assert verify_password("wrongpassword", hashed) is False

    def test_verify_password_empty_password(self):
        """Test verify_password with empty password."""
        password = "realpassword"
        hashed = hash_password(password)
        
        assert verify_password("", hashed) is False

    def test_hash_password_handles_special_characters(self):
        """Test hashing password with special characters."""
        password = "p@$$w0rd!#$%^&*()"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True

    def test_hash_password_handles_unicode(self):
        """Test hashing password with unicode characters."""
        password = "пароль密码🔐"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True


class TestJWTTokens:
    """Test cases for JWT token functions."""

    def test_create_access_token_returns_string(self):
        """Test that create_access_token returns a JWT string."""
        token = create_access_token(data={"sub": "123"})
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
        # JWT tokens have 3 parts separated by dots
        assert token.count(".") == 2

    def test_decode_access_token_valid(self):
        """Test decoding a valid token."""
        data = {"sub": "user123", "custom": "value"}
        token = create_access_token(data=data)
        
        payload = decode_access_token(token)
        
        assert payload is not None
        assert payload["sub"] == "user123"
        assert payload["custom"] == "value"
        assert "exp" in payload

    def test_decode_access_token_invalid(self):
        """Test decoding an invalid token returns None."""
        invalid_token = "invalid.token.here"
        
        payload = decode_access_token(invalid_token)
        
        assert payload is None

    def test_decode_access_token_expired(self):
        """Test that expired token returns None."""
        # Create token with very short expiration
        token = create_access_token(
            data={"sub": "123"},
            expires_delta=timedelta(seconds=-1),  # Already expired
        )
        
        payload = decode_access_token(token)
        
        assert payload is None

    def test_create_access_token_custom_expiration(self):
        """Test creating token with custom expiration."""
        token = create_access_token(
            data={"sub": "123"},
            expires_delta=timedelta(hours=1),
        )
        
        payload = decode_access_token(token)
        
        assert payload is not None
        assert payload["sub"] == "123"

