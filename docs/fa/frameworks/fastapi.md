# FastAPI

با `import pydd`، FastAPI **خودکار** وصل می‌شود. نیازی به `install()` دستی نیست.

## نصب و اجرا

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

## دامپ در route

```python
from pathlib import Path
from fastapi import FastAPI
from pydd import configure, dd

configure(project_root=Path(__file__).resolve().parent)

app = FastAPI()

@app.get("/posts/{post_id}")
def show_post(post_id: int):
    post = load_post(post_id)
    dd(post)   # HTML 500 در مرورگر
```

`import pydd` روی `FastAPI.__init__` patch می‌زند:

1. HTTP middleware — پرچم in-request؛ اگر boot آماده باشد HTML را برمی‌گرداند
2. Exception handler — `DdException` → `HTMLResponse(status=500)`

## Boot dump

در startup دامپ آماده کنید؛ سرور زنده می‌ماند:

```python
app = FastAPI()
dd(app)   # تا restart هر درخواست همان HTML را می‌دهد
```

!!! warning
    در boot mode **هر URL** همان دامپ را برمی‌گرداند. وقتی تمام شد `dd(app)` را بردارید و restart کنید.

خروجی کنسول:

```text
[pydd] Dump armed → http://127.0.0.1:8000/
```

تب مرورگر را refresh کنید — مرورگر خودکار باز نمی‌شود.

Host/port از `HOST`/`PORT` یا `UVICORN_HOST`/`UVICORN_PORT` (پیش‌فرض `127.0.0.1:8000`).

## تأیید با curl

```bash
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/posts/1
# 500 وقتی dd() در route اجرا شود
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

## بدون auto-patch (پیشرفته)

اگر side effect import نمی‌خواهید:

```python
from pydd.integrations import install_fastapi

app = FastAPI()
install_fastapi(app)
```

patch خودکار برای instanceهای دیگر `FastAPI()` در همان process از بین می‌رود.

## لینک‌ها

- [شروع سریع](../getting-started.md)
- [دمو](../demo.md)
- [PyPI — pydd-web](https://pypi.org/project/pydd-web/)
- [GitHub — pydd](https://github.com/ardavanshamroshan/pydd)
