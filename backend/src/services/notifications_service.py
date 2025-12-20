from sqlalchemy.orm import Session
from sqlalchemy.future import select
from src.models.notification_model import Notification
from src.models.push_nortification_model import PushSubscription
import traceback
import os
from typing import Optional


class NotificationService:
    @staticmethod
    async def get_user_notifications(db: Session, user_id: int):
        try:
            query = select(Notification).where(Notification.user_id == user_id)
            return db.execute(query).scalars().all()
        except Exception as e:
            traceback.print_exc()
            raise e
    

    @staticmethod
    async def mark_as_read(db: Session, user_id: int):
        try:
            query = select(Notification).where(Notification.user_id == user_id)
            notifications = db.execute(query).scalars().all()

            if not notifications:
                return False 

            for noti in notifications:
                noti.is_read = True

            db.commit()
            return True
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise e


    @staticmethod
    async def subcribe_nortificate(db: Session, user_id: int, data):
        endpoint = data.endpoint
        p256dh = data.p256dh
        auth = data.auth

        try:
            existing = db.query(PushSubscription).filter_by(user_id=user_id, endpoint=endpoint).first()
            if existing:
                existing.endpoint = endpoint
                existing.p256dh = p256dh
                existing.auth = auth
            else:
                new_sub = PushSubscription(
                    user_id=user_id,
                    endpoint=endpoint,
                    p256dh=p256dh,
                    auth=auth
                )
                db.add(new_sub)

            db.commit()
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise e
    

    @staticmethod
    async def unsubscribe_notification(db: Session, user_id: int, endpoint: str):
        try:
            sub = db.query(PushSubscription).filter_by(user_id=user_id, endpoint=endpoint).first()
            if not sub:
                return False

            db.delete(sub)
            db.commit()
            return True
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise e
        

    @staticmethod
    async def send_notification(db: Session, user_id: int, event_id: Optional[int], title: str, message: str):
        try:
            notification = Notification(
                user_id=user_id,
                event_id=event_id,
                message=message,
            )
            db.add(notification)
            db.commit()
            db.refresh(notification)
            subscriptions = db.query(PushSubscription).filter_by(user_id=user_id).all()

            def to_dict(obj):
                return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

            return [to_dict(sub) for sub in subscriptions]

        except Exception as e:
            traceback.print_exc()
            raise e