from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jwt import InvalidTokenError, ExpiredSignatureError

import json
from typing import List, Optional
from src.config.db_config import get_db
from src.services.comments_service import CommentService
from src.schemas.comments_schemas import *
from src.config.redis_config import redis_client as r

comments_router = APIRouter()

# trả về 1 đối tượng commentdetail
@comments_router.post("/posts/{post_id}", response_model=CommentDetail)
async def create_comment(request: Request, post_id: int, body: CommentCreate, db: Session = Depends(get_db)):
    """
    Bình luận 1 bài post
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth_header.split(" ")[1]
    session_json = await r.get(token)
    if not session_json:
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    if session_json['role'] == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin not authorized")

    try:
        user = json.loads(session_json)
        if user.get("status") == "banned":
            raise HTTPException(status_code=403, detail="Your account has been banned")
        user_id = user.get("user_id")
        comment = await CommentService.create_comment(db, post_id, user_id, body.content)
        return comment
    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")