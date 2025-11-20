from sqlalchemy import Column, Integer, String, Text, Date, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.config.db_config import Base


class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    manager_id = Column(Integer, ForeignKey("users.user_id"))
    title = Column(String(200))
    image_url = Column(String(200))
    description = Column(Text)
    category = Column(String(100))
    location = Column(String(200))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(20))  # pending | approved | rejected | completed
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    manager = relationship("User", back_populates="managed_events")
    registrations = relationship("EventRegistration", back_populates="event")
    posts = relationship("Post", back_populates="event")
    notifications = relationship("Notification", back_populates="event")

    @property
    def volunteer_number(self):
        """
        Tự động đếm số lượng trong danh sách 'registrations' 
        để trả về giá trị cho trường volunteer_number trong Pydantic schema.
        """
        if self.registrations:
            return len(self.registrations)
        return 0