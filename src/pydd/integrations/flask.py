"""Flask integration."""

from __future__ import annotations

from typing import Any

from pydd.context import DdException, reset_in_request, set_in_request


def install_flask(app: Any) -> None:
    if getattr(app, '_pydd_installed', False):
        return

    @app.before_request
    def _pydd_enter() -> None:
        app._pydd_token = set_in_request(True)

    @app.teardown_request
    def _pydd_leave(exc: BaseException | None = None) -> None:
        token = getattr(app, '_pydd_token', None)
        if token is not None:
            reset_in_request(token)
            app._pydd_token = None

    @app.errorhandler(DdException)
    def _on_dd(exc: DdException) -> tuple[str, int]:
        return exc.html, 500

    app._pydd_installed = True
