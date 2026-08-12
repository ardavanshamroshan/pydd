# FastAPI

FastAPI is **auto-wired** when you `import pydd`. No manual `install()` call needed.

## Install and run

=== "pip"

    ```bash
    pip install "pydd-web[fastapi]"
    uvicorn main:app --reload
    ```

=== "uv"

    ```bash
    uv add "pydd-web[fastapi]"
    uv run uvicorn main:app --reload
    ```

## Basic route dump

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

Importing `pydd` patches `FastAPI.__init__` to register:

1. HTTP middleware — sets the in-request flag; serves boot HTML if armed
2. Exception handler — converts `DdException` to `HTMLResponse(status=500)`

## Boot dump

Arm a dump at startup while keeping the server alive:

```python
app = FastAPI()
dd(app)   # every request serves dump HTML until restart
```

!!! warning
    While boot mode is armed, **every URL** returns the same dump. Remove `dd(app)` and restart when done.

The console prints something like:

```text
[pydd] Dump armed → http://127.0.0.1:8000/
```

Refresh your browser tab — no auto-open.

Host/port come from `HOST`/`PORT` or `UVICORN_HOST`/`UVICORN_PORT` (default `127.0.0.1:8000`).

## Verify with curl

```bash
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/posts/1
# 500 when dd() runs in route
```

## TestClient

```python
from fastapi.testclient import TestClient
import pydd
from main import app

client = TestClient(app)
response = client.get("/debug")
assert response.status_code == 500
assert "sf-dump" in response.text
```

## Avoid auto-patch (advanced)

If you need zero import side effects:

```python
# Do NOT import pydd at module level
from pydd.integrations import install_fastapi

app = FastAPI()
install_fastapi(app)
```

You lose automatic patching for other `FastAPI()` instances in the same process.

## Links

- [Getting started](../getting-started.md)
- [Demo](../demo.md)
- [PyPI — pydd-web](https://pypi.org/project/pydd-web/)
- [GitHub — pydd](https://github.com/ardavanshamroshan/pydd)
