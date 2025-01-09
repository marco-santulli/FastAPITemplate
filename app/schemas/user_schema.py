
from pydantic import BaseModel, EmailStr, Field, root_validator

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str = Field(None, min_length=8)
    hashed_password: str = None

    @root_validator
    def check_password_fields(cls, values):
        password = values.get("password")
        hashed_password = values.get("hashed_password")
        if not password and not hashed_password:
            raise ValueError("Either 'password' or 'hashed_password' must be provided.")
        if password and hashed_password:
            raise ValueError("Only one of 'password' or 'hashed_password' can be provided.")
        return values

class UserUpdate(BaseModel):
    email: EmailStr = None
    full_name: str = None
    password: str = None

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
