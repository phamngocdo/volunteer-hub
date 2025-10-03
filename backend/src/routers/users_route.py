from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from jwt import InvalidTokenError, ExpiredSignatureError
from sqlalchemy.orm import Session
from services.users_service import UserService
from schemas.user_schemas import UserUpdate

from config.db_config import get_db

users_router = APIRouter()

@users_router.get("/me")
async def get_current_user(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.session.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        user = await UserService.get_current_user(token=token, db=db)

        return user
    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    


@users_router.put("/me")
async def update_password(data: UserUpdate, request: Request, db: Session = Depends(get_db)):
    try:
        token = request.session.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user_data = {
            "password": data.password
        }
        await UserService.update_current_user(token=token, user_data=user_data, db=db)
        return JSONResponse(status_code=200, content={"message": "Update password successfull"})
    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")