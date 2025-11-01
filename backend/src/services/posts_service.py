from sqlalchemy.orm import Session
from sqlalchemy import func, select
from src.models.post_model import Post
from src.models.user_model import User
from src.models.comment_model import Comment
from src.models.react_model import React
from src.services.events_service import EventService
from fastapi import HTTPException

import traceback

class PostService:
    from sqlalchemy import select, func
from src.models import Post, User, React, Comment

class PostService:
    @staticmethod
    async def get_all_posts(db: Session, current_user_id: int):
        """
        Lấy tất cả bài post, kèm:
        - Tên người đăng
        - Số lượng react
        - React của user hiện tại
        - Số lượng comment
        """
        try:
            # --- Subquery: Đếm số react theo post_id ---
            react_subquery = (
                select(
                    React.post_id,
                    func.count(React.like_id).label("react_count")
                )
                .group_by(React.post_id)
                .subquery()
            )

            # --- Subquery: Đếm số comment theo post_id ---
            comment_subquery = (
                select(
                    Comment.post_id,
                    func.count(Comment.comment_id).label("comment_count")
                )
                .group_by(Comment.post_id)
                .subquery()
            )

            # --- Truy vấn chính ---
            post_query = (
                select(
                    Post,
                    User.first_name,
                    User.last_name,
                    func.coalesce(react_subquery.c.react_count, 0).label("react_count"),
                    func.coalesce(comment_subquery.c.comment_count, 0).label("comment_count")
                )
                .join(User, User.user_id == Post.user_id)
                .outerjoin(react_subquery, react_subquery.c.post_id == Post.post_id)
                .outerjoin(comment_subquery, comment_subquery.c.post_id == Post.post_id)
                .order_by(Post.created_at.desc())
            )

            posts_result = db.execute(post_query).all()

            # --- Lấy react của user hiện tại ---
            user_reacts_query = select(React.post_id, React.category).where(React.user_id == current_user_id)
            user_reacts_result = db.execute(user_reacts_query).all()
            user_reacts = {pid: cat for pid, cat in user_reacts_result}

            # --- Gộp dữ liệu ---
            posts_data = []
            for post, first_name, last_name, react_count, comment_count in posts_result:
                posts_data.append({
                    "post_id": post.post_id,
                    "content": post.content,
                    "images_url": post.images_url,
                    "event_id": post.event_id,
                    "user_id": post.user_id,
                    "created_at": post.created_at,
                    "first_name": first_name,
                    "last_name": last_name,
                    "react_count": react_count,
                    "comment_count": comment_count,
                    "user_react": user_reacts.get(post.post_id)  # react của user hiện tại
                })

            return posts_data

        except Exception:
            import traceback
            traceback.print_exc()
            raise

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