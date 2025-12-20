from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from src.config.db_config import get_db
from src.services.reacts_service import ReactService
from src.services.posts_service import PostService
from src.schemas.reacts_schemas import *
from src.utils.dependencies import get_current_user, role_required, active_status_required
reacts_router = APIRouter()

@reacts_router.post("/posts/{post_id}", response_model=ReactDetail)
async def create_react(
    request: Request, 
    post_id: int, 
    body: ReactCreate, 
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
    _2 = Depends(role_required(("manager", "volunteer"))),
    db: Session = Depends(get_db)
):
    """
    Thả cảm xúc (React) bài viết.
    
    Cho phép người dùng thả cảm xúc (like, love, haha...) vào một bài viết.
    Nếu đã react rồi thì sẽ cập nhật loại cảm xúc mới.
    """
    
    try:
        post = await PostService.get_post_by_id(db, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        react = await ReactService.create_react(db, post_id, user.get("sub"), body.category)

        return react
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    

@reacts_router.delete("/posts/{post_id}")
async def delete_react(
    request: Request,
    post_id: int, 
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
    _2 = Depends(role_required(("manager", "volunteer"))),
    db: Session = Depends(get_db)
):
    """
    Hủy thả cảm xúc.
    
    Xóa cảm xúc mà người dùng đã thả vào bài viết trước đó.
    """
    try:
        post = await PostService.get_post_by_id(db, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        result = await ReactService.delete_react(db, post_id, user_id = user.get("sub"))
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")