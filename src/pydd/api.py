"""pydd public API — HTML dd for web frameworks, terminal via pydump."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from pydump import configure as pydump_configure
from pydump import render_text as pydump_render_text
from pydump.helpers import install_helpers as _install_helpers

from pydd.boot import arm, find_app
from pydd.context import DdException, in_request
from pydd.html import build_html

__all__ = [
    'dd',
    'dump',
    'configure',
    'render_html',
    'render_text',
    'install_helpers',
    'DdException',
]

_PACKAGE = Path(__file__).resolve().parent
_SKIP = (str(_PACKAGE),)


def configure(*, project_root: Path | str | None = None) -> None:
    pydump_configure(project_root=project_root)


def render_html(*args: Any, **kwargs: Any) -> str:
    return build_html(*args, **kwargs)


def render_text(*args: Any, **kwargs: Any) -> str:
    return pydump_render_text(*args, skip_packages=_SKIP, **kwargs)


def dump(*args: Any, **kwargs: Any) -> None:
    """Always terminal stderr (same as pydump.dump), tip skips pydd."""
    print(render_text(*args, **kwargs), file=sys.stderr)


def dd(*args: Any, **kwargs: Any) -> None:
    """Dump and die.

    - Inside wired HTTP request → raise DdException(HTML)
    - With FastAPI app arg → arm dump (server stays up; refresh tab)
    - Else → terminal text (pydump) + SystemExit(1)
    """
    page = build_html(*args, **kwargs)
    if in_request():
        raise DdException(page)
    app = find_app(*args, **kwargs)
    if app is not None:
        arm(app, page)
        return
    print(render_text(*args, **kwargs), file=sys.stderr)
    raise SystemExit(1)


def install_helpers() -> None:
    """Expose web-aware ``dd`` / ``dump`` as builtins (overrides pydump)."""
    _install_helpers(dd=dd, dump=dump)
