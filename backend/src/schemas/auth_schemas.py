from pydantic import BaseModel, EmailStr
from src.schemas.user_schemas import UserBase
from typing import Literal

class AuthLogin(BaseModel):
    email: EmailStr
    password: str

class AuthRegister(UserBase):
    password: str
    role: Literal['volunteer', 'manager']