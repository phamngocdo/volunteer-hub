from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional, List

# Các trường chung của một sự kiện
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    location: str
    start_date: date
    end_date: date
    image_url: Optional[str] = None

class UserBase(BaseModel):
    """Các trường thông tin cơ bản của người dùng."""
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None