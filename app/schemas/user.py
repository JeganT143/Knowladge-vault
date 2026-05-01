import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator

# Input schema


class UserRegister(BaseModel):
    """Schema for POST /auth/register"""

    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Password must be between 8 and 128 characters long.",
    )
    full_name: str = Field(
        min_length=1,
        max_length=100,
        description="Full name must be between 1 and 100 characters long.",
    )

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        """
        Pydantic validatord run after the basic type checks. This one checks for password strength.
        """
        if v.isdight():
            raise ValueError("Password must contain at least one letter.")
        if v.lower() == v or v.upper() == v:
            raise ValueError(
                "Password must contain both uppercase and lowercase letters."
            )
        if not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in v):
            raise ValueError("Password must contain at least one special character.")
        return v


class UserLogin(BaseModel):
    """Schema for POST /auth/login"""

    email: EmailStr
    password: str


# Output schema
class UserPublic(BaseModel):
    """Schema for user data returned in API responses."""

    id: uuid.UUID
    email: EmailStr
    full_name: str
    created_at: datetime
    is_active: bool

    model_config = {
        "from_attributes": True,  # Allow creating from ORM models
    }


class TokenResponse(BaseModel):
    """Schema for token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int  # Expiration time in seconds
    User: UserPublic


# Update schema
class UserUpdate(BaseModel):
    """All fields are optional for updating user information."""

    full_name: str | None = Field(None, min_length=1, max_length=100)
    password: str | None = Field(
        None,
        min_length=8,
        max_length=128,
        description="Password must be between 8 and 128 characters long.",
    )
