from sqlalchemy.orm import Session
from sqlalchemy.future import select
from src.models.react_model import React
import traceback

class ReactService:
    @staticmethod
    async def create_react(db: Session, post_id: int, user_id: int, category: str):
        try:
            existing_react = (
                db.query(React)
                .filter(React.post_id == post_id, React.user_id == user_id)
                .first()
            )

            if existing_react:
                existing_react.category = category
                db.commit()
                db.refresh(existing_react)
                react_obj = existing_react
            else:
                new_react = React(post_id=post_id, user_id=user_id, category=category)
                db.add(new_react)
                db.commit()
                db.refresh(new_react)
                react_obj = new_react

            react_count = db.query(React).filter(React.post_id == post_id).count()

            return {
                "react_id": react_obj.react_id,
                "post_id": react_obj.post_id,
                "user_id": react_obj.user_id,
                "category": react_obj.category,
                "react_count": react_count
            }

        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise e

    @staticmethod
    async def delete_react(db: Session, post_id: int, user_id: int):
        try:
            query = select(React).where(React.post_id == post_id, React.user_id == user_id)
            react = db.execute(query).scalar_one_or_none()
            if react:
                db.delete(react)
                db.commit()

            react_count = db.query(React).filter(React.post_id == post_id).count()
            return {"detail": "React removed successfully", "react_count": react_count}

        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise e 
