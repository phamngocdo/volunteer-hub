from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.config.db_config import Base


class EventRegistration(Base):
    __tablename__ = "event_registrations"

    registration_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("events.event_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    status = Column(String(20))  # pending | approved | rejected | cancelled | completed
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint("event_id", "user_id", name="unique_event_user"),)

    # Relationships
    event = relationship("Event", back_populates="registrations")
    user = relationship("User", back_populates="registrations")
