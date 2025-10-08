import os
import uvicorn
from pathlib import Path
from dotenv import load_dotenv

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config.db_config import engine, Base
from src.models import *

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.sessions import SessionMiddleware


# from src.routers.example_route import reviews_router
# from src.routers.auth_route import auth_router


# SRC_DIR = Path(__file__).resolve().parent

backend_port = int(os.getenv("BACKEND_PORT", 8000))
frontend_port = int(os.getenv("FRONTEND_PORT", 3000))

app = FastAPI()

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

app.include_router(reviews_router, prefix="/api/reviews", tags=["Reviews"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

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
