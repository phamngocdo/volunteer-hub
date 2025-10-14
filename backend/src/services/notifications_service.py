from sqlalchemy.orm import Session
from sqlalchemy.future import select
from src.models.notification_model import Notification
import traceback

class NotificationService:
    @staticmethod
    async def get_user_notifications(db: Session, user_id: int):
        """
        Tìm và trả về các thông báo theo ID người dùng.
        """
        try:
            query = select(Notification).where(Notification.user_id == user_id)
            return db.execute(query).scalars().all()
        except Exception as e:
            traceback.print_exc()
            raise
    

    @staticmethod
    async def mark_as_read(db: Session, notification_id: int, user_id: int, is_read: bool):
        """
        Tìm thông báo theo ID và cập nhật is_read.
        """
        try: 
            # Tạo câu truy vấn chọn bài post có đúng ID và thuộc về đúng user
            query = select(Notification).where(
                Notification.notification_id == notification_id,
                Notification.user_id == user_id
            )
            noti = db.execute(query).scalar_one_or_none()# lấy duy nhất 1 kết quả hoặc None nếu không có
            if not noti:
                return False
            noti.is_read = is_read
            db.commit()
            db.refresh(noti)
            return noti
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise