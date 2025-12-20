import traceback
from sqlalchemy.orm import Session
from sqlalchemy import select, update, func
from sqlalchemy.future import select
from datetime import date
from typing import Optional, List
from src.models.registration_model import EventRegistration
from src.models.event_model import Event
from src.schemas.events_schemas import *

class EventService:
    @staticmethod
    async def get_event_by_id(db: Session, event_id: int) -> Optional[Event]:
        try:
            query = select(Event).where(Event.event_id == event_id)
            result = db.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            traceback.print_exc()
            raise e
 

    @staticmethod
    async def get_all_events(db: Session) -> List[Event]:
        try:
            query = select(Event)
            result = db.execute(query)
            return result.scalars().all()
        except Exception as e:
            traceback.print_exc()
            raise e
    
    
    @staticmethod
    async def get_events_by_manager(db: Session, manager_id: int) -> List[dict]:
        try:
            query = select(Event).where(Event.manager_id == manager_id).order_by(Event.start_date.desc())
            
            result = db.execute(query)
            events = result.scalars().all()

            events_with_volunteer_number = []
            for e in events:
                e_dict = e.__dict__.copy() 
                e_dict["volunteer_number"] = len(e.registrations) if e.registrations else 0
                events_with_volunteer_number.append(e_dict)

            return events_with_volunteer_number

        except Exception as e:
            traceback.print_exc()
            raise
 
    @staticmethod
    def get_joined_events(db: Session, current_user_id: int, role: str):
        try:
            if role == "volunteer":
                joined_event_ids = (
                    db.query(EventRegistration.event_id)
                    .filter(
                        EventRegistration.user_id == current_user_id,
                        EventRegistration.status.in_(["approved", "completed"])
                    )
                    .subquery()
                )

                events = (
                    db.query(
                        Event.event_id,
                        Event.title,
                        Event.image_url,
                        func.count(
                            func.nullif(EventRegistration.status.notin_(["approved", "completed"]), True)
                        ).label("member_count")
                    )
                    .join(EventRegistration, Event.event_id == EventRegistration.event_id)
                    .filter(Event.event_id.in_(joined_event_ids))
                    .group_by(Event.event_id, Event.title, Event.image_url)
                    .order_by(Event.title.asc())
                    .all()
                )

            elif role == "manager":
                events = (
                    db.query(
                        Event.event_id,
                        Event.title,
                        Event.image_url,
                        func.count(
                            func.nullif(EventRegistration.status.notin_(["approved", "completed"]), True)
                        ).label("member_count")
                    )
                    .outerjoin(EventRegistration, Event.event_id == EventRegistration.event_id)
                    .filter(
                        Event.manager_id == current_user_id,
                        Event.status.in_(["approved", "completed"])
                    )
                    .group_by(Event.event_id, Event.title, Event.image_url)
                    .order_by(Event.title.asc())
                    .all()
                )

            return [
                {
                    "event_id": e.event_id,
                    "title": e.title,
                    "image_url": e.image_url,
                    "member_count": e.member_count,
                }
                for e in events
            ]

        except Exception as e:
            traceback.print_exc()
            raise e

        
    @staticmethod
    async def get_public_events(
        db: Session,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        status: Optional[str] = None
    ) -> List[dict]:

        try:
            today = date.today()

            db.execute(
                update(Event)
                .where(Event.end_date < today)
                .where(Event.status != "completed")
                .values(status="completed")
            )
            db.commit()

            query = select(Event)

            allowed_status = ["approved", "completed"]
            if status:
                if status.lower() not in allowed_status:
                    query = query.where(Event.status.in_(allowed_status))
                else:
                    query = query.where(Event.status == status.lower())
            else:
                query = query.where(Event.status.in_(allowed_status))

            if category:
                query = query.where(Event.category == category.strip())

            if start_date:
                query = query.where(Event.start_date == start_date)

            query = query.order_by(Event.start_date.asc())

            result = db.execute(query)
            events = result.scalars().all()

            events_with_volunteer_number = []
            for e in events:
                e_dict = e.__dict__.copy() 
                e_dict["volunteer_number"] = len(e.registrations)
                events_with_volunteer_number.append(e_dict)

            return events_with_volunteer_number

        except Exception as e:
            traceback.print_exc()
            raise e
    

    @staticmethod
    async def create_event(db: Session, event: EventCreate, manager_id: int) -> Event:
        try:
            db_event = Event(
                **event.dict(),
                manager_id=manager_id,
                status="pending"
            )
            db.add(db_event)
            db.commit()
            db.refresh(db_event)
            return db_event
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise e
    
    @staticmethod
    async def update_event(db: Session, event_id: int, event_update: EventUpdate) -> Optional[Event]:
        try:
            db_event = await EventService.get_event_by_id(db, event_id)
            if not db_event:
                return None

            update_data = event_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_event, key, value)
            
            db.commit()
            db.refresh(db_event)
            return db_event
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise e
        
        
    @staticmethod
    async def update_event_status(db: Session, event_id: int, status: str) -> Optional[Event]:
        try:
            db_event = await EventService.get_event_by_id(db, event_id)
            if not db_event:
                return None
            
            db_event.status = status
            db.commit()
            db.refresh(db_event)
            return db_event
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise e

    
    @staticmethod
    async def delete_event(db: Session, event_id: int) -> bool:
        try:
            db_event = await EventService.get_event_by_id(db, event_id)
            if not db_event:
                return False
            
            db.delete(db_event)
            db.commit()
            return True
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise e

