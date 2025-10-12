from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from src.config.db_config import get_db
from src.services.notifications_service import NotificationService
from src.schemas.notifications_schemas import *

notifications_router = APIRouter()

# trả về danh sách các đối tượng notificationdetail
@notifications_router.get("/", response_model=List[NotificationDetail])
async def get_notifications(request: Request, db: Session = Depends(get_db)):
    """
    Lấy tất cả thông báo của người dùng
    """
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await NotificationService.get_user_notifications(db, user["user_id"])

@notifications_router.patch("/{notification_id}")
async def mark_notification_read(request: Request, notification_id: int, body: NotificationUpdate, db: Session = Depends(get_db)):
    """
    Đánh dấu đã đọc thông báo
    """
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    success = await NotificationService.mark_as_read(db, notification_id, user["user_id"], body.is_read)
    if not success:
        raise HTTPException(status_code=403, detail="Notification not found")
    return {"detail": "Mark notification as read successfully"}