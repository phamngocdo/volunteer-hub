import string
import secrets
import traceback
import random
from sqlalchemy.orm import Session
from config.db_config import Base
from config.redis_config import redis_client
from models.users_model import UserModel
from utils.security import hash_password, verify_password, create_access_token
from utils.gmail_sender import send_email_verification_code

class AuthService:
    pass

class VerificationCodeService:
    pass

class AuthService:
    @staticmethod
    async def login(db: Session, user_data: dict):
        email = user_data.get("email")
        password = user_data.get("password")

        try:
            user = db.query(UserModel).filter(UserModel.email == email).first()

            if not user or not verify_password(password, user.password):
                raise ValueError("Invalid email or password")

            if not verify_password(password, user.password):
                raise ValueError("Invalid email or password")
            
            access_token = create_access_token(data={"sub": str(user.id)})
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "email": user.email,
                    "username": user.username
                }
            }
        except Exception as e:
            traceback.print_exc()
            raise

    @staticmethod
    async def login_with_google(db: Session, email: str):
        try:
            user = db.query(UserModel).filter(UserModel.email == email).first()
            if not user:
                characters = string.ascii_letters + string.digits
                random_pw  = ''.join(secrets.choice(characters) for i in range(20))
                username = email.split('@')[0]
                user = UserModel(username=username, email=email, password=hash_password(random_pw))
                db.add(user)
                db.commit()
                db.refresh(user)

            access_token = create_access_token(data={"sub": str(user.id)})
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username
                }
            }
        except Exception as e:
            traceback.print_exc()
            raise

    @staticmethod
    async def register(db: Session, user_data: dict):
        email = user_data.get("email")
        username = user_data.get("username")
        phone = user_data.get("phone")
        password = user_data.get("password")
        try:
            user_email = db.query(UserModel).filter(UserModel.email == email).first()
            if user_email:
                raise ValueError("Email already exists")
            
            user_username = db.query(UserModel).filter(UserModel.username == username).first()
            if user_username:
                raise ValueError("Username already exists")
            
            hash_pw = hash_password(password)

            new_user = UserModel(
                username=username,
                email=email,
                phone=phone,
                password=hash_pw
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
        except Exception as e:
            traceback.print_exc()
            raise 

class CodeAlreadySentException(Exception):
    def __init__(self, detail: str):
        self.detail = detail

class VerificationCodeService:
    @staticmethod
    async def send_code(email: str):
        existing_code = await redis_client.get(f"verify: {email}")
        if existing_code:
            return CodeAlreadySentException(detail="Verification code already sent. Please wait before retrying.")
        
        characters = string.ascii_letters + string.digits 
        code = ''.join(random.choices(characters, k=6))
        await redis_client.set(f"verify:{email}", code, ex=120)
        await send_email_verification_code(to_email=email, verification_code=code)


    @staticmethod
    async def verify_code(email: str, code: str) -> bool:
        stored_code = await redis_client.get(f"verify:{email}")
        return stored_code == code

    @staticmethod
    async def delete_code(email: str):
        await redis_client.delete(f"verify:{email}")

