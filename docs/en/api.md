# API Reference

## Public functions

| Function | Description |
|----------|-------------|
| `dd(*args, **kwargs)` | Dump and stop — HTML 500 in request, boot arm, or terminal exit |
| `dump(*args, **kwargs)` | Dump to stderr without stopping (in requests: stderr only) |
| `render_html(*args, **kwargs)` | Return HTML string without raising |
| `render_text(*args, **kwargs)` | Return terminal string via pydump |
| `configure(project_root=...)` | Set base path for `// file:line` tips |
| `install_helpers()` | Inject web-aware `dd`/`dump` into builtins |

## Public types

| Symbol | Description |
|--------|-------------|
| `DdException` | Raised in-request; carries `.html` for framework handlers |
| `DumpNode` | Tree node from pydump inspection (re-export) |
| `inspect_value(value)` | Walk value → `DumpNode` (re-export from pydump) |
| `pydump` | Module re-export for terminal-only use |

## Integration helpers

```python
from pydd.integrations import (
    install_fastapi,
    install_flask,
    install_django,
    PyddMiddleware,
    patch_fastapi,
)
```

| Function | Use |
|----------|-----|
| `install_fastapi(app)` | Register middleware + handler on one FastAPI app |
| `install_flask(app)` | Register Flask hooks |
| `install_django()` | No-op reminder — use middleware in settings |
| `PyddMiddleware` | Django middleware class |
| `patch_fastapi()` | Patch `FastAPI.__init__` globally (called on `import pydd`) |

## `dd()` decision tree

```
dd(*args, **kwargs)
  │
  ├─ build HTML page
  │
  ├─ in HTTP request?  → raise DdException(page)  → framework returns 500 HTML
  │
  ├─ FastAPI app in args/kwargs?  → arm boot HTML on app, return
  │
  └─ else  → print terminal dump, SystemExit(1)
```

## Multiple values

```python
dd(user, post, filters=query_params)
```

Each positional and keyword argument produces a separate dump block.

## Configure tips

```python
from pathlib import Path
from pydd import configure

configure(project_root=Path(__file__).resolve().parent)
```

Tips show paths relative to `project_root`, e.g. `// app/views.py:42`.

## Editor and linter

Runtime builtin injection works at runtime but static analyzers need help.

### Ruff

```toml
[tool.ruff]
builtins = ["dd", "dump"]
```

### Pyright / Pylance / basedpyright

Prefer explicit import:

```python
from pydd import dd, dump
```

Or type-checking only:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydd import dd, dump

dd(user)  # runtime uses builtin if pydd was imported elsewhere
```

### PyCharm

Inspections → Python → Unresolved references → ignored identifiers: `dd`, `dump`

!!! warning
    Do **not** ship a full `typings/builtins.pyi` — it can replace typeshed and break project typing.

## Version

```python
import pydd
print(pydd.__version__)  # e.g. 0.2.4
```

## Links

- [PyPI — pydd-web](https://pypi.org/project/pydd-web/)
- [GitHub — pydd](https://github.com/ardavanshamroshan/pydd)
- [pydump API](https://ardavanshamroshan.github.io/pydump/en/api/)
