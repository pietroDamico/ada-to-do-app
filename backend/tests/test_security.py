import pytest

from app.core.security import (
    InvalidTokenError,
    create_access_token,
    get_password_hash,
    validate_token,
    verify_password,
)


def test_password_hashing_roundtrip():
    password = "supersecret"
    hashed = get_password_hash(password)

    assert hashed != password
    assert verify_password(password, hashed)


def test_validate_token_invalid():
    with pytest.raises(InvalidTokenError):
        validate_token("not-a-token")


def test_create_and_validate_token():
    token = create_access_token({"sub": "123"})
    payload = validate_token(token)

    assert payload["sub"] == "123"

