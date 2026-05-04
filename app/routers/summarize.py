"""AI summary of a note. WIP — not wired into the dashboard yet."""
import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api")


class SummarizeIn(BaseModel):
    text: str


@router.post("/summarize")
async def summarize(payload: SummarizeIn) -> dict[str, str]:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(503, "ai not configured")
    raise HTTPException(503, "ai temporarily unavailable")
