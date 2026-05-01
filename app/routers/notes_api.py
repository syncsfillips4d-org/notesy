"""Notes CRUD."""
import os
from itertools import count

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from app.routers.auth import current_user

router = APIRouter(prefix="/api")

DEMO_USER_EMAIL = os.environ.get("DEMO_USER_EMAIL", "demo@example.com")


class NoteIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(default="", max_length=10_000)


class Note(NoteIn):
    id: int
    author: str


_id_seq = count(start=4)
_notes: list[Note] = [
    Note(id=1, title="welcome", body="first note. press n for new.", author=DEMO_USER_EMAIL),
    Note(id=2, title="groceries", body="milk, eggs, bread", author=DEMO_USER_EMAIL),
    Note(id=3, title="todo", body=f"ping {DEMO_USER_EMAIL} for beta access", author=DEMO_USER_EMAIL),
]


@router.get("/notes")
async def list_notes() -> list[Note]:
    return _notes


@router.get("/notes/{note_id}")
async def get_note(note_id: int) -> Note:
    for n in _notes:
        if n.id == note_id:
            return n
    raise HTTPException(404)


@router.post("/notes", status_code=201)
async def create_note(payload: NoteIn, request: Request) -> Note:
    user = current_user(request) or "anon"
    n = Note(id=next(_id_seq), title=payload.title, body=payload.body, author=user)
    _notes.append(n)
    return n


@router.delete("/notes/{note_id}", status_code=204)
async def delete_note(note_id: int) -> None:
    for i, n in enumerate(_notes):
        if n.id == note_id:
            _notes.pop(i)
            return
    raise HTTPException(404)
