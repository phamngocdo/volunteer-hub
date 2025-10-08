from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserBase(BaseModel):
    """Các trường thông tin cơ bản của người dùng."""
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None

class UserUpdate(UserBase):
    password: str