import traceback
from jwt import InvalidTokenError, ExpiredSignatureError
from sqlalchemy.orm import Session
from models.users_model import UserModel
from utils.security import decode_token, verify_password, hash_password

class UserService():
    @staticmethod
    async def get_user_by_id(user_id: int, db: Session):
        try:
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
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
            user = db.query(UserModel).filter(UserModel.email == email).first()
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
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
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
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                raise ValueError("User not found")

            if "password" in user_data:
                password = user_data["password"]
                if not verify_password(password, user.password):
                    raise ValueError("Wrong current password")
                else:
                    user_data["password"] = hash_password(password=password)
            
            for key, value in user_data.items():
                setattr(user, key, value)
                
            db.commit()
            db.refresh(user)

            user_dict = user.__dict__.copy()
            user_dict.pop("password", None)
            return user_dict
        
        except (ExpiredSignatureError, InvalidTokenError) as e:
            raise
        except Exception as e:
            traceback.print_exc()
            raise