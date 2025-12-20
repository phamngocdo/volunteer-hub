from sqlalchemy.orm import Session
from sqlalchemy import func, select
from src.models.post_model import Post
from src.models.user_model import User
from src.models.event_model import Event
from src.models.comment_model import Comment
from src.models.react_model import React

import traceback

class PostService:
    @staticmethod
    async def get_post_by_id(db: Session, post_id:int):
        try:
            post = db.query(Post).filter(Post.post_id == post_id).first()
            return post
        except Exception as e:
            traceback.print_exc()
            raise e 

    @staticmethod
    async def get_all_posts(db: Session, current_user_id: int):
        try:
            react_subquery = (
                select(
                    React.post_id,
                    func.count(React.react_id).label("react_count")
                )
                .group_by(React.post_id)
                .subquery()
            )

            comment_subquery = (
                select(
                    Comment.post_id,
                    func.count(Comment.comment_id).label("comment_count")
                )
                .group_by(Comment.post_id)
                .subquery()
            )

            post_query = (
                select(
                    Post,
                    User.first_name,
                    User.last_name,
                    User.avatar_url,
                    Event.title.label("event_title"),
                    func.coalesce(react_subquery.c.react_count, 0).label("react_count"),
                    func.coalesce(comment_subquery.c.comment_count, 0).label("comment_count")
                )
                .join(User, User.user_id == Post.user_id)
                .join(Event, Event.event_id == Post.event_id)
                .outerjoin(react_subquery, react_subquery.c.post_id == Post.post_id)
                .outerjoin(comment_subquery, comment_subquery.c.post_id == Post.post_id)
                .order_by(Post.created_at.desc())
            )

            posts_result = db.execute(post_query).all()

            user_reacts_query = select(React.post_id, React.category).where(React.user_id == current_user_id)
            user_reacts_result = db.execute(user_reacts_query).all()
            user_reacts = {pid: cat for pid, cat in user_reacts_result}

            posts_data = []
            for post, first_name, last_name, avatar_url, event_title, react_count, comment_count in posts_result:
                posts_data.append({
                    "post_id": post.post_id,
                    "content": post.content,
                    "images_url": post.images_url,
                    "event_id": post.event_id,
                    "user_id": post.user_id,
                    "created_at": post.created_at,
                    "first_name": first_name,
                    "last_name": last_name,
                    "avatar_url": avatar_url,
                    "event_title": event_title,
                    "react_count": react_count,
                    "comment_count": comment_count,
                    "user_react": user_reacts.get(post.post_id)
                })

            return posts_data

        except Exception as e:
            traceback.print_exc()
            raise e

    @staticmethod
    async def get_posts_by_event(db: Session, event_id: int, current_user_id: int):
        try:
            react_subquery = (
                select(
                    React.post_id,
                    func.count(React.react_id).label("react_count")
                )
                .group_by(React.post_id)
                .subquery()
            )

            comment_subquery = (
                select(
                    Comment.post_id,
                    func.count(Comment.comment_id).label("comment_count")
                )
                .group_by(Comment.post_id)
                .subquery()
            )

            post_query = (
                select(
                    Post,
                    User.first_name,
                    User.last_name,
                    User.avatar_url,
                    Event.title.label("event_title"),
                    func.coalesce(react_subquery.c.react_count, 0).label("react_count"),
                    func.coalesce(comment_subquery.c.comment_count, 0).label("comment_count")
                )
                .join(User, User.user_id == Post.user_id)
                .join(Event, Event.event_id == Post.event_id)
                .outerjoin(react_subquery, react_subquery.c.post_id == Post.post_id)
                .outerjoin(comment_subquery, comment_subquery.c.post_id == Post.post_id)
                .where(Post.event_id == event_id)
                .order_by(Post.created_at.desc())
            )

            posts_result = db.execute(post_query).all()

            user_reacts_query = select(React.post_id, React.category).where(React.user_id == current_user_id)
            user_reacts_result = db.execute(user_reacts_query).all()
            user_reacts = {pid: cat for pid, cat in user_reacts_result}

            posts_data = []
            for post, first_name, last_name, avatar_url, event_title, react_count, comment_count in posts_result:
                posts_data.append({
                    "post_id": post.post_id,
                    "content": post.content,
                    "images_url": post.images_url,
                    "event_id": post.event_id,
                    "user_id": post.user_id,
                    "created_at": post.created_at,
                    "first_name": first_name,
                    "last_name": last_name,
                    "avatar_url": avatar_url,
                    "event_title": event_title,
                    "react_count": react_count,
                    "comment_count": comment_count,
                    "user_react": user_reacts.get(post.post_id)
                })

            return posts_data

        except Exception as e:
            traceback.print_exc()
            raise e

        
    @staticmethod
    async def create_post(db: Session, event_id: int, user_id: int, post):
        try:      
            db_post = Post(event_id=event_id, user_id=user_id, **post.dict())
            db.add(db_post)
            db.commit()
            db.refresh(db_post)
            return db_post
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise e

    @staticmethod
    async def delete_post(db: Session, post_id: int, user_id: int):
        try: 
            query = select(Post).where(Post.post_id == post_id, Post.user_id == user_id)
            post = db.execute(query).scalar_one_or_none()
            if not post:
                return False
            db.delete(post)
            db.commit()
            return True
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise e

    @staticmethod
    async def get_posts_by_user(db: Session, target_user_id: int, current_user_id: int):
        try:
            react_subquery = (
                select(
                    React.post_id,
                    func.count(React.react_id).label("react_count")
                )
                .group_by(React.post_id)
                .subquery()
            )

            comment_subquery = (
                select(
                    Comment.post_id,
                    func.count(Comment.comment_id).label("comment_count")
                )
                .group_by(Comment.post_id)
                .subquery()
            )

            post_query = (
                select(
                    Post,
                    User.first_name,
                    User.last_name,
                    User.avatar_url,
                    Event.title.label("event_title"),
                    func.coalesce(react_subquery.c.react_count, 0).label("react_count"),
                    func.coalesce(comment_subquery.c.comment_count, 0).label("comment_count")
                )
                .join(User, User.user_id == Post.user_id)
                .join(Event, Event.event_id == Post.event_id)
                .outerjoin(react_subquery, react_subquery.c.post_id == Post.post_id)
                .outerjoin(comment_subquery, comment_subquery.c.post_id == Post.post_id)
                .where(Post.user_id == target_user_id)
                .order_by(Post.created_at.desc())
            )

            posts_result = db.execute(post_query).all()

            user_reacts_query = select(React.post_id, React.category).where(React.user_id == current_user_id)
            user_reacts_result = db.execute(user_reacts_query).all()
            user_reacts = {pid: cat for pid, cat in user_reacts_result}

            posts_data = []
            for post, first_name, last_name, avatar_url, event_title, react_count, comment_count in posts_result:
                posts_data.append({
                    "post_id": post.post_id,
                    "content": post.content,
                    "images_url": post.images_url,
                    "event_id": post.event_id,
                    "user_id": post.user_id,
                    "created_at": post.created_at,
                    "first_name": first_name,
                    "last_name": last_name,
                    "avatar_url": avatar_url,
                    "event_title": event_title,
                    "react_count": react_count,
                    "comment_count": comment_count,
                    "user_react": user_reacts.get(post.post_id)
                })

            return posts_data

        except Exception as e:
            traceback.print_exc()
            raise e
