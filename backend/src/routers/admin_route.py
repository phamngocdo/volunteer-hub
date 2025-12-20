import traceback
import json
import io
import csv
from fastapi.responses import JSONResponse, StreamingResponse
from enum import Enum
from fastapi import APIRouter, Depends, status, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from typing import Optional

from src.utils.send_webpush import send_webpush
from src.config.db_config import get_db
from src.schemas.admin_schemas import *
from src.services.events_service import EventService
from src.services.users_service import UserService
from src.services.notifications_service import NotificationService
from src.utils.dependencies import get_current_user, role_required, active_status_required

class ExportFormat(str, Enum):
    json = "json"
    csv = "csv"


admin_router = APIRouter(
    dependencies=[
        Depends(active_status_required()),
        Depends(role_required(("admin")))
    ]
)


@admin_router.get("/users")
async def get_all_users(
    request: Request,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách người dùng.
    
    API dành cho Admin để xem danh sách tất cả người dùng trong hệ thống.
    """
    try:
        return await UserService.get_all_users(db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    

@admin_router.get("/events")
async def get_all_events(
    request: Request,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách sự kiện (Admin).
    
    API dành cho Admin để xem danh sách tất cả sự kiện, bao gồm các sự kiện chưa được duyệt.
    """
    try:
        return await EventService.get_all_events(db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    

@admin_router.patch("/users/{user_id}")
async def update_user_status(
    user_id: int, 
    status_update: UserStatusUpdate, 
    db: Session = Depends(get_db)
):
    """
    Cập nhật trạng thái người dùng (Ban/Unban).
    
    Cho phép Admin khóa (banned) hoặc mở khóa (active) tài khoản người dùng.
    """
    try:
        result = await UserService.update_user_status(db, user_id, status_update.status)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
        
        title = "Cập nhật trạng thái tài khoản"
        message = "Bạn đã bị khóa tài khoản." if status_update.status == UserStatus.BANNED else "Tài khoản của bạn đã được mở khóa."
        subs = await NotificationService.send_notification(
            db=db,
            event_id=None,
            user_id=user_id,
            title=title,
            message=message
        )

        if subs:
            send_webpush(title, message, subs)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@admin_router.patch("/events/{event_id}",
              response_model=EventAdminView)
async def update_event_status(
    event_id: int,
    status_update: EventStatusUpdate,
    db: Session = Depends(get_db)
): 
    """
    Duyệt sự kiện.
    
    Cho phép Admin duyệt (approve) hoặc từ chối (reject) một sự kiện đã được tạo bởi Manager.
    """
    try:
        event_to_update = await EventService.get_event_by_id(db, event_id)
        if not event_to_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with id {event_id} not found")
        updated_event = await EventService.update_event_status(db, event_id, status_update.status)

        title = "Cập nhật trạng thái sự kiện"
        message = f"Sự kiện {event_to_update.title} được duyệt thành công" if status_update.status == EventStatusAdminUpdate.APPROVED else f"Sự kiện {event_to_update.title} bị từ chối duyệt."
        subs = await NotificationService.send_notification(
            db=db,
            event_id=event_id,
            user_id=event_to_update.manager_id,
            title=title,
            message=message
        )

        if subs:
            send_webpush(title, message, subs)

        return updated_event
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    

@admin_router.delete("/events/{event_id}")
async def delete_event_by_admin(
    event_id: int, 
    db: Session = Depends(get_db)
):
    """
    Xóa sự kiện (Admin).
    
    Cho phép Admin xóa vĩnh viễn bất kỳ sự kiện nào khỏi hệ thống.
    """
    try:
        result = await EventService.delete_event(db, event_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with id {event_id} not found")
        return {"detail": "Event deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    

@admin_router.get("/export/users")
async def export_users_data(
    format: ExportFormat = Query(..., description="Định dạng file cần xuất: 'csv' hoặc 'json'"),
    db: Session = Depends(get_db)
):
    """
    Xuất dữ liệu người dùng.
    
    Xuất danh sách người dùng ra file CSV hoặc JSON.
    """
    users = await UserService.get_all_users(db)
    
    try:
        users_export = [UserExport.model_validate(user) for user in users]
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error parsing user data: {e}")

    if format == ExportFormat.json:
        users_data = [user.model_dump() for user in users_export]
        safe_data = json.loads(json.dumps(users_data, default=str))
        return JSONResponse(content=safe_data)

    if format == ExportFormat.csv:
        output = io.StringIO()
        writer = csv.writer(output)
        
        headers = list(UserExport.model_fields.keys())
        writer.writerow(headers)
        
        for user in users_export:
            writer.writerow([getattr(user, h) for h in headers])
            
        output.seek(0)
        return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=users.csv"})
    

@admin_router.get("/export/events", summary="Xuất dữ liệu sự kiện")
async def export_events_data(
    format: ExportFormat = Query(..., description="Định dạng file cần xuất: 'csv' hoặc 'json'"),
    db: Session = Depends(get_db)
):
    """
    Xuất dữ liệu sự kiện.
    
    Xuất danh sách sự kiện ra file CSV hoặc JSON.
    """
    events_db = await EventService.get_public_events(db)

    try:
        events_export = [EventExport.model_validate(event) for event in events_db]
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error parsing event data: {e}")

    if format == ExportFormat.json:

        events_data = [event.model_dump() for event in events_export]
        safe_data = json.loads(json.dumps(events_data, default=str))
        return JSONResponse(content=safe_data)

    if format == ExportFormat.csv:
        output = io.StringIO()
        writer = csv.writer(output)
        
        headers = list(EventExport.model_fields.keys())
        writer.writerow(headers)
        
        for event in events_export:
            writer.writerow([getattr(event, h) for h in headers])
            
        output.seek(0)
        return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=events.csv"})