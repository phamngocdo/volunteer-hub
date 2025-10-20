import os
from dotenv import load_dotenv

from pathlib import Path
from fastapi import APIRouter, Request, Depends, HTTPException,Form, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from authlib.jose import jwt
import requests
from src.services.users_service import UserService
from src.config.db_config import get_db
from src.services.events_service import *
from src.schemas.events_schemas import *
from src.utils.security import *
from src.config.redis_config import redis_client as r



SRC_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

events_router = APIRouter()

# --- PUBLIC ENDPOINTS ---

@events_router.get("/", response_model=List[EventSimple])
async def get_all_events(
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách tất cả sự kiện đã được duyệt (approved).
    """
    events = await EventService.get_public_events(db, category=category, start_date=start_date)
    return events


@events_router.get("/{event_id}", response_model=EventDetail)
async def get_event_details(event_id: int, db: Session = Depends(get_db)):
    """
    Lấy thông tin chi tiết của một sự kiện công khai.
    """
    event = await EventService.get_event_by_id(db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event

# --- MANAGER ENDPOINTS ---

@events_router.post("/", response_model=EventDetail, status_code=status.HTTP_201_CREATED)
async def create_event(
    request: Request,
    event: EventCreate,
    db: Session = Depends(get_db),
):
    """
    Tạo một sự kiện mới. Chỉ có 'manager' mới có quyền này.
    """

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth_header.split(" ")[1]

    session_json = await r.get(token)
    if not session_json:
        raise HTTPException(status_code=401, detail="Session expired or invalid")


    if session_json['role'] != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create events")

    new_event = await EventService.create_event(db, event=event, manager_id=session_json["user_id"])
    return new_event

@events_router.put("/{event_id}", response_model=EventDetail)
async def update_event(
    request: Request,
    event_id: int,
    event_update: EventUpdate,
    db: Session = Depends(get_db),
):
    """
    Cập nhật thông tin sự kiện. Chỉ manager tạo ra sự kiện mới có quyền.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth_header.split(" ")[1]

    session_json = await r.get(token)
    if not session_json:
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    if session_json["role"] != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create events")

    event_to_update = await EventService.get_event_by_id(db, event_id=event_id)
    if not event_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    if event_to_update.manager_id != session_json["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this event")
        
    return await EventService.update_event(db, event_id=event_id, event_update=event_update)


@events_router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    request: Request,
    event_id: int,
    db: Session = Depends(get_db),
):
    """Xóa một sự kiện. Chỉ manager tạo ra sự kiện mới có quyền."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth_header.split(" ")[1]

    session_json = await r.get(token)
    if not session_json:
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    if session_json["role"] != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create events")
    
    event_to_delete = await EventService.get_event_by_id(db, event_id=event_id)
    if not event_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    if event_to_delete.manager_id != session_json["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this event")
    
    await EventService.delete_event(db, event_id=event_id)
    return {"detail": "Event deleted successfully"}

# --- VOLUNTEER ENDPOINTS ---

@events_router.post("/{event_id}/register", response_model=RegistrationDetail, status_code=status.HTTP_201_CREATED)
async def register_for_event(
    request: Request,
    event_id: int,
    db: Session = Depends(get_db),
):
    """Tình nguyện viên đăng ký tham gia sự kiện."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth_header.split(" ")[1]

    session_json = await r.get(token)
    if not session_json:
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    if session_json["role"] != "volunteer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create events")

    user_id = session_json["user_id"]
    registration = await RegistrationService.create_registration(db, event_id=event_id, user_id=user_id)
    if not registration:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not register for this event. You may have already registered.")

    return registration

@events_router.delete("/{event_id}/cancel-registration", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_event_registration(
    request: Request,
    event_id: int,
    db: Session = Depends(get_db),
):
    """Tình nguyện viên hủy đăng ký sự kiện."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth_header.split(" ")[1]

    session_json = await r.get(token)
    if not session_json:
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    if session_json["role"] != "volunteer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create events")

    user_id = session_json["user_id"]

    success = await RegistrationService.cancel_registration(db, event_id=event_id, user_id=user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found")
    
    return {"detail": "Registration cancelled successfully"}

# --- REGISTRATION MANAGEMENT (for Manager) ---

@events_router.get("/{event_id}/registrations", response_model=List[RegistrationDetail])
async def get_event_registrations(
    request: Request,
    event_id: int,
    db: Session = Depends(get_db),
):
    """Manager xem danh sách tình nguyện viên đã đăng ký sự kiện của mình."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth_header.split(" ")[1]

    session_json = await r.get(token)
    if not session_json:
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    if session_json["role"] != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create events")

    current_user_id = session_json["user_id"]
    event = await EventService.get_event_by_id(db, event_id=event_id)
    if not event or event.manager_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view registrations for this event")
        
    return await RegistrationService.get_registrations_for_event(db, event_id=event_id)


@events_router.patch("/registrations/{registration_id}", response_model=RegistrationDetail)
async def update_registration_status(
    request: Request,
    registration_id: int,
    status_update: RegistrationStatusUpdate,
    db: Session = Depends(get_db),
):
    """Manager duyệt, từ chối, hoặc đánh dấu hoàn thành cho một đơn đăng ký."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth_header.split(" ")[1]

    session_json = await r.get(token)
    if not session_json:
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    if session_json["role"] != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create events")

    current_user_id = session_json["user_id"]
    event = await EventService.get_event_by_id(db, event_id=registration.event_id)
    if not event or event.manager_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to manage this registration")
    
    return await RegistrationService.update_status(db, registration_id=registration_id, status=status_update.status)
