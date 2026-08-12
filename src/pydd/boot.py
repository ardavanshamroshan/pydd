"""Boot-time dump: arm HTML on app, serve via middleware."""

from __future__ import annotations

import os
import sys
from typing import Any


def is_fastapi(value: Any) -> bool:
    cls = type(value)
    return cls.__name__ == 'FastAPI' and (cls.__module__ or '').startswith('fastapi')


def find_app(*args: Any, **kwargs: Any) -> Any | None:
    for value in (*args, *kwargs.values()):
        if is_fastapi(value):
            return value
    return None


def server_url() -> str:
    host = os.environ.get('HOST') or os.environ.get('UVICORN_HOST') or '127.0.0.1'
    port = os.environ.get('PORT') or os.environ.get('UVICORN_PORT') or '8000'
    if host in {'0.0.0.0', '::'}:
        host = '127.0.0.1'
    return f'http://{host}:{port}/'


def arm(app: Any, page: str) -> None:
    """Store dump HTML on app; middleware serves it; server stays alive."""
    app._pydd_boot_html = page
    url = server_url()
    print(f'[pydd] Dump armed → {url}', file=sys.stderr)
