"""Django integration."""

from __future__ import annotations

from typing import Any

from pydd.context import DdException, reset_in_request, set_in_request


class PyddMiddleware:
    """Add to MIDDLEWARE: ``'pydd.integrations.django.PyddMiddleware'``."""

    def __init__(self, get_response: Any) -> None:
        self.get_response = get_response

    def __call__(self, request: Any) -> Any:
        token = set_in_request(True)
        try:
            return self.get_response(request)
        except DdException as exc:
            from django.http import HttpResponse
            return HttpResponse(exc.html, status=500, content_type='text/html')
        finally:
            reset_in_request(token)

    def process_exception(self, request: Any, exception: BaseException) -> Any:
        if isinstance(exception, DdException):
            from django.http import HttpResponse
            return HttpResponse(exception.html, status=500, content_type='text/html')
        return None


def install_django() -> None:
    """No-op reminder — add PyddMiddleware to settings.MIDDLEWARE."""
    pass
