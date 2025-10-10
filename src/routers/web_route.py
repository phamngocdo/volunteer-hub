from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from utils.security import decode_token

web_router = APIRouter()

SRC_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=SRC_DIR / "templates")

@web_router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

