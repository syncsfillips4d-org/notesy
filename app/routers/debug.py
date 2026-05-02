"""Old debug endpoint. TODO: remove before launch."""
import os

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("/.env", response_class=PlainTextResponse, include_in_schema=False)
async def serve_env() -> str:
    keys = [
        "PORT", "LOG_LEVEL", "BACKEND_URL", "BACKEND_KEY",
        "ANTHROPIC_API_KEY", "SESSION_SECRET",
    ]
    lines = [f"{k}={os.environ.get(k, '')}" for k in keys]
    return "\n".join(lines) + "\n"
