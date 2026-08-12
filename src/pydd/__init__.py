"""pydd — dump-and-die for FastAPI / Flask / Django (on top of pydump)."""

from pydump import DumpNode, inspect_value

from pydd.api import configure, dd, dump, install_helpers, render_html, render_text
from pydd.context import DdException
from pydd.integrations.fastapi import patch_fastapi

__all__ = [
    'dd',
    'dump',
    'configure',
    'render_html',
    'render_text',
    'install_helpers',
    'DdException',
    'DumpNode',
    'inspect_value',
    'pydump',
]
__version__ = '0.2.4'

# Installing pydd also installs pydump — expose for ``import pydump`` / ``from pydd import pydump``.
import pydump  # noqa: E402

# Auto-wire FastAPI when importable.
patch_fastapi()

# Laravel-style globals; override pydump builtins with web-aware dd/dump.
install_helpers()
