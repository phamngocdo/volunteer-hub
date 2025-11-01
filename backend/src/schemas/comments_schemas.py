from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Comment
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
        from_attributes = True # giúp Pydantic chuyển đổi trực tiếp từ ORM object(SQLAlchemy) sang model mà không cần dict

class CreateCommentDetail(BaseModel):
    comment_id: int
    post_id: int
    user_id: int
    content: str
    created_at: datetime
    first_name: str
    last_name: str
    comment_count: int

    class Config:
        from_attributes = True