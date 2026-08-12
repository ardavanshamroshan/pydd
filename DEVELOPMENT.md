# pydd — development guide

Architecture of `pydd`, how it extends `pydump`, and how framework integrations work.

## Repository layout

```
pydd/
├── src/pydd/
│   ├── __init__.py           # exports + FastAPI auto-patch + install_helpers()
│   ├── api.py                # dd, dump, render_html, render_text, install_helpers
│   ├── boot.py               # dd(app) boot mode (arm HTML, no browser open)
│   ├── context.py            # DdException, request ContextVar
│   ├── html.py               # DumpNode → HTML page
│   └── integrations/
│       ├── fastapi.py        # middleware + exception handler + patch
│       ├── flask.py          # before/teardown + errorhandler
│       └── django.py         # PyddMiddleware
├── tests/
└── pyproject.toml            # depends on pydump-dd (PyPI)
```

Terminal core: **`pydump-dd`** on PyPI (`import pydump`).

## Dependency graph

```
pydd.api
  ├─ pydump (configure, dump, render_text)
  ├─ pydump.helpers (install_helpers → builtins)
  ├─ pydd.html (build_html)
  ├─ pydd.boot (arm, find_app)
  └─ pydd.context (DdException, in_request)

pydd.html
  └─ pydump.core (inspect_value, DumpNode, caller_frame)

integrations/*
  └─ pydd.context
```

No circular imports. HTML and text formatters share **`inspect_value()`** only.

## `dd()` decision tree (`api.py`)

```
build_html(*args, **kwargs)
    │
    ├─ in_request() ?
    │     └─ raise DdException(html)  → framework returns 500
    │
    ├─ find_app(*args) is FastAPI ?
    │     └─ arm(app, html)           → boot mode, return (no exit)
    │
    └─ else
          └─ print render_text(...)   → pydump terminal
             raise SystemExit(1)
```

### Request detection (`context.py`)

`ContextVar[bool]` set `True` in framework middleware during each HTTP request. Async-safe per task.

### Boot mode (`boot.py`)

Problem: `dd(app)` at module import must not `sys.exit` before uvicorn starts.

Solution:

1. Store HTML on `app._pydd_boot_html`
2. FastAPI middleware checks boot HTML **before** normal routing
3. Print dump URL to stderr (no browser open — refresh existing tab)

`find_app()` scans `args`/`kwargs` for an explicit `FastAPI` instance only.

## HTML formatter (`html.py`)

Walks the same `DumpNode` tree as `pydump`, emits interactive HTML markup:

- `dict:4 [▼` clickable header (`<a class="sf-dump-toggle">`)
- `"key" => value` with color spans
- Collapsed children via `sf-dump-compact` / `sf-dump-expanded` + small JS toggle
- `// file:line` tip: after `[▼` when expanded; after `]` when collapsed (`[▶] // file`) via tip-in / tip-out CSS

Terminal output intentionally differs: **pydump expands everything**; **pydd HTML collapses** nested levels for browser UX.

## Framework integrations

### FastAPI (`integrations/fastapi.py`)

**`patch_fastapi()`** — wraps `FastAPI.__init__` to call `install_fastapi(self)`.

**Middleware order matters:**

1. If `app._pydd_boot_html` → return `HTMLResponse(500)` immediately
2. Else set `in_request`, call `call_next`, reset context

**Exception handler** — `DdException` → `HTMLResponse(exc.html, 500)`

### Flask (`integrations/flask.py`)

- `before_request` → `set_in_request(True)`
- `teardown_request` → reset token
- `@app.errorhandler(DdException)` → `(html, 500)`

No boot-mode support for Flask yet (only FastAPI `arm()`).

### Django (`integrations/django.py`)

**`PyddMiddleware`** — new-style middleware:

```python
def __call__(self, request):
    token = set_in_request(True)
    try:
        return self.get_response(request)
    except DdException as exc:
        return HttpResponse(exc.html, status=500)
    finally:
        reset_in_request(token)
```

`process_exception` kept for compatibility but **`__call__` catch is required** for modern Django middleware.

## Public exports (`__init__.py`)

Re-exports pydump symbols for convenience:

- `DumpNode`, `inspect_value`
- `import pydump` as `pydd.pydump`

Installing `pydd` alone is enough for terminal + web APIs.

## Testing

### Unit tests

```bash
cd pydd
uv sync --extra dev
uv run pytest -q
```

Covers HTML render, terminal fallback, `DdException`, boot mode with `TestClient`.

### Integration projects

| Directory | Command | What it proves |
|-----------|---------|----------------|
| `../blog` | `uvicorn main:app` | FastAPI route + boot `dd(app)` |
| `../testDDInFlask` | `python app.py` | Flask `/dd` HTML |
| `../testDDInDjango` | `manage.py runserver` | Django `/dd/` HTML |
| `../testdump` | `python test_dd.py` | pydump only (not pydd) |

### FastAPI smoke (in-repo)

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydd import dd

app = FastAPI()

@app.get("/")
def root():
    dd({"ok": True})

client = TestClient(app, raise_server_exceptions=False)
r = client.get("/")
assert r.status_code == 500
assert "sf-dump" in r.text
```

## Extending pydd

### New framework

1. Set `in_request` in middleware or `before_request`
2. Catch `DdException` → return HTML response with status 500
3. Optionally add boot-mode storage on app object

### Richer HTML

Edit `html.py` `format_node()` — keep using `inspect_value()` from pydump.

### Disable FastAPI auto-patch

```python
# import api/context/html directly, or fork patch_fastapi
# preferred: install_fastapi(app) manually and import submodules before FastAPI
```

For most apps, auto-patch is intentional DX.

## Packaging

- **Name:** `pydd`
- **Depends on:** `pydump-dd` from PyPI (`import pydump`)
- **Optional:** `fastapi`, `flask`, `django`, `all`, `dev`
- **Python:** `>=3.10`

## Design trade-offs

| Choice | Why |
|--------|-----|
| Split pydump / pydd | CLI users avoid web stack |
| HTML collapse only in pydd | Terminal cannot toggle |
| `DdException` not bare `Exception` | Avoid catching real bugs |
| FastAPI boot on `_pydd_boot_html` | Server stays alive for browser dump |
| Shared `DumpNode` | One inspection implementation |

## Version 0.1.0 scope

- Terminal via pydump
- HTML dumps in FastAPI, Flask, Django
- FastAPI auto-wire and boot mode
- No Pygments source panel (future)
- No Flask/Django boot mode (future)
