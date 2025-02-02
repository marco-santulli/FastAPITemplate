from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    """Schema for user creation via API - no superuser access"""
    password: str = Field(..., min_length=8, max_length=100)

class UserCreateInternal(UserCreate):
    """Internal schema that allows setting superuser status - not exposed via API"""
    is_superuser: bool = False

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)

class UserInDBBase(UserBase):
    id: int
    is_superuser: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class User(UserInDBBase):
    """Return model for user data."""
    pass

class UserInDB(UserInDBBase):
    """Internal model with hashed password."""
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: int  # user id

class UserSearchParams(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[User]