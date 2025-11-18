from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# React
class ReactCreate(BaseModel):
    category: str  # "like"

class ReactDetail(BaseModel):
    like_id: int
    post_id: int
    user_id: int
    category: str
    react_count: int

    class Config:
        from_attributes = True