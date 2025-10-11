import os
import uvicorn
from pathlib import Path
from dotenv import load_dotenv

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from routers.auth_route import auth_router
from routers.users_route import users_router
from routers.events_route import events_router
from routers.web_route import web_router

SRC_DIR = Path(__file__).resolve().parent

backend_port = int(os.getenv("BACKEND_PORT", 8000))
frontend_port = int(os.getenv("FRONTEND_PORT", 3000))

app = FastAPI()

app.mount("/static", StaticFiles(directory=SRC_DIR / "static"), name="static")


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
app.include_router(users_router, prefix="/api/users", tags=["User"])
app.include_router(events_router, prefix="/api/events", tags=["Event"])
app.include_router(web_router, prefix="", tags=["Web"])


def start():
    uvicorn.run(
        "main:app",
        host="localhost",
        port=backend_port,
        reload=True,
        reload_dirs=[str(SRC_DIR)]
    )

if __name__ == "__main__":
    start()
