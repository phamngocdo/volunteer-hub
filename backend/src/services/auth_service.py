import string
import secrets
import traceback
import random
from sqlalchemy.orm import Session
from config.db_config import Base
from config.redis_config import redis_client
from models.events_model import User
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
            query = select(User).where(User.email == email)
            result = await db.execute(query)
            user = result.scalar_one_or_none()

            if not user or not verify_password(password, user.password):
                raise ValueError("Invalid email or password")
            
            access_token = create_access_token(data={"sub": str(user.id)})
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "user_id": user.user_id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                }
            }
        except Exception as e:
            traceback.print_exc()
            raise

    @staticmethod
    async def login_with_google(db: Session, email: str):
        """
        Đăng nhập/Đăng ký bằng Google.
        """

        try:
            email = user_info.get("email")
            query = select(User).where(User.email == email)
            result = await db.execute(query)
            user = result.scalar_one_or_none()

            if not user:
                first_name = user_info.get("first_name") or email.split('@')[0]
                last_name = user_info.get("last_name", "")
                random_pw = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(20))
                new_user = User(
                    first_name=first_name, # Sử dụng tên đã qua xử lý
                    last_name=last_name,   # Sử dụng họ đã qua xử lý
                    email=email,
                    password=hash_password(random_pw),
                    role="volunteer", # Mặc định vai trò là volunteer
                    status="active"
                )
                db.add(new_user)
                await db.commit()
                await db.refresh(new_user)
                user = new_user
            
            token_data = {"sub": str(user.user_id)}
            access_token = create_access_token(data=token_data)

            return {
                "access_token": access_token,
                "user": {
                    "user_id": user.user_id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                }
            }
        except Exception as e:
            traceback.print_exc()
            raise

    @staticmethod
    async def register(db: Session, user_data: dict):
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        email=user_data["email"],
        phone_number=user_data.get("phone_number"), # .get() cho trường optional
        password=user_data.get("password"),
        role=user_data["role"],
        try:
            user_email = db.query(User).filter(User.email == email).first()
            if user_email:
                raise ValueError("Email already exists")
            
            hash_pw = hash_password(password)

            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number, # .get() cho trường optional
                password=hash_pw,
                role=role,
                status="active" # Mặc định là active
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

