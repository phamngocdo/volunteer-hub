from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Notification
class NotificationDetail(BaseModel):
    notification_id: int
    user_id: int
    event_id: int
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

# cập nhật thông báo đã đọc
class NotificationUpdate(BaseModel):
    is_read: bool