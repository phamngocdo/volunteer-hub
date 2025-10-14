from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Post
class PostCreate(BaseModel):
    content: str
    images_url: Optional[str] = None

class PostDetail(PostCreate):
    post_id: int
    event_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True # giúp Pydantic chuyển đổi trực tiếp từ ORM object(SQLAlchemy) sang model mà không cần dict

