from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.config.db_config import Base


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("events.event_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    images_url = Column(String(200))
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    event = relationship("Event", back_populates="posts")
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    reacts = relationship("React", back_populates="post")
