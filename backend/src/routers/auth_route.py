import os
from dotenv import load_dotenv

from pathlib import Path
from fastapi import APIRouter, Request, Depends, HTTPException,Form, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from authlib.jose import jwt
import requests

from config.db_config import get_db
from services.auth_service import AuthService, VerificationCodeService, CodeAlreadySentException
from schemas.auth_schemas import AuthLogin, AuthRegister

SRC_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

oauth = OAuth()

backend_port = os.getenv('BACKEND_PORT', 8000)
redirect_uri = f"http://localhost:{backend_port}/auth/google/callback"

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_uri': redirect_uri
    }
)


auth_router = APIRouter()

@auth_router.post("/login")
async def login(request: Request, login_data: AuthLogin, db: Session = Depends(get_db)):
    try:
        user_data = {
            "email": login_data.email,
            "password": login_data.password
        }
        auth_result = await AuthService.login(db=db, user_data=user_data)

        request.session["user"] = auth_result["user"]
        request.session["access_token"] = auth_result["access_token"]

        return JSONResponse(status_code=status.HTTP_200_OK, content=auth_result)

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@auth_router.get("/google")
async def login_with_google(request: Request): 
    """Bắt đầu quá trình đăng nhập bằng Google bằng cách chuyển hướng người dùng."""
    redirect_uri = request.url_for('login_with_google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@auth_router.get("/google/callback")
async def login_with_google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)

        jwks_url = "https://www.googleapis.com/oauth2/v3/certs"
        jwks = requests.get(jwks_url).json()

        claims = jwt.decode(token['id_token'], jwks)
        claims.validate()

        email = claims.get('email')
        if not email:
            raise HTTPException(status_code=400, detail="Email not found from Google")
        
        auth_result = await AuthService.login_with_google(db=db, email=email)

        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(key="access_token", value=auth_result["access_token"], httponly=True)
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@auth_router.post("/register")
async def register(register_data: AuthRegister, db: Session = Depends(get_db)):
    """Đăng ký tài khoản mới."""
    try:
        # Ánh xạ dữ liệu từ schema sang cấu trúc DB của bạn
        user_data = {
            "first_name": register_data.first_name,
            "last_name": register_data.last_name,
            "email": register_data.email,
            "phone_number": register_data.phone_number,
            "password": register_data.password,
            "role": register_data.role
        }
        await AuthService.register(db=db, user_data=user_data)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Registration successful. Please login."})
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")



@auth_router.post("/logout")
async def logout(request: Request):
    try:
        if "user" in request.session:
            del request.session["user"]
        
        if "access_token" in request.session:
            del request.session["access_token"]

        response = RedirectResponse(url="/auth/login", status_code=302)
        response.delete_cookie(key="access_token", path="/", httponly=True)

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

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
