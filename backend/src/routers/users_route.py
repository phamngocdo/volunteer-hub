from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from jwt import InvalidTokenError, ExpiredSignatureError
from sqlalchemy.orm import Session
from src.services.users_service import UserService
from src.schemas.user_schemas import UserUpdate, HistoryItem
from typing import Optional, List

from src.config.db_config import get_db
from src.config.redis_config import redis_client as r

users_router = APIRouter()

@users_router.get("/me")
async def get_current_user(request: Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth_header.split(" ")[1]

    session_json = await r.get(token)
    if not session_json:
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    try:
        user = await UserService.get_current_user(token=token, db=db)
        return user
    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@users_router.put("/me")
async def update_password(data: UserUpdate, request: Request, db: Session = Depends(get_db)):
    try:
        token = request.session.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user_data = {
            "password": data.password
        }
        await UserService.update_current_user(token=token, user_data=user_data, db=db)
        return JSONResponse(status_code=200, content={"message": "Update password successfull"})
    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@users_router.get("/me/history", response_model=List[HistoryItem])
async def get_my_participation_history(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách lịch sử các sự kiện đã đăng ký/tham gia của người dùng.
    """
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    role = user["role"]
    if role != "volunteer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view history")
    
    user_id = user["user_id"]

    history_items = await UserService.get_user_history(db=db, user_id=user_id)
    return history_items