"""User schemas for request/response validation."""

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """Schema for user registration request."""

    username: str = Field(..., min_length=3, max_length=50, description="Username for the new user")
    password: str = Field(..., min_length=1, description="Password for the new user")


class UserResponse(BaseModel):
    """Schema for user response (without password)."""

    id: int = Field(..., description="User ID")
    username: str = Field(..., description="Username")

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    """Schema for user login request."""

    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")

