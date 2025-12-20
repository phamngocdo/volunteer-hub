import traceback
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from src.models.user_model import User
from src.utils.security import hash_password, verify_password, create_access_token

class AuthService:
    @staticmethod
    async def login(db: Session, user_data: dict):
        email = user_data.get("email")
        password = user_data.get("password")

        try:
            query = select(User).where(User.email == email)
            result = db.execute(query)
            user = result.scalar_one_or_none()

            if not user or not verify_password(password, user.password):
                raise ValueError("Invalid email or password")
            
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
            raise e


    @staticmethod
    async def register(db: Session, user_data: dict):
        try:
            first_name = user_data["first_name"]
            last_name = user_data["last_name"]
            email = user_data["email"]
            password = user_data["password"]
            phone_number = user_data.get("phone_number")
            role = user_data["role"]

            user_email = db.query(User).filter(User.email == email).first()
            if user_email:
                raise ValueError("Email đã được sử dụng")
            
            existing_phone = db.query(User).filter(User.phone_number == phone_number).first()
            if existing_phone:
                raise ValueError("Số điện thoại đã được sử dụng")
            
            hash_pw = hash_password(password)

            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                password=hash_pw,
                role=role,
                status="active"
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
        except Exception as e:
            traceback.print_exc()
            raise e 
