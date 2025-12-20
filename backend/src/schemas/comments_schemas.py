from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CommentCreate(BaseModel):
    content: str

class CommentDetail(BaseModel):
    comment_id: int
    post_id: int
    user_id: int
    content: str
    created_at: datetime
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

class CreateCommentDetail(CommentDetail):
    comment_count: int