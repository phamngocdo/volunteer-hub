import os
import uvicorn
from pathlib import Path
from dotenv import load_dotenv

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config.db_config import engine, Base

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from src.routers.auth_route import auth_router
from src.routers.events_route import events_router
from src.routers.users_route import users_router
from src.routers.web_route import web_router


# SRC_DIR = Path(__file__).resolve().parent
SRC_DIR = "./src"
templates = Jinja2Templates(directory=os.path.join(SRC_DIR, "templates"))

backend_port = int(os.getenv("BACKEND_PORT", 8000))
frontend_port = int(os.getenv("FRONTEND_PORT", 3000))

app = FastAPI()

app.mount("/static", StaticFiles(directory=os.path.join(SRC_DIR, "static")), name="static")


app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY"),
    session_cookie="sessionid",
    max_age=86400 * 30,
    same_site="lax", 
    https_only=True,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        f"http://localhost:{backend_port}",
        f"http://127.0.0.1:{frontend_port}"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(events_router, prefix="/api/events", tags=["Event"])
app.include_router(users_router, prefix="/api/users", tags=["User"])
app.include_router(web_router, prefix="", tags=["Web"])

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "code": 404, "message": "Không tìm thấy trang"},
        status_code=404
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "code": 500, "message": "Lỗi máy chủ nội bộ"},
        status_code=500
    )

def start():
    uvicorn.run(
        "app:app",
        host="localhost",
        port=backend_port,
        reload=True,
        reload_dirs=[str(SRC_DIR)]
    )

if __name__ == "__main__":
    start()
