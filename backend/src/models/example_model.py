from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP, func, CheckConstraint
from sqlalchemy.orm import relationship
from config.db_config import Base

class ReviewModel(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE"), nullable=False)
    buyer_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint('rating BETWEEN 1 AND 5', name='check_rating_between_1_and_5'),
    )

    product = relationship("ProductModel", backref="reviews")
    buyer = relationship("UserModel", backref="reviews")
