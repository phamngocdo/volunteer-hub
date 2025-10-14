from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from src.config.db_config import get_db
from src.services.comments_service import CommentService
from src.schemas.comments_schemas import *

comments_router = APIRouter()

# trả về 1 đối tượng commentdetail
@comments_router.post("/posts/{post_id}", response_model=CommentDetail)
async def create_comment(request: Request, post_id: int, body: CommentCreate, db: Session = Depends(get_db)):
    """
    Bình luận 1 bài post
    """
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await CommentService.create_comment(db, post_id, user["user_id"], body.content)