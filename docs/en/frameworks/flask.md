# Flask

Flask requires an explicit **`install_flask(app)`** call. Boot mode is not available yet.

## Install and run

```bash
pip install "pydd-web[flask]"
python app.py
```

Or with uv:

```bash
uv add flask pydd-web
uv run python app.py
```

## Full example

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

if __name__ == "__main__":
    app.run(debug=True)
```

Visit [http://127.0.0.1:5000/dd](http://127.0.0.1:5000/dd) to see the HTML dump.

## What `install_flask` does

| Hook | Purpose |
|------|---------|
| `before_request` | Sets `in_request` flag via `ContextVar` |
| `teardown_request` | Resets the flag after each request |
| `@app.errorhandler(DdException)` | Returns `(html, 500)` |

Installation is idempotent — safe to call once at app creation.

## Laravel-style globals

```python
import pydd  # in app factory or wsgi entry

# elsewhere in blueprints
dd(blueprint_data)
```

## Links

- [Getting started](../getting-started.md)
- [Demo](../demo.md)
- [PyPI — pydd-web](https://pypi.org/project/pydd-web/)
- [GitHub — pydd](https://github.com/ardavanshamroshan/pydd)
