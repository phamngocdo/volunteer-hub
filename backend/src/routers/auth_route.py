from dotenv import load_dotenv

from pathlib import Path
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.config.db_config import get_db
from src.services.auth_service import AuthService
from src.schemas.auth_schemas import AuthLogin, AuthRegister

SRC_DIR = Path(__file__).resolve().parent.parent
SESSION_EXPIRE_SECONDS = 60*60*24*14 # 14 days

load_dotenv()

auth_router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 60

@auth_router.post("/login")
async def login(
    request: Request,
    login_data: AuthLogin, 
    db: Session = Depends(get_db)
):
    """
    Đăng nhập vào hệ thống.
    
    API này nhận email và mật khẩu, kiểm tra thông tin xác thực và trả về access token nếu hợp lệ.
    """
    try:
        user_data = {
            "email": login_data.email,
            "password": login_data.password
        }

        auth_result = await AuthService.login(db=db, user_data=user_data)

        return JSONResponse(content={
            "access_token": auth_result["access_token"],
            "token_type": "Bearer",
            }
        )

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@auth_router.post("/register")
async def register(
    register_data: AuthRegister, 
    db: Session = Depends(get_db)
):
    """
    Đăng ký tài khoản mới.
    
    API này cho phép người dùng đăng ký tài khoản mới với vai trò 'volunteer' hoặc 'manager'.
    """
    try:
        user_data = {
            "first_name": register_data.first_name,
            "last_name": register_data.last_name,
            "email": register_data.email,
            "phone_number": register_data.phone_number,
            "password": register_data.password,
            "role": register_data.role
        }
        await AuthService.register(db=db, user_data=user_data)
        return JSONResponse(status_code=201, content={"message": "User registered successfully"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")