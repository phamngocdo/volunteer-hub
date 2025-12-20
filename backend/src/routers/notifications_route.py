from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.utils.dependencies import *
from src.config.db_config import get_db
from src.services.notifications_service import NotificationService
from src.schemas.notifications_schemas import *
from src.utils.dependencies import get_current_user

notifications_router = APIRouter()

@notifications_router.get("/", response_model=List[NotificationDetail])
async def get_notifications(
    request: Request,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách thông báo.
    
    Trả về tất cả thông báo của người dùng hiện tại, bao gồm cả đã đọc và chưa đọc.
    """
    try:
        notifications = await NotificationService.get_user_notifications(db, user_id=user.get("sub"))
        return notifications
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    

@notifications_router.patch("/")
async def mark_notification_read(
    request: Request,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Đánh dấu đã đọc tất cả thông báo.
    
    Cập nhật trạng thái 'false' (chưa đọc) thành 'true' (đã đọc) cho tất cả thông báo của user.
    """
    try:
        success = await NotificationService.mark_as_read(db=db, user_id=user.get("sub"))
        if not success:
            raise HTTPException(status_code=404, detail="Notification not found")
        return {"detail": "Mark notification as read successfully"}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    

@notifications_router.post("/subscribe")
async def subscribe(
    data: SubscriptionNotification, 
    request: Request, 
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Đăng ký nhận thông báo đẩy (WebPush).
    
    Lưu thông tin subscription từ trình duyệt để gửi thông báo đẩy sau này.
    """
    try:
        await NotificationService.subcribe_nortificate(db, user.get("sub"), data)
        return {"message": "Subscribed successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    
@notifications_router.delete("/unsubscribe")
async def unsubscribe(
    data: SubscriptionNotification,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Hủy đăng ký nhận thông báo đẩy.
    
    Xóa thông tin subscription của trình duyệt khỏi hệ thống.
    """
    try:
        success = await NotificationService.unsubscribe_notification(db, user.get("sub"), data.endpoint)
        if not success:
            raise HTTPException(status_code=404, detail="Subscription not found")
        return {"message": "Unsubscribed successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")