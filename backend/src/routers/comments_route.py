from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import List
from src.config.db_config import get_db
from src.services.comments_service import CommentService
from src.services.posts_service import PostService
from src.utils.dependencies import get_current_user, role_required, active_status_required
from src.schemas.comments_schemas import *

comments_router = APIRouter()

@comments_router.get("/posts/{post_id}", response_model=List[CommentDetail])
async def get_comments_by_post(
    request: Request,
    post_id: int,
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
    _2 = Depends(role_required(("manager", "volunteer"))),
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách bình luận của bài viết.
    
    Trả về tất cả bình luận thuộc về một bài viết cụ thể.
    """
    try:
        comments = await CommentService.get_comments_by_post(db, post_id)
        return comments

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    

@comments_router.post("/posts/{post_id}", response_model=CreateCommentDetail)
async def create_comment(
    request: Request,
    post_id: int, 
    body: CommentCreate,
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
    _2 = Depends(role_required(("manager", "volunteer"))),
    db: Session = Depends(get_db)
):
    """
    Tạo bình luận mới.
    
    Cho phép người dùng thêm bình luận vào một bài viết.
    """

    try:
        post = await PostService.get_post_by_id(db, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        comment = await CommentService.create_comment(db, post_id, user.get("sub"), body.content)
        if not comment:
            raise HTTPException(status_code=404, detail="Post not found")
        return comment
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")