from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.user_model import User
from src.models.comment_model import Comment
import traceback

class CommentService:
    @staticmethod
    async def get_comments_by_post(db: Session, post_id: int):
        try:
            comments = (
                db.query(
                    Comment.comment_id,
                    Comment.post_id,
                    Comment.user_id,
                    Comment.content,
                    Comment.created_at,
                    User.first_name,
                    User.last_name
                )
                .join(User, User.user_id == Comment.user_id)
                .filter(Comment.post_id == post_id)
                .order_by(Comment.created_at.asc())
                .all()
            )
            result = [
                {
                    "comment_id": c.comment_id,
                    "post_id": c.post_id,
                    "user_id": c.user_id,
                    "content": c.content,
                    "created_at": c.created_at,
                    "first_name": c.first_name,
                    "last_name": c.last_name,
                }
                for c in comments
            ]
            return result

        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise e

    @staticmethod
    async def create_comment(db: Session, post_id: int, user_id: int, content: str):
        try:
            comment = Comment(post_id=post_id, user_id=user_id, content=content)
            db.add(comment)
            db.commit()
            db.refresh(comment)
            user = db.query(User.first_name, User.last_name).filter(User.user_id == user_id).first()
            comment_count = db.query(Comment).filter(Comment.post_id == post_id).count()

            return {
                "comment_id": comment.comment_id,
                "post_id": comment.post_id,
                "user_id": comment.user_id,
                "content": comment.content,
                "created_at": comment.created_at,
                "first_name": user.first_name if user else None,
                "last_name": user.last_name if user else None,
                "comment_count": comment_count
            }

        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise e 
