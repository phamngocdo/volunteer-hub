from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jwt import InvalidTokenError, ExpiredSignatureError

import json
from typing import List, Optional
from src.config.db_config import get_db
from src.services.reacts_service import ReactService
from src.services.users_service import UserService
from src.schemas.reacts_schemas import *
from src.config.redis_config import redis_client as r

reacts_router = APIRouter()

# trả về 1 đối tượng reactdetail
@reacts_router.post("/posts/{post_id}", response_model=ReactDetail)
async def create_react(request: Request, post_id: int, body: ReactCreate, db: Session = Depends(get_db)):
    """
    Thả cảm xúc 1 bài post(chưa có thì tạo nếu có rồi thì update)
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth_header.split(" ")[1]

    session_json = await r.get(token)
    if not session_json:
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    
    try:
        # Kiểm tra JWT, signature và expiry giống /users/me
        user = await UserService.get_current_user(token=token, db=db)
        if user.get("role") == "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin not authorized")
        if user.get("status") == "banned":
            raise HTTPException(status_code=403, detail="Your account has been banned")
        user_id = user.get("user_id")
        react = await ReactService.create_react(db, post_id, user_id, body.category)
        return react
    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@reacts_router.delete("/posts/{post_id}")
async def delete_react(request: Request, post_id: int, db: Session = Depends(get_db)):
    """
    Bỏ cảm xúc bài post
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth_header.split(" ")[1]
    session_json = await r.get(token)
    if not session_json:
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    try:
        # Kiểm tra JWT, signature và expiry giống /users/me
        user = await UserService.get_current_user(token=token, db=db)
        if user.get("role") == "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin not authorized")
        if user.get("status") == "banned":
            raise HTTPException(status_code=403, detail="Your account has been banned")
        user_id = user.get("user_id")
        result = await ReactService.delete_react(db, post_id, user_id)
        return result
    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")