import traceback
from jwt import InvalidTokenError, ExpiredSignatureError
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.future import select
from src.models.user_model import User
from src.models.registration_model import EventRegistration
from typing import Optional, List
from src.utils.security import decode_token, verify_password, hash_password

class UserService():
    @staticmethod
    async def get_user_by_id(user_id: int, db: Session):
        try:
            user = db.query(User).filter(User.user_id == user_id).first()
            if user:
                user_dict = user.__dict__.copy()
                user_dict.pop("password", None)
                return user_dict
        except Exception as e:
            traceback.print_exc()
            raise 

    
    @staticmethod
    async def get_user_by_email(email: str, db: Session):
        try:
            user = db.query(User).filter(User.email == email).first()
            if user:
                user_dict = user.__dict__.copy()
                user_dict.pop("password", None)
                return user_dict
        except Exception as e:
            traceback.print_exc()
            raise 

    
    @staticmethod
    async def get_current_user(token: str, db: Session):
        try:
            user_id = decode_token(token).get("sub")
            user = db.query(User).filter(User.user_id == user_id).first()
            if user:
                user_dict = user.__dict__.copy()
                user_dict.pop("password", None)
                return user_dict
        except (ExpiredSignatureError, InvalidTokenError) as e:
            raise
        except Exception as e:
            traceback.print_exc()
            raise

    
    @staticmethod
    async def update_current_user(token: str, user_data: dict, db: Session):
        try:
            user_id = decode_token(token).get("sub")
            user = db.query(User).filter(User.user_id == user_id).first()
            if not user:
                raise ValueError("User not found")

            user_data = {k: v for k, v in user_data.items() if v not in [None, ""]}

            if "old_password" in user_data:
                old_password = user_data.pop("old_password")
                new_password = user_data.pop("new_password", None)
                if not verify_password(old_password, user.password):
                    raise ValueError("Sai mật khẩu cũ")
                if new_password:
                    user.password = hash_password(new_password)

            for key, value in user_data.items():
                setattr(user, key, value)

            db.commit()
            db.refresh(user)

            user_dict = user.__dict__.copy()
            user_dict.pop("password", None)
            return user_dict

        except (ExpiredSignatureError, InvalidTokenError):
            raise ValueError("Invalid or expired token")
        except Exception as e:
            traceback.print_exc()
            raise ValueError(e)
        
    
    @staticmethod
    async def get_user_history(db: Session, user_id: int) -> List[EventRegistration]:
        """
        Lấy danh sách lịch sử đăng ký sự kiện của một người dùng.
        """
        try:
            query = (
                select(EventRegistration)
                .where(EventRegistration.user_id == user_id)
                .options(selectinload(EventRegistration.event)) # Tối ưu hóa: Tải sẵn thông tin event
                .order_by(EventRegistration.created_at.desc()) # Sắp xếp theo ngày đăng ký mới nhất
            )
            
            result = db.execute(query)
            return result.scalars().all()
        except Exception as e:
            traceback.print_exc()
            raise