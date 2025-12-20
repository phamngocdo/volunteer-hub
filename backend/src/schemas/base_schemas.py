from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional, List

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    location: str
    start_date: date
    end_date: date
    image_url: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None