# Import Base từ file cấu hình CSDL của bạn
from src.config.db_config import Base

# Import tất cả các class Model của bạn
from .user_model import User
from .event_model import Event
from .registration_model import EventRegistration
from .post_model import Post  # <-- Dòng import này sẽ giúp SQLAlchemy tìm thấy class Post
from .comment_model import Comment
from .react_model import React
from .notification_model import Notification