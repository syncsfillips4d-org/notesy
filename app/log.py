"""Structured request logging on stdout."""
import json
import os
import sys
import time
from typing import Any


def _emit(payload: dict[str, Any]) -> None:
    payload["ts"] = time.time()
    sys.stdout.write(json.dumps(payload, default=str) + "\n")
    sys.stdout.flush()


def log_request(*, method: str, path: str, ip: str, ua: str, status: int, ms: float, ref: str) -> None:
    _emit({
        "kind": "http",
        "method": method,
        "path": path,
        "ip": ip,
        "ua": ua,
        "status": status,
        "ms": round(ms, 1),
        "ref": ref,
    })
