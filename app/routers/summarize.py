"""AI summary of a note. WIP — not wired into the dashboard yet."""
import os

from anthropic import Anthropic
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
    client = Anthropic(api_key=api_key)
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=200,
        messages=[{"role": "user", "content": f"Summarize in one sentence:\n\n{payload.text}"}],
    )
    return {"summary": "".join(b.text for b in msg.content if hasattr(b, "text"))}
