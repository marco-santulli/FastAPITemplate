
from pydantic import BaseModel, EmailStr, Field, model_validator

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str = Field(None, min_length=8)
    hashed_password: str = None

    @model_validator(mode="after")
    def check_password_fields(self):
        logger.info('Entering check_password_fields')
    def check_password_fields(self):
    def check_password_fields(self):
        logger.info('Entering check_password_fields')
    def check_password_fields(self):
        if not self.password and not self.hashed_password:
            raise ValueError("Either 'password' or 'hashed_password' must be provided.")
        if self.password and self.hashed_password:
            raise ValueError("Provide only one of 'password' or 'hashed_password'.")
        return self

class UserUpdate(BaseModel):
    email: EmailStr = None
    full_name: str = None
    password: str = None
    hashed_password: str = None

    @model_validator(mode="after")
    def validate_password_fields(self):
        logger.info('Entering validate_password_fields')
    def validate_password_fields(self):
    def validate_password_fields(self):
        logger.info('Entering validate_password_fields')
    def validate_password_fields(self):
        if self.password and self.hashed_password:
            raise ValueError("Provide only one of 'password' or 'hashed_password'.")
        return self

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
