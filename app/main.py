import os
import time
from urllib.parse import parse_qsl, urlencode

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.log import log_request
from app.routers import auth, debug, graphql_router, notes_api, pages, summarize

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# Fail closed when running on Fly without proper config.
if os.environ.get("FLY_APP_NAME"):
    _required = ["BACKEND_URL", "BACKEND_KEY", "SESSION_SECRET"]
    _missing = [k for k in _required if not os.environ.get(k)]
    if _missing:
        raise SystemExit(f"missing required env vars: {', '.join(_missing)}")

app = FastAPI(
    title="notesy",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

SENSITIVE_QUERY_NAMES = {
    "api_key",
    "apikey",
    "auth",
    "authorization",
    "backend_key",
    "key",
    "password",
    "secret",
    "token",
}


def _redacted_path(request: Request) -> str:
    query = request.url.query
    if not query:
        return request.url.path
    pairs = []
    for name, value in parse_qsl(query, keep_blank_values=True):
        clean_name = name.lower().replace("-", "_")
        pairs.append((name, "[redacted]" if clean_name in SENSITIVE_QUERY_NAMES and value else value))
    return request.url.path + "?" + urlencode(pairs)


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
        path=_redacted_path(request),
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
