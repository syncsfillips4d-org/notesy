import os

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "templates"))

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8001/v1")
BACKEND_KEY = os.environ.get("BACKEND_KEY", "dev-key")


def _ctx() -> dict[str, str]:
    return {"backend_url": BACKEND_URL, "backend_key": BACKEND_KEY}


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html", _ctx())


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(request, "login.html", _ctx())


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(request, "dashboard.html", _ctx())


@router.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    return "User-agent: *\nDisallow: /admin\n"
