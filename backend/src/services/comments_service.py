from sqlalchemy.orm import Session
from sqlalchemy.future import select
from src.models.comment_model import Comment
import traceback

class CommentService:
    @staticmethod
    async def create_comment(db: Session, post_id: int, user_id: int, content: str):
        """
        Tạo một comment mới trong database.
        """
        try:
            comment = Comment(post_id=post_id, user_id=user_id, content=content)
            db.add(comment)
            db.commit()
            db.refresh(comment)
            return comment
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise