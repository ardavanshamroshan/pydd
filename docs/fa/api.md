# مرجع API

## توابع عمومی

| تابع | توضیح |
|------|--------|
| `dd(*args, **kwargs)` | دامپ و توقف — HTML 500 در درخواست، boot، یا خروج ترمینال |
| `dump(*args, **kwargs)` | دامپ روی stderr بدون توقف (در درخواست: فقط stderr) |
| `render_html(*args, **kwargs)` | رشته HTML بدون raise |
| `render_text(*args, **kwargs)` | رشته ترمینال via pydump |
| `configure(project_root=...)` | مسیر پایه برای tipهای `// file:line` |
| `install_helpers()` | تزریق `dd`/`dump` آگاه از وب به builtins |

## انواع عمومی

| نماد | توضیح |
|------|--------|
| `DdException` | در درخواست raise؛ `.html` برای handler فریم‌ورک |
| `DumpNode` | گره درخت inspection pydump (re-export) |
| `inspect_value(value)` | value → `DumpNode` (re-export) |
| `pydump` | re-export ماژول pydump |

## helperهای integration

```python
from pydd.integrations import (
    install_fastapi,
    install_flask,
    install_django,
    PyddMiddleware,
    patch_fastapi,
)
```

| تابع | کاربرد |
|------|--------|
| `install_fastapi(app)` | middleware + handler روی یک app FastAPI |
| `install_flask(app)` | hookهای Flask |
| `install_django()` | no-op — middleware در settings |
| `PyddMiddleware` | کلاس middleware Django |
| `patch_fastapi()` | patch سراسری `FastAPI.__init__` (با `import pydd`) |

## درخت تصمیم `dd()`

```
dd(*args, **kwargs)
  │
  ├─ ساخت صفحه HTML
  │
  ├─ در HTTP؟  → raise DdException(page)  → فریم‌ورک 500 HTML
  │
  ├─ app FastAPI در args/kwargs?  → arm boot HTML، return
  │
  └─ else  → چاپ ترمینال، SystemExit(1)
```

## چند مقدار

```python
dd(user, post, filters=query_params)
```

هر آرگومان positional و keyword بلوک دامپ جدا دارد.

## پیکربندی tip

```python
from pathlib import Path
from pydd import configure

configure(project_root=Path(__file__).resolve().parent)
```

Tipها مسیر نسبی به `project_root`، مثلاً `// app/views.py:42`.

## ویرایشگر و linter {#editor-and-linter}

تزریق builtin در runtime کار می‌کند؛ analyzerها نیاز به تنظیم دارند.

### Ruff

```toml
[tool.ruff]
builtins = ["dd", "dump"]
```

### Pyright / Pylance

Import صریح:

```python
from pydd import dd, dump
```

یا فقط type-check:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydd import dd, dump

dd(user)
```

### PyCharm

Inspections → Python → Unresolved references → ignored: `dd`, `dump`

!!! warning
    **`typings/builtins.pyi` کامل نفرستید** — typeshed را خراب می‌کند.

## نسخه

```python
import pydd
print(pydd.__version__)  # مثلاً 0.2.4
```

## لینک‌ها

- [PyPI — pydd-web](https://pypi.org/project/pydd-web/)
- [GitHub — pydd](https://github.com/ardavanshamroshan/pydd)
- [API pydump](https://ardavanshamroshan.github.io/pydump/fa/api/)
