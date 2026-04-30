import os
import time

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.log import log_request
from app.routers import auth, debug, graphql_router, notes_api, pages, summarize

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

app = FastAPI(
    title="notesy",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)


@app.middleware("http")
async def access_log(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    ms = (time.perf_counter() - started) * 1000
    fwd = (
        request.headers.get("fly-client-ip")
        or request.headers.get("x-forwarded-for", "").split(",")[0].strip()
        or (request.client.host if request.client else "")
    )
    log_request(
        method=request.method,
        path=request.url.path + (("?" + request.url.query) if request.url.query else ""),
        ip=fwd,
        ua=request.headers.get("user-agent", ""),
        status=response.status_code,
        ms=ms,
        ref=request.headers.get("referer", ""),
    )
    return response


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(notes_api.router)
app.include_router(summarize.router)
app.include_router(graphql_router.router)
app.include_router(debug.router)


@app.get("/healthz")
async def healthz():
    return {"ok": True}