class RegistrationService:
    @staticmethod
    async def get_registration_status(db: Session, event_id: int, volunteer_id: int) -> str:
        try:
            event = db.query(Event).filter(Event.event_id == event_id).first()

            if not event:
                return "event_ended" 

            if event.status == "completed":
                return "event_ended"

            registration = (
                db.query(EventRegistration)
                .join(Event, Event.event_id == EventRegistration.event_id)
                .filter(
                    EventRegistration.event_id == event_id,
                    EventRegistration.user_id == volunteer_id
                )
                .first()
            )

            if not registration:
                return "not_registered"

            return registration.status

        except Exception as e:
            traceback.print_exc()
            raise e
        

    @staticmethod
    async def get_registration_by_id(db: Session, registration_id: int) -> Optional[EventRegistration]:
        try:
            query = select(EventRegistration).where(EventRegistration.registration_id == registration_id)
            result = db.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            traceback.print_exc()
            raise e
    

    @staticmethod
    async def get_registrations_for_event(db: Session, event_id: int) -> List[EventRegistration]:
        try:
            query = select(EventRegistration).where(EventRegistration.event_id == event_id)
            result = db.execute(query)
            return result.scalars().all()
        except Exception as e:
            traceback.print_exc()
            raise e
    

    @staticmethod
    async def create_registration(db: Session, event_id: int, user_id: int) -> Optional[EventRegistration]:
        try:
            event = await EventService.get_event_by_id(db, event_id)
            if not event or event.status != 'approved':
                return None 
            
            query = select(EventRegistration).where(
                EventRegistration.event_id == event_id,
                EventRegistration.user_id == user_id
            )
            result = db.execute(query)
            if result.scalar_one_or_none():
                return None  

            db_reg = EventRegistration(
                event_id=event_id,
                user_id=user_id,
                status="pending"
            )
            db.add(db_reg)
            db.commit()
            db.refresh(db_reg)
            return db_reg
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise e
        
    
    @staticmethod
    async def cancel_registration(db: Session, event_id: int, user_id: int) -> bool:
        try:
            query = select(EventRegistration).where(
                EventRegistration.event_id == event_id,
                EventRegistration.user_id == user_id
            )
            result = db.execute(query)
            db_reg = result.scalar_one_or_none()

            if not db_reg:
                return False 

            db.delete(db_reg)
            db.commit()
            return True
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise e
        
    
    @staticmethod
    async def update_status(db: Session, registration_id: int, status: str) -> Optional[EventRegistration]:
        try:
            db_reg = await RegistrationService.get_registration_by_id(db, registration_id)
            if not db_reg:
                return None
            
            db_reg.status = status
            db.commit()
            db.refresh(db_reg)
            return db_reg
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise e
        

    @staticmethod
    async def complete_registrations_for_event(db: Session, event_id: int) -> None:
        try:
            query = select(EventRegistration).where(EventRegistration.event_id == event_id)
            result = db.execute(query)
            registrations = result.scalars().all()

            for reg in registrations:
                reg.status = "completed"

            db.commit()
            return None
        except Exception as e:
            traceback.print_exc()
            db.rollback()
            raise e