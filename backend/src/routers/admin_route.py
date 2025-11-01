import traceback
import json
import io
import csv
from fastapi.responses import JSONResponse, StreamingResponse
from enum import Enum
from fastapi import APIRouter, Depends, status, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from typing import List, Optional

# Import các thành phần cần thiết
from src.config.db_config import get_db
from src.schemas import admin_schemas
from src.services.events_service import EventService
from src.models import User, Event
from src.config.redis_config import redis_client as r

# --- Enum cho định dạng Export ---
class ExportFormat(str, Enum):
    json = "json"
    csv = "csv"

# --- Dependency để xác thực quyền Admin ---

async def get_current_admin_user(request: Request, db: Session = Depends(get_db)) -> User:
    """
    Dependency để lấy token, xác thực người dùng qua Redis session và kiểm tra vai trò 'admin'.
    Inject đối tượng User vào các endpoint nếu hợp lệ.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    token = auth_header.split(" ")[1]

    session_json = await r.get(token)
    if not session_json:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or invalid")

    try:
        session_json = json.loads(session_json)
        if session_json['role'] != 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Not authorized. Admin role required."
            )
        
        user = db.query(User).filter(User.user_id == session_json['user_id']).first()
        if not user:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin user not found in database.")
        return user
        
    except HTTPException as e:
        raise e
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

# --- Khởi tạo Router với Dependency xác thực chung ---

admin_router = APIRouter(
    # DÒNG QUAN TRỌNG: Áp dụng dependency này cho TẤT CẢ các endpoint bên dưới2
    dependencies=[Depends(get_current_admin_user)]
)

# --- User Management Endpoints ---

@admin_router.get("/users",
                  response_model=List[admin_schemas.UserAdminView],
                  summary="Lấy danh sách tất cả người dùng (có thể lọc theo status)")
async def get_all_users(
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None, description="Lọc theo trạng thái (ví dụ: 'active', 'banned')")
):
    """
    API để admin lấy danh sách tất cả người dùng.
    Có thể lọc theo trạng thái (status) qua query parameter.
    (Không cần `Depends` ở đây nữa vì đã được áp dụng chung)
    """
    try:
        # Bắt đầu câu query cơ bản
        query = select(User)
        
        # Thêm điều kiện lọc 'where' nếu 'status' được cung cấp
        if status:
            query = query.where(User.status == status)
            
        # Luôn sắp xếp theo ngày tạo mới nhất
        query = query.order_by(User.created_at.desc())
        
        result = db.execute(query)
        return result.scalars().all()
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not fetch users")

@admin_router.patch("/users/{user_id}", 
              response_model=admin_schemas.UserAdminView,
              summary="Cập nhật trạng thái người dùng (Khóa/Mở khóa)")
async def update_user_status(
    user_id: int, 
    status_update: admin_schemas.UserStatusUpdate, 
    db: Session = Depends(get_db)
):
    """
    API để admin thay đổi trạng thái của một người dùng ('active' hoặc 'banned').
    """
    user_to_update = db.query(User).filter(User.user_id == user_id).first()
    if not user_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    
    try:
        user_to_update.status = status_update.status.value
        db.commit()
        db.refresh(user_to_update)
        return user_to_update
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not update user status")

# --- Event Management Endpoints ---

@admin_router.get("/events", 
            response_model=List[admin_schemas.EventAdminView],
            summary="Lấy danh sách tất cả sự kiện")
async def get_all_events(
    status_filter: Optional[str] = Query(None, alias="status", description="Lọc sự kiện theo trạng thái"),
    db: Session = Depends(get_db)
):
    """
    API để admin lấy danh sách tất cả sự kiện, có thể lọc theo trạng thái.
    """
    try:
        query = select(Event).order_by(Event.created_at.desc())
        if status_filter:
            query = query.where(Event.status == status_filter)
        result = db.execute(query)
        return result.scalars().all()
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not fetch events")

@admin_router.patch("/events/{event_id}",
              response_model=admin_schemas.EventAdminView,
              summary="Duyệt hoặc từ chối sự kiện")
async def update_event_status(
    event_id: int,
    status_update: admin_schemas.EventStatusUpdate,
    db: Session = Depends(get_db)
):
    """
    API để admin duyệt hoặc từ chối một sự kiện ('approved' hoặc 'rejected').
    """
    event_to_update = await EventService.get_event_by_id(db, event_id)
    if not event_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with id {event_id} not found")
        
    try:
        event_to_update.status = status_update.status.value
        db.commit()
        db.refresh(event_to_update)
        return event_to_update
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not update event status")
    
@admin_router.delete("/events/{event_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Xóa một sự kiện (quyền admin)")
async def delete_event_by_admin(
    event_id: int, 
    db: Session = Depends(get_db)
):
    """
    API để admin xóa một sự kiện khỏi hệ thống bằng EventService.
    """
    success = await EventService.delete_event(db, event_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found or could not be deleted"
        )
    return

@admin_router.get("/export/users", summary="Xuất dữ liệu người dùng")
async def export_users_data(
    format: ExportFormat = Query(..., description="Định dạng file cần xuất: 'csv' hoặc 'json'"),
    db: Session = Depends(get_db)
):
    """
    API để admin xuất toàn bộ dữ liệu người dùng ra file CSV hoặc JSON.
    Đã sửa để xử lý datetime và chỉ xuất các trường trong schema UserExport.
    """
    # Sửa: Dùng select()
    users_db = db.execute(select(User)).scalars().all()
    
    # Sửa: Chuyển đổi sang Pydantic model
    try:
        users_export = [admin_schemas.UserExport.from_orm(user) for user in users_db]
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error parsing user data: {e}")

    if format == ExportFormat.json:
        # Sửa: Dùng .model_dump() (Pydantic v2) hoặc .dict() (Pydantic v1)
        # Pydantic đã tự động chuyển datetime thành string
        users_data = [user.model_dump() for user in users_export]
        safe_data = json.loads(json.dumps(users_data, default=str))
        return JSONResponse(content=safe_data)

    if format == ExportFormat.csv:
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Sửa: Lấy header từ Pydantic model để đảm bảo nhất quán
        headers = list(admin_schemas.UserExport.model_fields.keys()) # Pydantic v2
        # (Dùng list(UserExport.__fields__.keys()) cho Pydantic v1)
        writer.writerow(headers)
        
        # Sửa: Ghi dữ liệu từ Pydantic model
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
    API để admin xuất toàn bộ dữ liệu sự kiện ra file CSV hoặc JSON.
    Đã sửa để xử lý datetime và chỉ xuất các trường trong schema EventExport.
    """
    # Sửa: Dùng select()
    events_db = db.execute(select(Event)).scalars().all()

    # Sửa: Chuyển đổi sang Pydantic model
    try:
        events_export = [admin_schemas.EventExport.from_orm(event) for event in events_db]
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error parsing event data: {e}")

    if format == ExportFormat.json:
        # Sửa: Dùng .model_dump() (Pydantic v2) hoặc .dict() (Pydantic v1)
        # Bỏ qua cách làm json.dumps(json.loads()) không hiệu quả
        events_data = [event.model_dump() for event in events_export]
        safe_data = json.loads(json.dumps(events_data, default=str))
        return JSONResponse(content=safe_data)

    if format == ExportFormat.csv:
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Sửa: Lấy header từ Pydantic model
        headers = list(admin_schemas.EventExport.model_fields.keys()) # Pydantic v2
        # (Dùng list(EventExport.__fields__.keys()) cho Pydantic v1)
        writer.writerow(headers)
        
        # Sửa: Ghi dữ liệu từ Pydantic model
        for event in events_export:
            writer.writerow([getattr(event, h) for h in headers])
            
        output.seek(0)
        return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=events.csv"})