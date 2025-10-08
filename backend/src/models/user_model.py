from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.config.db_config import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    phone_number = Column(String(100))
    role = Column(String(20))  # volunteer | manager | admin
    status = Column(String(20))  # active | banned | pending
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    managed_events = relationship("Event", back_populates="manager")
    registrations = relationship("EventRegistration", back_populates="user")
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    reacts = relationship("React", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
