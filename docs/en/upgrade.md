# Upgrade guide

How to upgrade **pydd-web** and its **pydump-dd** dependency safely.

## Current version

**0.2.4** — PyPI: [pydd-web](https://pypi.org/project/pydd-web/)

## Quick upgrade

```bash
pip install -U pydd-web
```

With uv:

```bash
uv add "pydd-web>=0.2.4"
```

## PyPI name change (0.2.2)

| Before | After |
|--------|-------|
| `pip install pydd` (old name) | **`pip install pydd-web`** |
| Local path to pydump | **`pydump-dd` from PyPI** |

**Import unchanged:** `import pydd`

Update `requirements.txt` / `pyproject.toml`:

```diff
- pydd>=0.2.1
+ pydd-web>=0.2.4
```

pydump is pulled automatically — you do not need a separate `pydump-dd` line unless you pin it explicitly.

## 0.2.3 → 0.2.4

- Docs site + project URLs on PyPI metadata
- Requires `pydump-dd>=0.2.4`
- No code changes required

## 0.2.2 → 0.2.3

- README/install docs fixed for PyPI names
- Requires `pydump-dd>=0.2.3`

No code changes required.

## 0.2.1 → 0.2.2

### Added
- HTML tips show `$variable · kind · type`
- MIT LICENSE file

### Changed
- Distribution renamed to **`pydd-web`**
- Depends on **`pydump-dd>=0.2.2`** from PyPI

### Action
Replace package name in dependencies. Reinstall:

```bash
pip uninstall pydd pydd-web 2>/dev/null; pip install pydd-web
```

## 0.2.0 → 0.2.1

### Added
- Laravel-style builtins: `import pydd` injects `dd`/`dump` (overrides pydump)
- `install_helpers()` for explicit re-install

### Fixed
- Boot `dd(app)` no longer auto-opens browser
- `dd(var)` outside request no longer hijacks via `last_app()` fallback
- Multiple HTML dumps separated visually
- Tip placement fixes in HTML and terminal

### Changed
- Document Ruff/IDE setup for builtins

### Action
If you relied on auto-open browser in boot mode, refresh the tab manually instead.

## 0.1.0 → 0.2.x

First stable web integration release. Migrate from ad-hoc debugging:

1. `pip install pydd-web`
2. `import pydd` in FastAPI entrypoint (or `install_flask` / Django middleware)
3. Replace `print()` debug with `dd()`

## Pinning versions

Production apps should not use `dd()` at all. For dev environments:

```toml
[project]
dependencies = [
    "pydd-web==0.2.4",
]
```

Or allow patch updates:

```toml
"pydd-web>=0.2.4,<0.3"
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: pydd` | Install **`pydd-web`**, not `pydd` on PyPI |
| Terminal tips show `pydd/api.py` | Upgrade to >= 0.2.1 |
| HTML dumps merged together | Upgrade to >= 0.2.1 |
| Missing `$variable` in tips | Upgrade pydump to >= 0.2.2 (via pydd upgrade) |

## Links

- [Changelog](changelog.md)
- [PyPI — pydd-web](https://pypi.org/project/pydd-web/)
- [GitHub releases](https://github.com/ardavanshamroshan/pydd/releases)
- [pydump upgrade guide](https://ardavanshamroshan.github.io/pydump/en/upgrade/)
