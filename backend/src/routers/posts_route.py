from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jwt import InvalidTokenError, ExpiredSignatureError

from typing import List, Optional
import json
from src.config.db_config import get_db
from src.services.posts_service import PostService
from src.services.users_service import UserService
from src.schemas.posts_schemas import *
from src.config.redis_config import redis_client as r

posts_router = APIRouter()

# trả về danh sách các đối tượng postalldetail
@posts_router.get("/", response_model=List[PostAllDetail])
async def get_all_posts(request: Request, db: Session = Depends(get_db)):
    """
    Lấy tất cả bài post của tất cả sự kiện, kèm:
    - Thông tin người đăng (first_name, last_name)
    - Số lượng react
    - React của user hiện tại
    - Số lượng comment
    """
    # --- Kiểm tra token ---
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

        posts = await PostService.get_all_posts(db, user_id)
        return posts

    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")



# trả về danh sách các đối tượng postdetail
@posts_router.get("/events/{event_id}/", response_model=List[PostDetail])
async def get_posts_by_event(request: Request, event_id: int, db: Session = Depends(get_db)):
    """
    Lấy tất cả bài post của 1 sự kiện.
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

        posts = await PostService.get_posts_by_event(db, event_id)
        return posts

    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# trả về 1 đối tượng postdetail
@posts_router.post("/events/{event_id}/", response_model=PostDetail)
async def create_post(request: Request, event_id: int, post: PostCreate, db: Session = Depends(get_db)):
    """
    Đăng bài viết mới của 1 sự kiện
    """
    #Lấy token
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth_header.split(" ")[1]
    #Lấy thông tin user trong Redis
    session_json = await r.get(token)
    if not session_json:
        raise HTTPException(status_code=401, detail="Session expired or invalid")   
    
    try:
        # Kiểm tra JWT, signature và expiry giống /users/me
        user = await UserService.get_current_user(token=token, db=db)
        if user.get("role") == "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin not authorized")
        # Kiểm tra nếu bị cấm
        if user.get("status") == "banned":
            raise HTTPException(status_code=403, detail="Your account has been banned")
        user_id = user.get("user_id")
        new_post = await PostService.create_post(db, event_id, user_id, post)
        return new_post
    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@posts_router.delete("/{post_id}")
async def delete_post(request: Request, post_id: int, db: Session = Depends(get_db)):
    """
    Xóa bài post khỏi database nếu bài viết thuộc về user tương ứng.
    """
    # --- Lấy token ---
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = auth_header.split(" ")[1]

    # --- Lấy thông tin user trong Redis ---
    session_json = await r.get(token)
    if not session_json:
        raise HTTPException(status_code=401, detail="Session expired or invalid")  
    
    try:
        # Kiểm tra JWT, signature và expiry giống /users/me
        user = await UserService.get_current_user(token=token, db=db)
        if user.get("role") == "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin not authorized")
        # Kiểm tra nếu bị cấm
        if user.get("status") == "banned":
            raise HTTPException(status_code=403, detail="Your account has been banned")

        user_id = user.get("user_id")

        success = await PostService.delete_post(db, post_id, user_id)
        if not success:
            raise HTTPException(status_code=403, detail="Post not found or unauthorized")

        return {"detail": "Post deleted successfully"}

    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

