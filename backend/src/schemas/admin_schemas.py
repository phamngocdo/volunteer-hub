from pydantic import BaseModel, EmailStr
from datetime import date
from datetime import datetime, date
from typing import Optional, List
from enum import Enum

###User Admin Schemas###
# Enum để ràng buộc các giá trị status hợp lệ
class UserStatus(str, Enum):
    ACTIVE = "active"
    BANNED = "banned"

class UserStatusUpdate(BaseModel):
    """
    Schema cho body request khi khóa/mở khóa tài khoản.
    Tương ứng với: PATCH /api/v1/admin/users/{user_id}
    """
    status: UserStatus

class UserAdminView(BaseModel):
    """
    Schema để hiển thị thông tin chi tiết của người dùng cho admin.
    Tương ứng với response của: GET /api/v1/admin/users
    """
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
        from_attributes = True # Cho phép Pydantic đọc dữ liệu từ các đối tượng ORM


###Event Admin Schemas###
# Enum cho các trạng thái khi admin duyệt sự kiện
class EventStatusAdminUpdate(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"

class EventStatusUpdate(BaseModel):
    """
    Schema cho body request khi duyệt hoặc từ chối một sự kiện.
    Tương ứng với: PATCH /api/v1/admin/events/{event_id}
    """
    status: EventStatusAdminUpdate

class EventManagerInfo(BaseModel):
    """Schema con, chỉ chứa thông tin cần thiết về người quản lý sự kiện."""
    user_id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True

class EventAdminView(BaseModel):
    """
    Schema để hiển thị thông tin chi tiết của sự kiện cho admin.
    Tương ứng với response của: GET /api/v1/admin/events
    """
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
    manager: EventManagerInfo # Nested schema để hiển thị thông tin manager

    class Config:
        from_attributes = True

# --- Schemas dùng cho việc Export Dữ liệu ---

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
        # Giúp Pydantic đọc dữ liệu từ các đối tượng SQLAlchemy
        from_attributes = True # (hoặc orm_mode = True cho Pydantic v1)

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
    # Thêm các trường khác của Event nếu cần

    class Config:
        from_attributes = True # (hoặc orm_mode = True cho Pydantic v1)