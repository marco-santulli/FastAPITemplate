
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    email: EmailStr = None
    full_name: str = None
    password: str = None

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
