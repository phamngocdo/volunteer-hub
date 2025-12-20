from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional, List
from src.schemas.base_schemas import EventBase, UserBase

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    image_url: Optional[str] = None

class EventSimple(EventBase):
    event_id: int
    status: str
    manager_id: int
    volunteer_number: Optional[int] = None
    class Config:
        from_attributes = True

class EventDetail(EventSimple):
    manager: UserBase

class RegistrationStatusUpdate(BaseModel):
    status: str

class RegistrationDetail(BaseModel):
    registration_id: int
    status: str
    created_at: datetime
    
    user: UserBase
    event: EventSimple

    class Config:
        from_attributes = True

class JoinedEventDetail(BaseModel):
    event_id: int
    title: str
    image_url: Optional[str] = None
    member_count: int

    class Config:
        from_attributes = True