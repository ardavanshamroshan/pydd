# Installation

## Package names

| What | PyPI distribution | Import |
|------|-------------------|--------|
| Web dumps (this package) | **`pydd-web`** | `import pydd` |
| Terminal core (dependency) | **`pydump-dd`** | `import pydump` |

Installing `pydd-web` automatically pulls in `pydump-dd`.

## Basic install

```bash
pip install pydd-web
```

## Framework extras

```bash
pip install "pydd-web[fastapi]"
pip install "pydd-web[flask]"
pip install "pydd-web[django]"
pip install "pydd-web[all]"
```

| Extra | Adds |
|-------|------|
| `fastapi` | FastAPI >= 0.100 |
| `flask` | Flask >= 2.3 |
| `django` | Django >= 4.2 |
| `all` | All three frameworks |
| `dev` | pytest, httpx, fastapi[standard] (development only) |

## pip + virtual environment

```bash
cd myapp
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install pydd-web
```

## uv

```bash
cd myapp
uv add pydd-web
# or with extra
uv add "pydd-web[fastapi]"
```

`pyproject.toml`:

```toml
[project]
dependencies = [
    "fastapi[standard]",
    "pydd-web>=0.2.4",
]
```

Run:

```bash
uv run uvicorn main:app --reload
```

## Terminal-only (no web)

If you only need CLI/script dumps, install pydump directly — no pydd required:

```bash
pip install pydump-dd
```

See [pydump documentation](https://ardavanshamroshan.github.io/pydump/).

## Development install

Clone and install in editable mode:

```bash
git clone https://github.com/ardavanshamroshan/pydd.git
cd pydd
pip install -e ".[dev]"
# or
uv sync --extra dev
uv run pytest -q
```

## Requirements

- **Python** >= 3.10
- **Runtime dependency:** `pydump-dd>=0.2.4`
- Framework packages are optional unless you use that integration

## Verify installation

```bash
python -c "import pydd; print(pydd.__version__)"
```

Expected output: `0.2.4` (or your installed version).

## Links

- **PyPI:** [pypi.org/project/pydd-web](https://pypi.org/project/pydd-web/)
- **GitHub:** [github.com/ardavanshamroshan/pydd](https://github.com/ardavanshamroshan/pydd)
- **Issues:** [github.com/ardavanshamroshan/pydd/issues](https://github.com/ardavanshamroshan/pydd/issues)
