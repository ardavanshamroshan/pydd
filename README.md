# pydd

**Documentation:** [English](https://ardavanshamroshan.github.io/pydd/) · [فارسی](https://ardavanshamroshan.github.io/pydd/fa/)  
**PyPI:** [pydd-web](https://pypi.org/project/pydd-web/) · **GitHub:** [ardavanshamroshan/pydd](https://github.com/ardavanshamroshan/pydd)

**Dump and die for Python web apps.** HTML dumps in the browser during HTTP requests; terminal output everywhere else.

Built on **[pydump](https://pypi.org/project/pydump-dd/)** (`pydump-dd` on PyPI — installed automatically when you install `pydd-web`):

```python
import pydd  # installs dd/dump as builtins + FastAPI patch

dd(user)     # no from-import needed in this file
dump(data)
```

Explicit import still works: `from pydd import dd, dump, render_html, render_text`.

## Preview

### In a web request (HTML)

Visiting a debug route returns a **500** response with an interactive dark-theme dump:

```text
dict:4 [▼ // views.py:18
  "id" => 1
  "author" => "Jane Doe"
  "title" => "Hello world"
  "tags" => list:3 [▶]
]
```

Click `list:3 [▶]` (or the whole header) to expand nested data in the browser.

### Outside a request (terminal)

Same data falls back to **pydump** text on stderr — fully expanded, no collapse:

```text
dict:4 [
  "id" => 1
  ...
] // script.py:10
```

### Boot-time dump (`dd(app)`)

Pass your FastAPI app at import time to arm a dump while the server keeps running. Refresh the existing tab (or visit the printed URL) to see it — no auto-open:

```python
app = FastAPI()
dd(app)  # every request serves dump HTML until restart
```

## Introduction

`pydd` wires `pydump` into popular Python web frameworks:

| Framework | Setup |
|-----------|--------|
| **FastAPI** | Auto-wired on `import pydd` |
| **Flask** | `install_flask(app)` |
| **Django** | `PyddMiddleware` in `MIDDLEWARE` |

Inside an HTTP request, `dd()` raises `DdException` with HTML; the framework returns it as a 500 page. Outside a request, behavior matches `pydump`.

## Installation

PyPI distribution names: **`pydd-web`** (this package) and **`pydump-dd`** (terminal core, dependency).  
Import names unchanged: `import pydd`, `import pydump`.

Install **pydd only** (pulls in pydump-dd):

```bash
pip install pydd-web
# or with a framework extra
pip install "pydd-web[fastapi]"
pip install "pydd-web[flask]"
pip install "pydd-web[django]"
pip install "pydd-web[all]"
```

Install **pydump only** (terminal, no web — no pydd):

```bash
pip install pydump-dd
```

### pip + venv

```bash
cd myapp
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install pydd-web
```

With a framework extra (when you do not already have it installed):

```bash
pip install "pydd-web[fastapi]"
pip install "pydd-web[flask]"
pip install "pydd-web[django]"
pip install "pydd-web[all]"
```

| Extra | Adds |
|-------|------|
| `fastapi` | FastAPI |
| `flask` | Flask |
| `django` | Django |
| `all` | All three |

### uv

```bash
cd myapp
uv add pydd-web
# or
uv add "pydd-web[fastapi]"
```

`pyproject.toml`:

```toml
[project]
dependencies = [
    "fastapi[standard]",
    "pydd-web>=0.2.2",
]
```

Run:

```bash
uv run uvicorn main:app --reload
```

`pydump-dd` is pulled in automatically as a dependency of `pydd-web`.

### Install into the pydd repo itself (development)

```bash
cd /path/to/pydd
pip install -e ".[dev]"
# or
uv sync --extra dev
uv run pytest -q
```

### Test projects

| Project | Stack |
|---------|--------|
| FastAPI | `../blog` |
| Django | `../testDDInDjango` |
| Flask | `../testDDInFlask` |
| Terminal only | `../pyexample` (uses `pydump` directly) |

---

## FastAPI

### Install and run

```bash
cd myapp
uv init                    # skip if project exists
uv add "fastapi[standard]"
uv add pydd-web
uv run uvicorn main:app --reload
```

Or with pip:

```bash
pip install "pydd-web[fastapi]"
uvicorn main:app --reload
```

`pyproject.toml` (uv):

```toml
dependencies = ["fastapi[standard]", "pydd-web>=0.2.2"]
```

### Code

```python
from pathlib import Path
from fastapi import FastAPI
from pydd import configure, dd

configure(project_root=Path(__file__).resolve().parent)

app = FastAPI()

@app.get("/posts/{post_id}")
def show_post(post_id: int):
    post = load_post(post_id)
    dd(post)   # HTML 500 in browser
```

Importing `pydd` patches `FastAPI.__init__` to register middleware and a `DdException` handler. No manual `install()` call.

### Boot dump

```python
app = FastAPI()
dd(app)   # arms HTML on app; refresh http://127.0.0.1:8000/
```

Useful when debugging app wiring at startup. **Every request** returns the dump until you remove `dd(app)` and restart. No browser is opened automatically.

### Verify

```bash
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/posts/1
# 500 when dd() runs in route
```

---

## Flask

### Install and run

```bash
cd myapp
uv init
uv add flask
uv add pydd-web
uv run python app.py
```

Or with pip:

```bash
pip install "pydd-web[flask]"
python app.py
```

### Code

```python
from pathlib import Path
from flask import Flask, request
from pydd import configure, dd
from pydd.integrations import install_flask

configure(project_root=Path(__file__).resolve().parent)

app = Flask(__name__)
install_flask(app)

@app.get("/dd")
def debug_dump():
    dd({
        "title": "Flask dd test",
        "query": dict(request.args),
    })
```

`install_flask` registers `before_request` / `teardown_request` for the request flag and an error handler for `DdException`.

---

## Django

### Install and run

```bash
cd myapp
uv init
uv add django
uv add pydd-web
uv run python manage.py migrate
uv run python manage.py runserver
```

Or with pip:

```bash
pip install "pydd-web[django]"
python manage.py migrate
python manage.py runserver
```

### Settings

```python
# config/settings.py
from pathlib import Path
from pydd import configure

BASE_DIR = Path(__file__).resolve().parent.parent
configure(project_root=BASE_DIR)

MIDDLEWARE = [
    # ...
    "pydd.integrations.django.PyddMiddleware",
]
```

### View

```python
# debugapp/views.py
from django.http import HttpResponse
from pydd import dd

def home(request):
    return HttpResponse('<a href="/dd/">/dd/</a>')

def debug_dump(request):
    dd({
        "title": "Django dd test",
        "query": dict(request.GET),
    })
```

`PyddMiddleware` sets the request context and catches `DdException` in `__call__`, returning `HttpResponse(status=500)`.

---

## Usage reference

### API

| Call | In HTTP request | CLI / script | `dd(app)` boot |
|------|-----------------|----------------|----------------|
| `dd(x)` | HTML 500 | stderr + exit 1 | arm HTML (refresh tab) |
| `dump(x)` | stderr only | stderr only | stderr only |
| `render_html(x)` | string | string | string |
| `render_text(x)` | string | string | string |
| `install_helpers()` | inject builtins (auto on `import pydd`; overrides pydump) | | |

After `import pydd` once (e.g. in `main.py`), use `dd` / `dump` in any module without importing them again.

### Editor / linter (Ruff, Pyright, PyCharm)

Runtime inject ≠ static name. Ruff / basedpyright / Pylance / PyCharm do **not** see `builtins.dd` from `install_helpers()`. Runtime works; the editor stays blind unless you configure or import.

**Ruff** — treat helpers like real builtins in the consumer `pyproject.toml`:

```toml
[tool.ruff]
builtins = ["dd", "dump"]
```

**Cursor / VS Code / basedpyright / Pylance** — prefer an explicit import (cleanest for the IDE):

```python
from pydd import dd, dump

dd(user)
```

Same functions as the builtins path. Still fine to keep `import pydd` in `main.py` for FastAPI patch + runtime inject.

Type-only alternative (bare `dd()` at runtime, import for the checker only):

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydd import dd, dump

dd(user)
```

**PyCharm** — Inspections → Python → Unresolved references → ignored identifiers: `dd`, `dump` — or use `from pydd import dd`.

Do **not** ship a full `typings/builtins.pyi` to fake these names: a complete `builtins.pyi` can replace typeshed stubs and break typing for the whole project.

### Multiple values

```python
dd(user, post, filters=query_params)
```

### Configure tips

```python
from pathlib import Path
from pydd import configure

configure(project_root=Path(__file__).resolve().parent)
```

## Advantages

- **Two modes, one API** — HTML in requests, text elsewhere
- **FastAPI zero-config** — import and use
- **Laravel-style helpers** — `import pydd` once, then `dd` / `dump` as builtins
- **Includes pydump** — terminal debugging without a second dependency
- **Interactive HTML** — expand/collapse nested structures in the browser
- **Boot mode** — inspect a FastAPI app at startup without killing the server
- **Framework hooks** — Flask and Django supported explicitly
- **Shared inspection** — same `DumpNode` tree as `pydump`

## Disadvantages

- **Not for production** — `dd()` is a debugger; it stops the request with HTTP 500
- **Boot mode hijacks all routes** — while armed, every URL serves the dump
- **HTML collapse does not exist in terminal** — use `render_text` / `pydump` for full CLI trees
- **Dynamic builtins vs checkers** — Ruff needs `builtins = ["dd", "dump"]`; Pyright/Pylance need an explicit or `TYPE_CHECKING` import (see Editor / linter)
- **FastAPI monkey-patch** — patches `FastAPI.__init__`; avoid if you need strict import side-effect control (call `install_fastapi` manually instead and skip auto-patch — advanced)
- **Limited object dumping** — same introspection limits as `pydump`
- **Django** — requires middleware entry in `settings.py` (not automatic)

## pydump vs pydd

| Need | Package |
|------|---------|
| Scripts, CLI, tests, notebooks | `pydump` |
| FastAPI / Flask / Django | `pydd` |
| Both | `pydd` only |

## License

MIT
