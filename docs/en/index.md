# pydd

**Dump and die for Python web apps.** HTML dumps in the browser during HTTP requests; terminal output everywhere else.

Built on **[pydump](https://pypi.org/project/pydump-dd/)** — the terminal dump-and-die core.

<figure class="shot" markdown>
![pydd HTML dump in the browser](../assets/images/pydd-dd-web-result.jpg)
<figcaption>Interactive HTML dump — FastAPI / Flask / Django</figcaption>
</figure>

## Frameworks

Jump to setup for your stack:

<div class="grid cards fw-cards" markdown>

-   [![FastAPI](../assets/logos/fastapi.svg){ .fw-logo }](frameworks/fastapi.md)

    **[FastAPI](frameworks/fastapi.md)**

    Auto-wired on `import pydd`

-   [![Flask](../assets/logos/flask.svg){ .fw-logo }](frameworks/flask.md)

    **[Flask](frameworks/flask.md)**

    `install_flask(app)`

-   [![Django](../assets/logos/django.svg){ .fw-logo }](frameworks/django.md)

    **[Django](frameworks/django.md)**

    `PyddMiddleware`

</div>

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

## Live preview

<figure class="shot" markdown>
![Multi-variable HTML dump](../assets/images/pydd-dd-web-result.jpg)
<figcaption>Multiple vars — labeled panels in the browser</figcaption>
</figure>

<figure class="shot" markdown>
![Single dict dump panel](../assets/images/pydd-dd-dict-panel.jpg)
<figcaption>Typed header, expandable tree, call-site tip</figcaption>
</figure>

<figure class="shot" markdown>
![Terminal fallback via pydump](../assets/images/pydump-dd-terminal-result.jpg)
<figcaption>Outside HTTP — same data via pydump in the terminal</figcaption>
</figure>

## What pydd does

| Context | Behavior |
|---------|----------|
| Inside an HTTP request | Interactive **HTML** dump → HTTP **500** response |
| CLI / script / test | **Terminal** dump via pydump → `SystemExit(1)` |
| `dd(fastapi_app)` at boot | **Arm** HTML on every request; server stays running |

## pydump vs pydd

| Need | Package | PyPI name |
|------|---------|-----------|
| Scripts, CLI, tests | [pydump](https://ardavanshamroshan.github.io/pydump/) | `pydump-dd` |
| FastAPI / Flask / Django | **pydd** (this package) | `pydd-web` |
| Both | Install **pydd** only | pulls in `pydump-dd` |

## License

MIT — see [GitHub repository](https://github.com/ardavanshamroshan/pydd).
