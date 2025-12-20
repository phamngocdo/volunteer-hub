import traceback
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.future import select
from src.models.user_model import User
from src.models.registration_model import EventRegistration
from typing import List, Optional
from src.utils.security import verify_password, hash_password, create_access_token

class UserService():
    @staticmethod
    async def get_user_by_id(db: Session, user_id: int):
        try:
            user = db.query(User).filter(User.user_id == user_id).first()
            if user:
                user_dict = user.__dict__.copy()
                user_dict.pop("password", None)
                return user_dict
        except Exception as e:
            traceback.print_exc()
            raise e 


    @staticmethod
    async def get_all_users(db: Session):
        try:
            users = db.query(User).all() 

            result = []
            for user in users:
                user_dict = user.__dict__.copy()
                user_dict.pop("password", None)
                result.append(user_dict)

            return result

        except Exception as e:
            traceback.print_exc()
            raise e

    
    @staticmethod
    async def update_user(db: Session, user_id: int, user_data: dict):
        try:
            user = db.query(User).filter(User.user_id == user_id).first()
                        
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

            access_token = create_access_token(
                data={
                    "sub": str(user.user_id),
                    "role": user.role,
                    "status": user.status,
                    "avatar_url": user.avatar_url

                }
            )
            return {
                "access_token": access_token,
            }

        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise e 
    

    @staticmethod
    async def update_user_status(db: Session, user_id: int, new_status: str):
        try:
            user = db.query(User).filter(User.user_id == user_id).first()

            user.status = new_status
            db.commit()
            db.refresh(user)
            user_dict = user.__dict__.copy()
            user_dict.pop("password", None)

            return user_dict

        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise e
        
    
    @staticmethod
    async def get_user_history(db: Session, user_id: int) -> List[EventRegistration]:
        try:
            query = (
                select(EventRegistration)
                .where(EventRegistration.user_id == user_id)
                .options(selectinload(EventRegistration.event)) 
                .order_by(EventRegistration.created_at.desc())
            )
            
            result = db.execute(query)
            return result.scalars().all()
        except Exception as e:
            traceback.print_exc()
            raise e