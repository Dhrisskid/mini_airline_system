from pydantic import BaseModel, EmailStr, field_validator
from models.user import UserRole


class UserRequestModel(BaseModel):
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if len(v) > 72:
            raise ValueError('Password cannot exceed 72 characters')
        return v

class AdminCreateUserModel(BaseModel):
    email: EmailStr
    password: str
    role: UserRole

    @field_validator('password')
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class LoginRequestModel(BaseModel):
    email: EmailStr
    password: str


class UpdatePasswordRequest(BaseModel):
    new_password: str

    @field_validator('new_password')
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class UpdateActiveStatusRequest(BaseModel):
    is_active: bool

