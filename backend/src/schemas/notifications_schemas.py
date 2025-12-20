from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NotificationDetail(BaseModel):
    notification_id: int
    user_id: int
    event_id: Optional[int]
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class NotificationUpdate(BaseModel):
    is_read: bool

class SubscriptionNotification(BaseModel):
    endpoint: str
    auth: str
    p256dh: str

    class Config:
        from_attributes = True
