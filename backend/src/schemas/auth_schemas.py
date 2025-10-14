from pydantic import BaseModel, EmailStr
from src.schemas.user_schemas import UserBase
from typing import Literal

class AuthLogin(BaseModel):
    """Schema cho dữ liệu đăng nhập."""
    email: EmailStr
    password: str

class AuthRegister(UserBase):
    """
    Schema cho dữ liệu đăng ký. Kế thừa các trường từ UserBase
    và thêm password, role.
    """
    password: str
    # Sử dụng Literal để giới hạn vai trò chỉ có thể là 'volunteer' hoặc 'manager' khi đăng ký
    role: Literal['volunteer', 'manager']