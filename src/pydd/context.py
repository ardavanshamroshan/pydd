"""Request-scope flag so dd() knows HTTP vs CLI."""

from __future__ import annotations

from contextvars import ContextVar

_IN_REQUEST: ContextVar[bool] = ContextVar('pydd_http', default=False)


class DdException(Exception):
    """Raised inside HTTP request; framework returns HTML 500."""

    def __init__(self, content: str) -> None:
        self.html = content
        super().__init__('dd')


def in_request() -> bool:
    return _IN_REQUEST.get()


def set_in_request(value: bool):
    return _IN_REQUEST.set(value)


def reset_in_request(token) -> None:
    _IN_REQUEST.reset(token)
