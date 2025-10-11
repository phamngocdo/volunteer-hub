from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime
from src.schemas.base_schemas import UserBase
from src.schemas.events_schemas import EventSimple 

class UserUpdate(UserBase):
    password: str

class HistoryItem(BaseModel):
    """
    Schema cho một mục trong Lịch sử tham gia của người dùng.
    """
    # Lấy từ bảng event_registrations
    status: str
    created_at: datetime # Ngày đăng ký

    # Lấy thông tin chi tiết của sự kiện (Nested Schema)
    event: EventSimple

    class Config:
        from_attributes = True