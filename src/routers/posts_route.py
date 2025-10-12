from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from src.config.db_config import get_db
from src.services.posts_service import PostService
from src.schemas.posts_schemas import *

posts_router = APIRouter()
# trả về danh sách các đối tượng postdetail
@posts_router.get("/events/{event_id}/", response_model=List[PostDetail])
async def get_posts_by_event(event_id: int, db: Session = Depends(get_db)):
    """
    Lấy tất cả bài post của 1 sự kiện
    """
    posts = await PostService.get_posts_by_event(db, event_id)
    return posts

# trả về 1 đối tượng postdetail
@posts_router.post("/events/{event_id}/", response_model=PostDetail)
async def create_post(request: Request, event_id: int, post: PostCreate, db: Session = Depends(get_db)):
    """
    Đăng bài viết mới của 1 sự kiện
    """
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    new_post = await PostService.create_post(db, event_id, user["user_id"], post)
    return new_post

@posts_router.delete("/{post_id}")
async def delete_post(request: Request, post_id: int, db: Session = Depends(get_db)):
    """
    Xóa bài post khỏi database nếu bài viết thuộc về user tương ứng.
    """
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    success = await PostService.delete_post(db, post_id, user["user_id"])
    if not success:
        raise HTTPException(status_code=403, detail="Post not found or unauthorized")
    return {"detail": "Post deleted successfully"}

