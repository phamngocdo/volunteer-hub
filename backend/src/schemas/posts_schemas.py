from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PostCreate(BaseModel):
    content: str
    images_url: Optional[str] = None

class PostDetail(PostCreate):
    post_id: int
    event_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PostAllDetail(BaseModel):
    post_id: int
    content: str
    images_url: Optional[str] = None
    event_id: int
    user_id: int
    created_at: datetime
    first_name: str
    last_name: str
    event_title: Optional[str] = None
    react_count: int
    comment_count: int
    user_react: Optional[str] = None

    class Config:
        from_attributes = True
