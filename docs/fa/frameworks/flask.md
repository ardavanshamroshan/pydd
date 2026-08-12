# Flask

Flask نیاز به **`install_flask(app)`** صریح دارد. boot mode هنوز نیست.

## نصب و اجرا

```bash
pip install "pydd-web[flask]"
python app.py
```

یا با uv:

```bash
uv add flask pydd-web
uv run python app.py
```

## مثال کامل

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

[http://127.0.0.1:5000/dd](http://127.0.0.1:5000/dd) را باز کنید.

## `install_flask` چه می‌کند

| Hook | کار |
|------|-----|
| `before_request` | پرچم `in_request` با `ContextVar` |
| `teardown_request` | reset بعد از هر درخواست |
| `@app.errorhandler(DdException)` | `(html, 500)` |

Idempotent — یک‌بار هنگام ساخت app کافی است.

## globals شبیه Laravel

```python
import pydd  # در factory یا wsgi

# در blueprintها
dd(blueprint_data)
```

## لینک‌ها

- [شروع سریع](../getting-started.md)
- [دمو](../demo.md)
- [PyPI — pydd-web](https://pypi.org/project/pydd-web/)
- [GitHub — pydd](https://github.com/ardavanshamroshan/pydd)
