import os
import uvicorn
from pathlib import Path
from dotenv import load_dotenv

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.auth_route import auth_router
from src.routers.users_route import users_router
from src.routers.events_route import events_router
from src.routers.posts_route import posts_router
from src.routers.comments_route import comments_router
from src.routers.reacts_route import reacts_router
from src.routers.notifications_route import notifications_router

SRC_DIR = Path(__file__).resolve().parent

load_dotenv()

backend_port = int(os.getenv("BACKEND_PORT", 8000))
frontend_port = int(os.getenv("FRONTEND_PORT", 3000))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        f"http://127.0.0.1:{frontend_port}"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/api/users", tags=["User"])
app.include_router(events_router, prefix="/api/events", tags=["Event"])
app.include_router(posts_router, prefix="/api/posts", tags=["Post"])
app.include_router(comments_router, prefix="/api/comments", tags=["Comment"])
app.include_router(reacts_router, prefix="/api/reacts", tags=["React"])
app.include_router(notifications_router, prefix="/api/notifications", tags=["Notification"])

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
