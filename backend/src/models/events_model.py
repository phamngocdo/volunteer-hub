from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    Boolean,
    Date,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.db_config import Base

# Lớp User tương ứng với bảng "users"
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(Text, nullable=False)
    phone_number = Column(String(100), nullable=True)
    role = Column(String(20), nullable=False)  # 'volunteer', 'manager', 'admin'
    status = Column(String(20), nullable=False, default='active') # 'active', 'banned', 'pending'
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Định nghĩa các mối quan hệ (relationships)
    managed_events = relationship("Event", back_populates="manager")
    registrations = relationship("EventRegistration", back_populates="user")
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    reacts = relationship("React", back_populates="user")
    notifications = relationship("Notification", back_populates="user")


# Lớp Event tương ứng với bảng "events"
class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True)
    manager_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    title = Column(String(200), nullable=False)
    image_url = Column(String(200), nullable=True)
    description = Column(Text)
    category = Column(String(100))
    location = Column(String(200))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(20), nullable=False, default='pending') # 'pending', 'approved', 'rejected', 'completed'
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    manager = relationship("User", back_populates="managed_events")
    registrations = relationship("EventRegistration", back_populates="event", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="event", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="event", cascade="all, delete-orphan")


# Lớp EventRegistration tương ứng với bảng "event_registrations"
class EventRegistration(Base):
    __tablename__ = "event_registrations"
    __table_args__ = (UniqueConstraint('event_id', 'user_id', name='_event_user_uc'),)

    registration_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.event_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    status = Column(String(20), nullable=False, default='pending') # 'pending', 'approved', 'rejected', 'cancelled', 'completed'
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    event = relationship("Event", back_populates="registrations")
    user = relationship("User", back_populates="registrations")


# Lớp Post tương ứng với bảng "posts"
class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.event_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    images_url = Column(String(200), nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    event = relationship("Event", back_populates="posts")
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    reacts = relationship("React", back_populates="post", cascade="all, delete-orphan")


# Lớp Comment tương ứng với bảng "comments"
class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")


# Lớp React tương ứng với bảng "reacts"
class React(Base):
    __tablename__ = "reacts"
    __table_args__ = (UniqueConstraint('post_id', 'user_id', name='_post_user_uc'),)

    like_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    category = Column(String(100), default='like')
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    post = relationship("Post", back_populates="reacts")
    user = relationship("User", back_populates="reacts")


# Lớp Notification tương ứng với bảng "notifications"
class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.event_id"), nullable=True)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="notifications")
    event = relationship("Event", back_populates="notifications")