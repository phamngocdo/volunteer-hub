from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional, List
from enum import Enum

class UserStatus(str, Enum):
    ACTIVE = "active"
    BANNED = "banned"

class UserStatusUpdate(BaseModel):
    status: UserStatus

class UserAdminView(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    role: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EventStatusAdminUpdate(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"

class EventStatusUpdate(BaseModel):
    status: EventStatusAdminUpdate

class EventManagerInfo(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True

class EventAdminView(BaseModel):
    event_id: int
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str
    created_at: datetime
    updated_at: datetime
    manager: EventManagerInfo

    class Config:
        from_attributes = True

class UserExport(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str
    role: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EventExport(BaseModel):
    event_id: int
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    start_date: date
    end_date: date
    manager_id: int

    class Config:
        from_attributes = True