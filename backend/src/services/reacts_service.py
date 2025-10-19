from sqlalchemy.orm import Session
from sqlalchemy.future import select
from fastapi import HTTPException
from src.models.post_model import Post
from src.models.react_model import React
import traceback

class ReactService:
    @staticmethod
    async def create_react(db, post_id: int, user_id: int, category: str):
        """
        Tạo hoặc cập nhật cảm xúc cho bài post.
        """
        try:
            # Kiểm tra xem bài post có tồn tại không
            post = db.query(Post).filter(Post.post_id == post_id).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")

            # Kiểm tra xem đã react chưa
            query = select(React).where(React.post_id == post_id, React.user_id == user_id)
            existing_react = db.execute(query).scalar_one_or_none()

            if existing_react:
                # Nếu đã tồn tại → cập nhật lại category
                existing_react.category = category
                db.commit()
                db.refresh(existing_react)
                return existing_react

            # Nếu chưa tồn tại → tạo mới
            new_react = React(post_id=post_id, user_id=user_id, category=category)
            db.add(new_react)
            db.commit()
            db.refresh(new_react)
            return new_react
        except HTTPException:
            raise
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise

    @staticmethod
    async def delete_react(db: Session, post_id: int, user_id: int):
        """
        Xóa react khỏi database
        """
        try: 
            # Tạo câu truy vấn chọn bài post có đúng ID và thuộc về đúng user
            query = select(React).where(React.post_id == post_id, React.user_id == user_id)
            react = db.execute(query).scalar_one_or_none()# lấy duy nhất 1 kết quả hoặc None nếu không có
            if react:
                db.delete(react)
                db.commit()
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise