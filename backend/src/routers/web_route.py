from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jwt import ExpiredSignatureError, InvalidTokenError
from utils.security import decode_token

web_router = APIRouter()

SRC_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=SRC_DIR / "templates")


@web_router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    token = request.session.get("access_token")
    user = request.session.get("user")
    
    try:
        decode_token(token)
    except (ExpiredSignatureError, InvalidTokenError, TypeError):
        request.session.pop("user", None)
        request.session.pop("access_token", None)
        user = None

    return templates.TemplateResponse("home.html", {"request": request, "user": user})

# Example when access route but did not login
# @web_router.get("/chat")
# async def chat_page(request: Request):
#     user = request.session.get("user")
#     token = request.session.get("access_token")

#     try:
#         decode_token(token)
#     except (ExpiredSignatureError, InvalidTokenError, TypeError):
#         request.session.pop("user", None)
#         request.session.pop("access_token", None)
#         return RedirectResponse(url="/auth/login", status_code=302)

#     return templates.TemplateResponse("chat.html", {"request": request, "user": user})
