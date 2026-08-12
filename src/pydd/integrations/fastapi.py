"""FastAPI integration."""

from __future__ import annotations

from typing import Any

from pydd.context import DdException, reset_in_request, set_in_request

_PATCHED = False


def _boot_html(app: Any) -> str | None:
    return getattr(app, '_pydd_boot_html', None)


def install_fastapi(app: Any) -> None:
    if getattr(app, '_pydd_installed', False):
        return

    @app.middleware('http')
    async def _pydd_scope(request: Any, call_next: Any) -> Any:
        boot = _boot_html(app)
        if boot is not None:
            from fastapi.responses import HTMLResponse
            return HTMLResponse(content=boot, status_code=500)
        token = set_in_request(True)
        try:
            return await call_next(request)
        finally:
            reset_in_request(token)

    @app.exception_handler(DdException)
    async def _on_dd(request: Any, exc: DdException) -> Any:
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=exc.html, status_code=500)

    app._pydd_installed = True


def patch_fastapi() -> None:
    global _PATCHED
    if _PATCHED:
        return
    try:
        from fastapi import FastAPI
    except ImportError:
        return
    original = FastAPI.__init__

    def wrapped(self: Any, *args: Any, **kwargs: Any) -> None:
        original(self, *args, **kwargs)
        install_fastapi(self)

    FastAPI.__init__ = wrapped  # type: ignore[method-assign]
    _PATCHED = True
