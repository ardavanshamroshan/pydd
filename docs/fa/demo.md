# دمو

مثال‌های copy-paste برای اجرای محلی. همه با `dd()` **HTTP 500** می‌دهند — عادی است.

## نمونه خروجی (HTML)

باز کردن route دیباگ در مرورگر:

```text
dict:4 [▼ // views.py:18
  "id" => 1
  "author" => "Jane Doe"
  "title" => "Hello world"
  "tags" => list:3 [▶]
]
```

روی `list:3 [▶]` یا header کلیک کنید.

## نمونه خروجی (ترمینال)

همان داده خارج از درخواست:

```text
dict:4 [
  "id" => 1
  ...
  "tags" => list:3 [
    0 => "python"
    ...
  ]
] // script.py:10
```

---

## دمو FastAPI

`main.py`:

```python
from pathlib import Path
from fastapi import FastAPI
from pydd import configure, dd

configure(project_root=Path(__file__).resolve().parent)

app = FastAPI()

SAMPLE = {
    "id": 1,
    "author": "Jane Doe",
    "title": "Hello world",
    "tags": ["python", "debug", "pydd"],
}

@app.get("/demo")
def demo():
    dd(SAMPLE)
```

```bash
pip install "pydd-web[fastapi]"
uvicorn main:app --reload
# http://127.0.0.1:8000/demo
```

---

## دمو Flask

`app.py`:

```python
from pathlib import Path
from flask import Flask, request
from pydd import configure, dd
from pydd.integrations import install_flask

configure(project_root=Path(__file__).resolve().parent)

app = Flask(__name__)
install_flask(app)

@app.get("/demo")
def demo():
    dd({
        "title": "Flask demo",
        "query": dict(request.args),
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
```

```bash
pip install "pydd-web[flask]"
python app.py
```

---

## دمو Django

```python
# myapp/views.py
from pydd import dd

def demo(request):
    dd({
        "title": "Django demo",
        "GET": dict(request.GET),
    })
```

URL + middleware: [راهنمای Django](frameworks/django.md).

---

## دمو CLI (فقط ترمینال)

```python
import pydd
dd({"mode": "terminal"})  # stderr، خروج 1
```

یا pydump: [دمو pydump](https://ardavanshamroshan.github.io/pydump/fa/demo/).

---

## Boot mode (FastAPI)

```python
from fastapi import FastAPI
from pydd import dd

app = FastAPI()
dd(app)
```

---

## لینک‌ها

| منبع | آدرس |
|------|------|
| PyPI | [pypi.org/project/pydd-web](https://pypi.org/project/pydd-web/) |
| GitHub | [github.com/ardavanshamroshan/pydd](https://github.com/ardavanshamroshan/pydd) |
| دمو pydump | [ardavanshamroshan.github.io/pydump/fa/demo/](https://ardavanshamroshan.github.io/pydump/fa/demo/) |
