from sqlalchemy.orm import Session
from sqlalchemy.future import select
from fastapi import HTTPException
from src.models.post_model import Post
from src.models.comment_model import Comment
import traceback

class CommentService:
    @staticmethod
    async def create_comment(db: Session, post_id: int, user_id: int, content: str):
        """
        Tạo một comment mới trong database.
        """
        try:
            # Kiểm tra xem bài post có tồn tại không
            post = db.query(Post).filter(Post.post_id == post_id).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")
            # Nếu có thì tạo comment
            comment = Comment(post_id=post_id, user_id=user_id, content=content)
            db.add(comment)
            db.commit()
            db.refresh(comment)
            return comment
        except HTTPException:
            raise
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise