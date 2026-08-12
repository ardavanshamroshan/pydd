# Features

## Core capabilities

- **Two modes, one API** — HTML dumps inside HTTP requests; terminal dumps everywhere else
- **Laravel-style helpers** — `import pydd` once, then use `dd` / `dump` as builtins project-wide
- **Interactive HTML** — dark Symfony-style theme with expand/collapse on nested structures
- **Shared inspection core** — same `DumpNode` tree as [pydump](https://pypi.org/project/pydump-dd/)
- **Call-site tips** — `$variable · kind · type` and `// file:line` in HTML and terminal
- **Multiple values** — pass positional and keyword arguments; each gets its own dump block
- **Zero-config FastAPI** — middleware and exception handler installed on `import pydd`
- **Explicit Flask / Django hooks** — `install_flask(app)` and `PyddMiddleware`
- **Boot mode (FastAPI)** — `dd(app)` arms HTML on every request while the server keeps running
- **Includes pydump** — terminal debugging without a second dependency declaration

## Behavior matrix

| Call | In HTTP request | CLI / script | `dd(app)` boot |
|------|-----------------|----------------|----------------|
| `dd(x)` | HTML 500 | stderr + exit 1 | arm HTML (refresh tab) |
| `dump(x)` | stderr only | stderr only | stderr only |
| `render_html(x)` | return string | return string | return string |
| `render_text(x)` | return string | return string | return string |

## Framework integration

### FastAPI

- Auto-patches `FastAPI.__init__` to register middleware and `DdException` handler
- Request-scoped flag via `ContextVar` (async-safe)
- Boot mode serves armed HTML before any route runs
- Manual alternative: `install_fastapi(app)` without import side effects

### Flask

- `before_request` / `teardown_request` for request detection
- Error handler returns `(html, 500)` for `DdException`
- No boot mode yet

### Django

- `PyddMiddleware` sets request context in `__call__`
- Catches `DdException` and returns `HttpResponse(status=500)`
- Requires explicit middleware entry in `settings.py`

## HTML dump features

- Collapsible nested containers (click `▶` / header to expand)
- Separate `<pre class="sf-dump">` blocks for multiple values
- Tips on header line when collapsed: `[▶] // file:line`
- Tips after `[▼` when expanded
- Default collapse depth: `max_depth=1` in browser (terminal fully expands)

## Terminal fallback

When not in an HTTP request and no FastAPI app is passed to `dd()`:

- Delegates to pydump ANSI formatter on stderr
- Skips pydd internal frames in call-site tips
- `dd()` raises `SystemExit(1)` after printing

## Configuration

- `configure(project_root=Path(...))` — relative paths in `//` tips
- Boot URL hints from `HOST`, `PORT`, `UVICORN_HOST`, `UVICORN_PORT` env vars

## What pydd is not

!!! warning "Development only"
    - **Not for production** — stops the request with HTTP 500
    - **Boot mode hijacks all routes** until restart
    - **No HTML collapse in terminal** — use `render_text` for full CLI trees
    - **Limited object introspection** — same rules as pydump (public attrs only)

## Related packages

| Package | PyPI | Docs |
|---------|------|------|
| pydd | [pydd-web](https://pypi.org/project/pydd-web/) | You are here |
| pydump | [pydump-dd](https://pypi.org/project/pydump-dd/) | [pydump docs](https://ardavanshamroshan.github.io/pydump/) |
