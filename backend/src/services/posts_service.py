from sqlalchemy.orm import Session
from sqlalchemy.future import select
from src.models.post_model import Post
from src.services.events_service import EventService
from fastapi import HTTPException
from src.models.react_model import React
import traceback

class PostService:
    @staticmethod
    async def get_posts_by_event(db: Session, event_id: int):
        """
        Tìm và trả về các bài post theo ID.
        """
        try:
            query = select(Post).where(Post.event_id == event_id)
            return db.execute(query).scalars().all()
        except Exception as e:
            traceback.print_exc()
            raise
        
    @staticmethod
    async def create_post(db: Session, event_id: int, user_id: int, post):
        """
        Tạo 1 post mới trong database.
        """
        try:      
            # Kiểm tra sự kiện tồn tại và phải được 'approved'
            event = await EventService.get_event_by_id(db, event_id)
            if not event:
                raise HTTPException(status_code=404, detail="Event not found")
            if event.status.lower() != "approved":
                raise HTTPException(status_code=403, detail="Event not approved yet")
            # Nếu thỏa mãn thì tạo post
            db_post = Post(event_id=event_id, user_id=user_id, **post.dict())
            db.add(db_post)
            db.commit()
            db.refresh(db_post)
            return db_post
        except HTTPException:
            raise
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise

    @staticmethod
    async def delete_post(db: Session, post_id: int, user_id: int):
        """
        Xóa bài post khỏi database nếu bài viết thuộc về user tương ứng.
        """
        try: 
            # Tạo câu truy vấn chọn bài post có đúng ID và thuộc về đúng user
            query = select(Post).where(Post.post_id == post_id, Post.user_id == user_id)
            post = db.execute(query).scalar_one_or_none() # lấy duy nhất 1 kết quả hoặc None nếu không có
            if not post:
                return False
            db.delete(post)
            db.commit()
            return True
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise