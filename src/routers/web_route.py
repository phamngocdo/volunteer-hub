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

@web_router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if request.session.get("access_token"):
        try:
            token = request.session["access_token"]
            payload = decode_token(token)
            user_id = payload.get("sub")
            if user_id:
                return RedirectResponse(url="/", status_code=302)
        except Exception:
            pass
    return templates.TemplateResponse("login.html", {"request": request})

@web_router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    if request.session.get("access_token"):
        try:
            token = request.session["access_token"]
            payload = decode_token(token)
            user_id = payload.get("sub")
            if user_id:
                return RedirectResponse(url="/", status_code=302)
        except Exception:
            pass
    return templates.TemplateResponse("register.html", {"request": request})

@web_router.get("/complete-profile", response_class=HTMLResponse)
async def complete_profile_page(request: Request):
    if request.session.get("access_token"):
        try:
            token = request.session["access_token"]
            payload = decode_token(token)
            user_id = payload.get("sub")
            if user_id:
                return RedirectResponse(url="/", status_code=302)
        except Exception:
            pass

    if not request.session.get("google_user_info"):
        return RedirectResponse(url="/register", status_code=302)
    google_info = request.session["google_user_info"]
    return templates.TemplateResponse(
        "complete-profile.html",
        {
            "request": request,
            "prefill": google_info
        }
    )