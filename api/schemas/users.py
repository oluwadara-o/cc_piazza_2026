"""Copied from class 4 TODO: Update"""
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Request body for registration.
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)


# Request body for login.
class UserLogin(BaseModel):
    username: Optional[str] = Field(min_length=3, max_length=50, default=None)
    email: Optional[EmailStr] = Field(default=None)
    password: str


# Response body for a user.
# Notice that the password is not included.
class UserResponse(BaseModel):
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


# Response body returned after login.
class TokenResponse(BaseModel):
    access_token: str
    token_type: str