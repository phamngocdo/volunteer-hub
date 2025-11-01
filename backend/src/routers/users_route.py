from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from jwt import InvalidTokenError, ExpiredSignatureError
from sqlalchemy.orm import Session
from src.services.users_service import UserService
from src.schemas.user_schemas import UserUpdate, HistoryItem
from typing import Optional, List
import traceback

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
async def update_user_info(
    data: UserUpdate, 
    request: Request, 
    db: Session = Depends(get_db)
):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = auth_header.split(" ")[1]
    session_json = await r.get(token)

    if not session_json:
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    try:
        user_data = {
            "first_name": data.first_name,
            "last_name": data.last_name,
            "email": data.email,
            "phone_number": data.phone_number,
            "old_password": data.old_password,
            "new_password": data.new_password,
        }

        await UserService.update_current_user(token=token, user_data=user_data, db=db)

        return JSONResponse(
            status_code=200,
            content={"message": "User information updated successfully"}
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")
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
        raise HTTPException(status_code=403, detail="Not authorized to view history")
    
    user_id = user["user_id"]

    history_items = await UserService.get_user_history(db=db, user_id=user_id)
    return history_items

@users_router.get("/me/history", 
                response_model=List[HistoryItem],
                summary="Xem lịch sử tham gia sự kiện của bản thân")
async def get_my_participation_history(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    API để tình nguyện viên lấy danh sách lịch sử các sự kiện đã đăng ký.
    Yêu cầu xác thực với vai trò 'volunteer'.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = auth_header.split(" ")[1]

    # Lấy session từ Redis để xác thực và lấy thông tin
    session_json = await r.get(token)
    if not session_json:
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    
    try:
        # Kiểm tra vai trò người dùng trong session
        if session_json.get('role') != 'volunteer':
            raise HTTPException(
                status_code=403, 
                detail="Not authorized to view history. Volunteer role required."
            )
        
        user_id = session_json.get('user_id')
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in session")

        # Gọi service để lấy dữ liệu lịch sử
        history_items = await UserService.get_user_history(db=db, user_id=user_id)
        return history_items

    except HTTPException as e:
        raise e
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Could not fetch user history")