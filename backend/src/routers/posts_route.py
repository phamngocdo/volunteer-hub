from fastapi import APIRouter, Request, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session

from typing import List
from src.config.db_config import get_db
from src.services.posts_service import PostService
from src.services.events_service import EventService
from src.schemas.posts_schemas import *
from src.utils.dependencies import get_current_user, role_required, active_status_required
from src.utils.file_uploads import save_image

posts_router = APIRouter()

@posts_router.get("/", response_model=List[PostAllDetail])
async def get_all_posts(
    request: Request, 
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
    _2 = Depends(role_required(("manager", "volunteer"))),
    db: Session = Depends(get_db)
):
    """
    Lấy tất cả bài viết trên bảng tin.
    
    Trả về danh sách tất cả các bài viết công khai, bao gồm cả thông tin người đăng và sự kiện liên quan.
    """

    try:

        user_id = user.get("sub")
        posts = await PostService.get_all_posts(db, user_id)
        return posts

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@posts_router.get("/events/{event_id}/", response_model=List[PostAllDetail])
async def get_posts_by_event(
    request: Request,
    event_id: int, 
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
    _2 = Depends(role_required(("manager", "volunteer"))),
    db: Session = Depends(get_db)
):
    """
    Lấy bài viết theo sự kiện.
    
    Trả về danh sách các bài viết thảo luận trong một sự kiện cụ thể.
    """

    try:
        user_id = user.get("sub")
        posts = await PostService.get_posts_by_event(db, event_id, user_id)
        return posts

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    

@posts_router.post("/events/{event_id}/", response_model=PostDetail)
async def create_post(
    request: Request,
    event_id: int, 
    post: PostCreate, 
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
    _2 = Depends(role_required(("manager", "volunteer"))),
    db: Session = Depends(get_db)
):
    """
    Tạo bài viết mới trong sự kiện.
    
    Cho phép tình nguyện viên hoặc người quản lý đăng bài viết thảo luận trong một sự kiện.
    """
    
    try:
        user_id = user.get("sub")
        event = await EventService.get_event_by_id(db, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        new_post = await PostService.create_post(db, event_id, user_id, post)
        if not new_post:
            raise HTTPException(status_code=404, detail="Event Id not found")
        return new_post
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@posts_router.delete("/{post_id}")
async def delete_post(
    request: Request, 
    post_id: int, 
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
    _2 = Depends(role_required(("manager", "volunteer"))),
    db: Session = Depends(get_db)
):
    """
    Xóa bài viết.
    
    Cho phép người dùng xóa bài viết của chính mình.
    """
    
    try:
        user_id = user.get("sub")
        success = await PostService.delete_post(db, post_id, user_id)
        if not success:
            raise HTTPException(status_code=403, detail="Post not found or unauthorized")

        return {"detail": "Post deleted successfully"}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    

@posts_router.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
):
    """
    Tải ảnh bài viết lên Thư mục Public.
    
    Upload ảnh đính kèm cho bài viết và trả về URL.
    """
    try:
        return save_image(file, "posts")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    

@posts_router.get("/users/me/", response_model=List[PostAllDetail])
async def get_posts_by_user(
    request: Request,
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
    _2 = Depends(role_required(("manager", "volunteer"))),
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách bài viết của tôi.
    
    Trả về tất cả các bài viết mà người dùng hiện tại đã đăng.
    """

    try:
        current_user_id = user.get("sub")
        posts = await PostService.get_posts_by_user(db, current_user_id, current_user_id)
        return posts

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")