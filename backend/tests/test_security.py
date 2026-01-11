"""Tests for security utilities."""

import pytest

from app.core.security import hash_password, verify_password


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

