from sqlalchemy.orm import Session
from sqlalchemy.future import select
from fastapi import HTTPException
from src.models.post_model import Post
from src.models.react_model import React
from src.models.user_model import User
import traceback

class ReactService:
    @staticmethod
    async def create_react(db: Session, post_id: int, user_id: int, category: str):
        """
        Tạo hoặc cập nhật cảm xúc cho bài post, trả về kèm react_count.
        """
        try:
            # Kiểm tra bài post tồn tại
            post = db.query(Post).filter(Post.post_id == post_id).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")

            # Kiểm tra đã react chưa
            existing_react = (
                db.query(React)
                .filter(React.post_id == post_id, React.user_id == user_id)
                .first()
            )

            if existing_react:
                # Nếu đã tồn tại → cập nhật lại category
                existing_react.category = category
                db.commit()
                db.refresh(existing_react)
                react_obj = existing_react
            else:
                # Nếu chưa tồn tại → tạo mới
                new_react = React(post_id=post_id, user_id=user_id, category=category)
                db.add(new_react)
                db.commit()
                db.refresh(new_react)
                react_obj = new_react

            # Lấy react_count mới nhất
            react_count = db.query(React).filter(React.post_id == post_id).count()

            return {
                "like_id": react_obj.like_id,
                "post_id": react_obj.post_id,
                "user_id": react_obj.user_id,
                "category": react_obj.category,
                "react_count": react_count
            }

        except HTTPException:
            raise
        except Exception:
            traceback.print_exc()
            db.rollback()
            raise HTTPException(status_code=500, detail="Error creating react")

    @staticmethod
    async def delete_react(db: Session, post_id: int, user_id: int):
        """
        Xóa react khỏi database và trả về react_count mới.
        """
        try:
            query = select(React).where(React.post_id == post_id, React.user_id == user_id)
            react = db.execute(query).scalar_one_or_none()
            if react:
                db.delete(react)
                db.commit()

            # Lấy react_count sau khi xóa
            react_count = db.query(React).filter(React.post_id == post_id).count()
            return {"detail": "React removed successfully", "react_count": react_count}

        except Exception:
            traceback.print_exc()
            db.rollback()
            raise HTTPException(status_code=500, detail="Error deleting react")
