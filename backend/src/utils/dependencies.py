from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, InvalidTokenError

from src.utils.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
def active_status_required():
    async def wrapper(current_user: dict = Depends(get_current_user)):
        user_status = current_user.get("status")
        if user_status == "banned":
            raise HTTPException(
                status_code=403,
                detail="Your account was banned",
            )
        return current_user
    return wrapper

def role_required(role: tuple):
    async def wrapper(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        if user_role not in role:
            raise HTTPException(
                status_code=403,
                detail=f"You do not have permission.",
            )
        return current_user
    return wrapper
