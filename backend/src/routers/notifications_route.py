from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jwt import InvalidTokenError, ExpiredSignatureError

from typing import List, Optional
import json
from src.config.db_config import get_db
from src.services.notifications_service import NotificationService
from src.schemas.notifications_schemas import *
from src.config.redis_config import redis_client as r

notifications_router = APIRouter()

# trả về danh sách các đối tượng notificationdetail
@notifications_router.get("/", response_model=List[NotificationDetail])
async def get_notifications(request: Request, db: Session = Depends(get_db)):
    """
    Lấy tất cả thông báo của người dùng
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth_header.split(" ")[1]
    session_json = await r.get(token)
    if not session_json:
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    try:
        user = json.loads(session_json)
        if user.get("status") == "banned":
            raise HTTPException(status_code=403, detail="Your account has been banned")
        user_id = user.get("user_id")
        notifications = await NotificationService.get_user_notifications(db, user_id)
        return notifications
    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
@notifications_router.patch("/{notification_id}")
async def mark_notification_read(request: Request, notification_id: int, body: NotificationUpdate, db: Session = Depends(get_db)):
    """
    Đánh dấu đã đọc thông báo
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth_header.split(" ")[1]
    session_json = await r.get(token)
    if not session_json:
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    try:
        user = json.loads(session_json)
        if user.get("status") == "banned":
            raise HTTPException(status_code=403, detail="Your account has been banned")
        user_id = user.get("user_id")
        success = await NotificationService.mark_as_read(db, notification_id, user_id, body.is_read)
        if not success:
            raise HTTPException(status_code=404, detail="Notification not found")
        return {"detail": "Mark notification as read successfully"}
    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")