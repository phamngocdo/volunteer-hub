from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.config.db_config import Base


class React(Base):
    __tablename__ = "reacts"

    like_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    category = Column(String(100))  # like | love | haha | wow | sad | angry
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint("post_id", "user_id", name="unique_post_user_react"),)

    # Relationships
    post = relationship("Post", back_populates="reacts")
    user = relationship("User", back_populates="reacts")
