from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional, List
from schemas.user_schemas import UserBase

# Các trường chung của một sự kiện
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    location: str
    start_date: date
    end_date: date
    image_url: Optional[str] = None

# Schema dùng để validate dữ liệu đầu vào khi TẠO event
class EventCreate(EventBase):
    pass

# Schema dùng để validate dữ liệu đầu vào khi CẬP NHẬT event
# Tất cả các trường đều là Optional để cho phép cập nhật một phần
class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    image_url: Optional[str] = None

# Schema dùng để trả về thông tin event dạng rút gọn (trong danh sách)
class EventSimple(EventBase):
    event_id: int
    status: str
    manager_id: int

    class Config:
        orm_mode = True

# Schema dùng để trả về thông tin chi tiết của một event, bao gồm cả thông tin manager
class EventDetail(EventSimple):
    manager: UserBase # Đây là nested schema, tự động trả về thông tin của manager

# --- Schemas cho Registration ---

# Schema dùng để validate body của request khi manager cập nhật trạng thái
class RegistrationStatusUpdate(BaseModel):
    status: str # Ví dụ: "approved", "rejected", "completed"

# Schema dùng để trả về thông tin chi tiết của một đơn đăng ký
class RegistrationDetail(BaseModel):
    registration_id: int
    status: str
    created_at: datetime
    
    # Nested schemas để trả về thông tin của user và event liên quan
    user: UserBase
    event: EventSimple

    class Config:
        orm_mode = True