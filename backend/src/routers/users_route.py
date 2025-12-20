from fastapi import APIRouter, Depends, HTTPException, Request, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from src.services.users_service import UserService
from src.schemas.user_schemas import UserUpdate, HistoryItem
from src.config.db_config import get_db
from src.utils.dependencies import get_current_user
from src.utils.file_uploads import save_image

users_router = APIRouter()

@users_router.get("/me")
async def get_user(
    request: Request,
    user: dict = Depends(get_current_user),
    db: Session=Depends(get_db)
):
    """
    Lấy thông tin cá nhân.
    
    Trả về thông tin chi tiết của người dùng đang đăng nhập.
    """

    try:
        user = await UserService.get_user_by_id(user_id=user.get("sub"), db=db)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@users_router.put("/me")
async def update_user_info(
    data: UserUpdate, 
    request: Request,
    user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Cập nhật thông tin cá nhân.
    
    Cho phép người dùng cập nhật thông tin profile và đổi mật khẩu.
    """
    try:
        user_data = {
            "avatar_url": data.avatar_url,
            "first_name": data.first_name,
            "last_name": data.last_name,
            "phone_number": data.phone_number,
            "old_password": data.old_password,
            "new_password": data.new_password,
        }

        auth_result = await UserService.update_user(user_id=user.get("sub"), user_data=user_data, db=db)

        return JSONResponse(content={
            "access_token": auth_result["access_token"],
            "token_type": "Bearer",
            }
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@users_router.get("/me/history", 
                response_model=List[HistoryItem],
                summary="Xem lịch sử tham gia sự kiện của bản thân")
async def get_my_participation_history(
    request: Request,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):    
    """
    Xem lịch sử tham gia.
    
    Trả về danh sách các sự kiện mà người dùng đã đăng ký tham gia kèm trạng thái.
    """
    try:
        history_items = await UserService.get_user_history(db=db, user_id=user.get("sub"))
        return history_items

    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@users_router.post("/avatar")
async def upload_image(
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user),
):
    """
    Tải ảnh đại diện lên Thư mục Public.
    
    Upload ảnh avatar và trả về URL.
    """
    try:
        return save_image(file, "users")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")