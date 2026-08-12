# Demo

Copy-paste examples you can run locally. All demos return **HTTP 500** when `dd()` fires — that is expected.

## Sample output (HTML)

When you visit a debug route in the browser:

```text
dict:4 [▼ // views.py:18
  "id" => 1
  "author" => "Jane Doe"
  "title" => "Hello world"
  "tags" => list:3 [▶]
]
```

Click `list:3 [▶]` or the header to expand nested data.

## Sample output (terminal)

Same data outside a request:

```text
dict:4 [
  "id" => 1
  "author" => "Jane Doe"
  "title" => "Hello world"
  "tags" => list:3 [
    0 => "python"
    1 => "debug"
    2 => "pydd"
  ]
] // script.py:10
```

---

## FastAPI demo

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

@app.get("/")
def root():
    return {"message": "Visit /demo to trigger dd()"}

@app.get("/demo")
def demo():
    dd(SAMPLE)
```

```bash
pip install "pydd-web[fastapi]"
uvicorn main:app --reload
# open http://127.0.0.1:8000/demo
```

---

## Flask demo

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
        "sample": {"id": 1, "tags": ["flask", "pydd"]},
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
```

```bash
pip install "pydd-web[flask]"
python app.py
# open http://127.0.0.1:5000/demo?foo=bar
```

---

## Django demo

Minimal debug view:

```python
# myapp/views.py
from pydd import dd

def demo(request):
    dd({
        "title": "Django demo",
        "GET": dict(request.GET),
        "method": request.method,
    })
```

Add URL + middleware per [Django guide](frameworks/django.md).

---

## CLI demo (terminal only)

No web server — uses pydump fallback:

```python
import pydd

data = {"framework": None, "mode": "terminal"}
dd(data)  # prints to stderr, exits 1
```

Or use pydump directly: [pydump demo](https://ardavanshamroshan.github.io/pydump/en/demo/).

---

## Boot mode demo (FastAPI)

```python
from fastapi import FastAPI
from pydd import dd

app = FastAPI()
dd(app)  # arm — refresh http://127.0.0.1:8000/any-path
```

Console:

```text
[pydd] Dump armed → http://127.0.0.1:8000/
```

---

## Links

| Resource | URL |
|----------|-----|
| PyPI | [pypi.org/project/pydd-web](https://pypi.org/project/pydd-web/) |
| GitHub | [github.com/ardavanshamroshan/pydd](https://github.com/ardavanshamroshan/pydd) |
| pydump demo | [ardavanshamroshan.github.io/pydump/en/demo/](https://ardavanshamroshan.github.io/pydump/en/demo/) |
