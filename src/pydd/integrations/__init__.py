"""Framework install helpers."""

from pydd.integrations.django import PyddMiddleware, install_django
from pydd.integrations.fastapi import install_fastapi, patch_fastapi
from pydd.integrations.flask import install_flask

__all__ = [
    'install_fastapi',
    'install_flask',
    'install_django',
    'PyddMiddleware',
    'patch_fastapi',
]
