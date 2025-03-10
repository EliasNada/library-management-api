import re
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import field_validator

from enum import Enum

class RoleEnum(str, Enum):
    user = 'user'
    librarian = 'librarian'

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: RoleEnum = RoleEnum.user

    @field_validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True
