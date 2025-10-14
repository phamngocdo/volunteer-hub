import os
from dotenv import load_dotenv

from pathlib import Path
from fastapi import APIRouter, Request, Depends, HTTPException,Form, status
from fastapi.responses import JSONResponse
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from authlib.jose import jwt
import json

from src.config.db_config import get_db
from src.config.redis_config import redis_client as r
from src.services.auth_service import AuthService, VerificationCodeService, CodeAlreadySentException
from src.schemas.auth_schemas import AuthLogin, AuthRegister

SRC_DIR = Path(__file__).resolve().parent.parent
SESSION_EXPIRE_SECONDS = 60*60*24*14 # 14 days

load_dotenv()

auth_router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 60

@auth_router.post("/login")
async def login(request: Request, login_data: AuthLogin, db: Session = Depends(get_db)):
    try:
        user_data = {
            "email": login_data.email,
            "password": login_data.password
        }

        auth_result = await AuthService.login(db=db, user_data=user_data)

        token = auth_result["access_token"]

        session_data = {
            "user_id": auth_result["user"]["user_id"],
            "email": auth_result["user"]["email"]
        }
        try:
            await r.set(token, json.dumps(session_data), ex=SESSION_EXPIRE_SECONDS)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Redis error: {e}")

        return JSONResponse(content={"access_token": auth_result["access_token"], "token_type": "Bearer"})

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@auth_router.post("/register")
async def register(register_data: AuthRegister, db: Session = Depends(get_db)):
    """Đăng ký tài khoản mới."""
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
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User registered successfully"})
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")



@auth_router.post("/logout")
async def logout(request: Request):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Unauthorized")
        token = auth_header.split(" ")[1]

        deleted = await r.delete(token)
        if deleted == 0:
            raise HTTPException(status_code=400, detail="Session not found or already expired")

        return {"detail": "Logout successful"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    

@auth_router.post("/verify-code")
async def send_verify_code(email: str, db: Session = Depends(get_db)):
    """Gửi mã xác thực đến email."""
    try:
        await VerificationCodeService.send_code(db=db, email=email)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Verification code sent successfully"})
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except CodeAlreadySentException as e:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
