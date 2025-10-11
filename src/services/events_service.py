import traceback
from sqlalchemy.orm import Session
from sqlalchemy import exists
from sqlalchemy import func
from sqlalchemy.future import select
from datetime import date
from typing import Optional, List
from src.utils.exceptions import *

from src.models.registration_model import EventRegistration
from src.models.event_model import Event
from src.schemas.events_schemas import *

class EventService:
    @staticmethod
    async def get_event_by_id(db: Session, event_id: int) -> Optional[Event]:
        """
        Tìm và trả về một sự kiện theo ID.
        """
        try:
            query = select(Event).where(Event.event_id == event_id)
            result = db.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            traceback.print_exc()
            raise
    
    @staticmethod
    async def get_public_events(db: Session, category: Optional[str], start_date: Optional[date]) -> List[Event]:
        """
        Lấy danh sách các sự kiện đã được duyệt (public).
        """
        try:
            query = select(Event)

            if category:
                # 1. Chuẩn hóa input từ người dùng
                cleaned_category = category.lower().strip()
                
                # 2. So sánh input đã chuẩn hóa với cột category đã được chuyển về chữ thường trong DB
                query = query.where(func.lower(Event.category) == cleaned_category)
            
            if start_date:
                query = query.where(Event.start_date >= start_date)

            query = query.order_by(Event.start_date.asc())
            result = db.execute(query)
            return result.scalars().all()
        except Exception as e:
            traceback.print_exc()
            raise
    
    @staticmethod
    async def create_event(db: Session, event: EventCreate, manager_id: int) -> Event:
        """
        Tạo một sự kiện mới trong database.
        """
        try:
            db_event = Event(
                **event.dict(),
                manager_id=manager_id,
                status="pending"
            )
            db.add(db_event)
            db.commit()
            db.refresh(db_event)
            return db_event
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise
    
    @staticmethod
    async def update_event(db: Session, event_id: int, event_update: EventUpdate) -> Optional[Event]:
        """
        Cập nhật thông tin cho một sự kiện.
        """
        try:
            db_event = await EventService.get_event_by_id(db, event_id)
            if not db_event:
                return None

            update_data = event_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_event, key, value)
            
            db.commit()
            db.refresh(db_event)
            return db_event
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise
    
    @staticmethod
    async def delete_event(db: Session, event_id: int) -> bool:
        """
        Xóa một sự kiện khỏi database.
        """
        try:
            db_event = await EventService.get_event_by_id(db, event_id)
            if not db_event:
                return False
            
            db.delete(db_event)
            db.commit()
            return True
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise

class RegistrationService:
    @staticmethod
    async def get_registration_by_id(db: Session, registration_id: int) -> Optional[EventRegistration]:
        """
        Lấy thông tin một đơn đăng ký bằng ID của nó.
        """
        try:
            query = select(EventRegistration).where(EventRegistration.registration_id == registration_id)
            result = db.execute(query)
            return result.scalar_one_or_none()
        except Exception:
            traceback.print_exc()
            raise
    
    @staticmethod
    async def get_registrations_for_event(db: Session, event_id: int) -> List[EventRegistration]:
        """
        Lấy tất cả các đơn đăng ký của một sự kiện.
        """
        try:
            query = select(EventRegistration).where(EventRegistration.event_id == event_id)
            result = db.execute(query)
            return result.scalars().all()
        except Exception:
            traceback.print_exc()
            raise
    
    @staticmethod
    async def create_registration(db: Session, event_id: int, user_id: int) -> Optional[EventRegistration]:
        """
        Tạo một đơn đăng ký mới cho user vào một event, sau khi kiểm tra các điều kiện:
        1. Sự kiện phải tồn tại và đã được 'approved'.
        2. Tình nguyện viên chưa đăng ký sự kiện này trước đó.
        """
        try:
            # Điều kiện 1: Kiểm tra sự kiện
            event = await EventService.get_event_by_id(db, event_id)
            if not event or event.status != 'approved':
                return None  # Không cho đăng ký nếu sự kiện không hợp lệ

            # Điều kiện 2: Kiểm tra user đã đăng ký chưa
            query = select(EventRegistration).where(
                EventRegistration.event_id == event_id,
                EventRegistration.user_id == user_id
            )
            result = db.execute(query)
            if result.scalar_one_or_none():
                return None  # Đã tồn tại đăng ký, không tạo mới

            # Nếu tất cả điều kiện hợp lệ, tạo đơn đăng ký mới
            db_reg = EventRegistration(
                event_id=event_id,
                user_id=user_id,
                status="pending"  # Trạng thái mặc định chờ manager duyệt
            )
            db.add(db_reg)
            db.commit()
            db.refresh(db_reg)
            return db_reg
        except Exception:
            traceback.print_exc()
            db.rollback()
            raise
    
    @staticmethod
    async def cancel_registration(db: Session, event_id: int, user_id: int) -> bool:
        """
        Cho phép user hủy đăng ký tham gia một sự kiện.
        Trả về True nếu thành công, False nếu không tìm thấy đơn đăng ký.
        """
        try:
            # Tìm chính xác đơn đăng ký của user cho sự kiện này
            query = select(EventRegistration).where(
                EventRegistration.event_id == event_id,
                EventRegistration.user_id == user_id
            )
            result = db.execute(query)
            db_reg = result.scalar_one_or_none()

            if not db_reg:
                return False  # Không tìm thấy đơn đăng ký để hủy

            db.delete(db_reg)
            db.commit()
            return True
        except Exception:
            traceback.print_exc()
            db.rollback()
            raise
    
    @staticmethod
    async def update_status(db: Session, registration_id: int, status: str) -> Optional[EventRegistration]:
        """
        Cập nhật trạng thái cho một đơn đăng ký (approved, rejected, completed).
        Thường được sử dụng bởi Manager.
        """
        try:
            db_reg = await RegistrationService.get_registration_by_id(db, registration_id)
            if not db_reg:
                return None  # Không tìm thấy đơn đăng ký
            
            db_reg.status = status
            db.commit()
            db.refresh(db_reg)
            return db_reg
        except Exception:
            traceback.print_exc()
            db.rollback()
            raise