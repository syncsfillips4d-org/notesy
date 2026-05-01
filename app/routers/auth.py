"""Cookie-session login. Demo only — accepts any email/password."""
import os
from itsdangerous import URLSafeSerializer

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/api")

_SESSION_SECRET = os.environ.get("SESSION_SECRET", "change-me-in-prod")
_serializer = URLSafeSerializer(_SESSION_SECRET, salt="session")


def current_user(request: Request) -> str | None:
    cookie = request.cookies.get("session")
    if not cookie:
        return None
    try:
        return _serializer.loads(cookie).get("user")
    except Exception:
        return None


@router.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):  # noqa: ARG001 — demo
    token = _serializer.dumps({"user": email})
    resp = RedirectResponse("/dashboard", status_code=303)
    resp.set_cookie("session", token, httponly=True, samesite="lax", max_age=86400)
    return resp


@router.post("/logout")
async def logout():
    resp = RedirectResponse("/", status_code=303)
    resp.delete_cookie("session")
    return resp


@router.get("/me")
async def me(request: Request):
    return {"user": current_user(request)}
