from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReactCreate(BaseModel):
    category: str

class ReactDetail(BaseModel):
    react_id: int
    post_id: int
    user_id: int
    category: str
    react_count: int

    class Config:
        from_attributes = True