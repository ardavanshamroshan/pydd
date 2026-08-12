# Getting started

This guide gets you from zero to an HTML dump in a FastAPI app in under five minutes.

## Prerequisites

- Python **3.10+**
- A web framework (FastAPI, Flask, or Django)

## 1. Install

```bash
pip install pydd-web
```

For FastAPI with all server extras:

```bash
pip install "pydd-web[fastapi]"
```

See the full [Installation](installation.md) guide for pip, uv, and framework extras.

## 2. Minimal FastAPI app

Create `main.py`:

```python
from pathlib import Path
from fastapi import FastAPI
from pydd import configure, dd

configure(project_root=Path(__file__).resolve().parent)

app = FastAPI()

@app.get("/debug")
def debug_route():
    user = {"id": 1, "name": "Ada", "roles": ["admin", "editor"]}
    dd(user)
```

## 3. Run the server

```bash
uvicorn main:app --reload
```

## 4. Trigger the dump

Open [http://127.0.0.1:8000/debug](http://127.0.0.1:8000/debug) in your browser.

You should see:

- HTTP status **500** (expected — `dd()` stops the request)
- A **dark-theme interactive dump** with expand/collapse on nested data
- A tip line like `// main.py:14 · user · container · dict`

## 5. Use Laravel-style globals (optional)

Instead of `from pydd import dd`, you can rely on builtins:

```python
import pydd  # once, e.g. in main.py

# in any other module — no import needed
dd(some_value)
```

!!! note "Editor / linter"
    Ruff and type checkers do not see injected builtins. Add `[tool.ruff] builtins = ["dd", "dump"]` or use explicit imports. See [API Reference — Editor setup](api.md#editor-and-linter).

## Next steps

- [FastAPI guide](frameworks/fastapi.md) — boot mode, verification, TestClient
- [Flask guide](frameworks/flask.md) — `install_flask(app)`
- [Django guide](frameworks/django.md) — middleware setup
- [Demo](demo.md) — copy-paste examples for all frameworks
- [Features](features.md) — full capability list

## Links

| Resource | URL |
|----------|-----|
| PyPI | [pypi.org/project/pydd-web](https://pypi.org/project/pydd-web/) |
| GitHub | [github.com/ardavanshamroshan/pydd](https://github.com/ardavanshamroshan/pydd) |
| pydump docs | [ardavanshamroshan.github.io/pydump](https://ardavanshamroshan.github.io/pydump/) |
