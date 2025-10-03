import traceback
from sqlalchemy.orm import Session
from models.example_model import ReviewModel

class ReviewService():
    @staticmethod
    async def get_review_by_id(review_id: int, db: Session):
        try:
            review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
            return review if review else None
        except Exception as e:
            traceback.print_exc()
            raise 
    
    @staticmethod
    async def get_review_by_product_id(product_id: int, db: Session):
        try:
            reviews = db.query(ReviewModel).filter(ReviewModel.product_id == product_id).all()
            return reviews if reviews else None
        except Exception as e:
            traceback.print_exc()
            raise 