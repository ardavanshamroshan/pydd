# pydd

**Dump and die for Python web apps.** HTML dumps in the browser during HTTP requests; terminal output everywhere else.

Built on **[pydump](https://pypi.org/project/pydump-dd/)** — the terminal dump-and-die core.

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } **Install**

    ---

    `pip install pydd-web`

    [:octicons-arrow-right-24: Installation guide](installation.md)

-   :material-rocket-launch:{ .lg .middle } **Get started**

    ---

    Add `dd()` to a FastAPI route in minutes.

    [:octicons-arrow-right-24: Getting started](getting-started.md)

-   :material-language-python:{ .lg .middle } **PyPI**

    ---

    Distribution name: **`pydd-web`**

    [:octicons-link-external-24: pydd-web on PyPI](https://pypi.org/project/pydd-web/)

-   :material-github:{ .lg .middle } **GitHub**

    ---

    Source, issues, and contributions.

    [:octicons-link-external-24: ardavanshamroshan/pydd](https://github.com/ardavanshamroshan/pydd)

</div>

## Quick example

```python
import pydd  # installs dd/dump as builtins + FastAPI patch

@app.get("/posts/{post_id}")
def show_post(post_id: int):
    post = load_post(post_id)
    dd(post)   # HTML 500 in browser — no from-import needed
```

Explicit import still works: `from pydd import dd, dump, render_html, render_text`.

## What pydd does

| Context | Behavior |
|---------|----------|
| Inside an HTTP request | Interactive **HTML** dump → HTTP **500** response |
| CLI / script / test | **Terminal** dump via pydump → `SystemExit(1)` |
| `dd(fastapi_app)` at boot | **Arm** HTML on every request; server stays running |

## Supported frameworks

| Framework | Setup |
|-----------|--------|
| **FastAPI** | Auto-wired on `import pydd` |
| **Flask** | `install_flask(app)` |
| **Django** | `PyddMiddleware` in `MIDDLEWARE` |

## pydump vs pydd

| Need | Package | PyPI name |
|------|---------|-----------|
| Scripts, CLI, tests | [pydump](https://ardavanshamroshan.github.io/pydump/) | `pydump-dd` |
| FastAPI / Flask / Django | **pydd** (this package) | `pydd-web` |
| Both | Install **pydd** only | pulls in `pydump-dd` |

## License

MIT — see [GitHub repository](https://github.com/ardavanshamroshan/pydd).
