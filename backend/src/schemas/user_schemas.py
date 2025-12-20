from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime
from src.schemas.base_schemas import UserBase
from src.schemas.events_schemas import EventSimple 

class UserUpdate(UserBase):
    first_name: str
    last_name: str
    phone_number: str
    avatar_url: Optional[str]
    old_password: Optional[str]
    new_password: Optional[str]

class HistoryItem(BaseModel):
    status: str
    created_at: datetime
    event: EventSimple

    class Config:
        from_attributes = True