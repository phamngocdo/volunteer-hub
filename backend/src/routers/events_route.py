from dotenv import load_dotenv
from pathlib import Path
from fastapi import APIRouter, Request, Depends, HTTPException, status, File, UploadFile
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from src.config.db_config import get_db
from src.services.events_service import *
from src.services.notifications_service import NotificationService
from src.schemas.events_schemas import *
from src.utils.dependencies import active_status_required, role_required, get_current_user
from src.utils.file_uploads import save_image
from src.utils.send_webpush import send_webpush


SRC_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

events_router = APIRouter()

@events_router.get("/", response_model=List[EventSimple])
async def get_all_events(
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách tất cả sự kiện (Công khai).
    
    Cho phép lọc theo danh mục, ngày bắt đầu và trạng thái. 
    API này dành cho tất cả người dùng (kể cả khách).
    """
    events = await EventService.get_public_events(db, category=category, start_date=start_date, status=status)
    return events


@events_router.get("/joined", response_model=List[JoinedEventDetail])
async def get_joined_events(
    request: Request,
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
    _2 = Depends(role_required(("manager", "volunteer"))),
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách sự kiện đã tham gia.
    
    Trả về danh sách các sự kiện mà người dùng hiện tại (volunteer/manager) đã đăng ký tham gia.
    """
    try:
        user_id = user.get("sub")
        role = user.get("role")
        return EventService.get_joined_events(db, user_id, role)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    

@events_router.get("/manager", response_model=List[EventSimple])
async def get_my_created_events(
    request: Request,
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
    _2 = Depends(role_required(("manager",))),
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách sự kiện do tôi tạo (Manager).
    
    Chỉ dành cho Manager. Trả về các sự kiện mà Manager hiện tại đã tạo.
    """
    try:
        events = await EventService.get_events_by_manager(db, manager_id=user.get("sub"))
        return events
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@events_router.get("/{event_id}", response_model=EventDetail)
async def get_event_details(
    event_id: int,
    db: Session = Depends(get_db)
):
    """
    Xem chi tiết sự kiện.
    
    Trả về thông tin chi tiết của một sự kiện dựa trên ID.
    """
    try:
        event = await EventService.get_event_by_id(db, event_id=event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    

@events_router.post("/",response_model=EventDetail)
async def create_event(
    request: Request,
    event: EventCreate,
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
    _2 = Depends(role_required(("manager"))),
    db: Session = Depends(get_db),
):
    """
    Tạo sự kiện mới (Manager).
    
    Chỉ dành cho Manager. Tạo một sự kiện mới với các thông tin được cung cấp.
    """
    try:
        new_event = await EventService.create_event(db, event=event, manager_id=user.get("sub"))
        return new_event
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@events_router.put("/{event_id}", response_model=EventDetail)
async def update_event(
    request: Request,
    event_id: int,
    event_update: EventUpdate,
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
    _2 = Depends(role_required(("manager"))),
    db: Session = Depends(get_db),
):
    """
    Cập nhật sự kiện (Manager).
    
    Chỉ dành cho Manager. Cập nhật thông tin của một sự kiện đã tồn tại.
    Nếu trạng thái chuyển sang 'completed', hệ thống sẽ tự động hoàn thành các đăng ký tham gia.
    """
    try:
        event_to_update = await EventService.get_event_by_id(db, event_id=event_id)
        if not event_to_update:
            raise HTTPException(status_code=404, detail="Event not found")
        
        if event_to_update.status == "completed":
            await RegistrationService.complete_registrations_for_event(db, event_id=event_id)

        return await EventService.update_event(db, event_id=event_id, event_update=event_update)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@events_router.delete("/{event_id}")
async def delete_event(
    request: Request,
    event_id: int,
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
    _2 = Depends(role_required(("manager"))),
    db: Session = Depends(get_db),
):
    """
    Xóa sự kiện (Manager).
    
    Chỉ dành cho Manager. Xóa một sự kiện khỏi hệ thống.
    """
    try:
        event_to_delete = await EventService.get_event_by_id(db, event_id=event_id)
        if not event_to_delete:
            raise HTTPException(status_code=404, detail="Event not found")
        
        await EventService.delete_event(db, event_id=event_id)
        return {"detail": "Event deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@events_router.post("/{event_id}/register", response_model=dict)
async def register_for_event(
    request: Request,
    event_id: int,
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
    _2 = Depends(role_required(("volunteer"))),
    db: Session = Depends(get_db),
):
    """
    Đăng ký tham gia sự kiện (Volunteer).
    
    Chỉ dành cho tình nguyện viên. Đăng ký tham gia vào một sự kiện cụ thể.
    """
    try:
        user_id = user.get("sub")
        event = await EventService.get_event_by_id(db, event_id=event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        await RegistrationService.create_registration(db, event_id=event_id, user_id=user_id)
        return {"detail": "Register successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@events_router.get("/{event_id}/registration-status", response_model=dict)
async def check_registration_status(
    request: Request,
    event_id: int,
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
    _2 = Depends(role_required(("volunteer"))),
    db: Session = Depends(get_db),
):
    """
    Kiểm tra trạng thái đăng ký (Volunteer).
    
    Kiểm tra xem tình nguyện viên hiện tại đã đăng ký sự kiện này chưa và trạng thái ra sao.
    """
    try:
        user_id = user.get("sub")
        event = await EventService.get_event_by_id(db, event_id=event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        status = await RegistrationService.get_registration_status(db, event_id, user_id)
        return {"event_id": event_id, "registration_status": status}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@events_router.delete("/{event_id}/registration", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_event_registration(
    request: Request,
    event_id: int,
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
    _2 = Depends(role_required(("volunteer"))),
    db: Session = Depends(get_db),
):
    """
    Hủy đăng ký tham gia (Volunteer).
    
    Cho phép tình nguyện viên hủy đăng ký khỏi một sự kiện.
    """
    try:
        user_id = user.get("sub")
        event = await EventService.get_event_by_id(db, event_id=event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        success = await RegistrationService.cancel_registration(db, event_id=event_id, user_id=user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Registration not found")
        
        return {"detail": "Registration cancelled successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@events_router.get("/{event_id}/registrations", response_model=List[RegistrationDetail])
async def get_event_registrations(
    request: Request,
    event_id: int,
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
    _2 = Depends(role_required(("manager"))),
    db: Session = Depends(get_db),
):
    """
    Lấy danh sách đơn đăng ký (Manager).
    
    Xem danh sách tất cả các đơn đăng ký tham gia cho một sự kiện cụ thể.
    """
    try:
        event = await EventService.get_event_by_id(db, event_id=event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        return await RegistrationService.get_registrations_for_event(db, event_id=event_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@events_router.patch("/registrations/{registration_id}", response_model=RegistrationDetail)
async def update_registration_status(
    request: Request,
    registration_id: int,
    status_update: RegistrationStatusUpdate,
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
    _2 = Depends(role_required(("manager"))),
    db: Session = Depends(get_db),
):
    """
    Duyệt/Từ chối đơn đăng ký (Manager).
    
    Cập nhật trạng thái của đơn đăng ký (ví dụ: approved, rejected).
    Sẽ gửi thông báo đến người dùng sau khi cập nhật thành công.
    """
    try:
        registration = await RegistrationService.get_registration_by_id(db, registration_id)
        if not registration:
            raise HTTPException(status_code=404, detail="Registation not found")
        
        updated_reg = await RegistrationService.update_status(db, registration_id=registration_id, status=status_update.status)
        
        if updated_reg and updated_reg.event:
            event_title = updated_reg.event.title
            user_id = updated_reg.user_id
            new_status = status_update.status
            
            message = ""
            if new_status == "approved":
                message = f"Đơn đăng ký tham gia sự kiện '{event_title}' của bạn đã được duyệt."
            elif new_status == "rejected":
                message = f"Đơn đăng ký tham gia sự kiện '{event_title}' của bạn đã bị từ chối."
            
            if message:
                subs = await NotificationService.send_notification(
                    db=db, 
                    user_id=user_id, 
                    event_id=updated_reg.event_id, 
                    title="Thông báo sự kiện",
                    message=message
                )
                if subs:
                    send_webpush(title="Thông báo sự kiện", message=message, subscriptions=subs)

        return updated_reg
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@events_router.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user),
    _1 = Depends(active_status_required()),
):
    """
    Tải ảnh sự kiện lên Public.
    
    Nhận file ảnh, upload lên thư mục Public và trả về URL của ảnh.
    """
    try:
        return save_image(file, "events")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

