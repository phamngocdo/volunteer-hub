from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from src.config.db_config import get_db
from src.services.reacts_service import ReactService
from src.schemas.reacts_schemas import *

reacts_router = APIRouter()

# trả về 1 đối tượng reactdetail
@reacts_router.post("/posts/{post_id}", response_model=ReactDetail)
async def create_react(request: Request, post_id: int, body: ReactCreate, db: Session = Depends(get_db)):
    """
    Thả cảm xúc 1 bài post(chưa có thì tạo nếu có rồi thì update)
    """
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await ReactService.create_react(db, post_id, user["user_id"], body.category)

@reacts_router.delete("/posts/{post_id}")
async def delete_react(request: Request, post_id: int, db: Session = Depends(get_db)):
    """
    Bỏ cảm xúc bài post
    """
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    await ReactService.delete_react(db, post_id, user["user_id"])
    return {"detail": "React removed successfully"}