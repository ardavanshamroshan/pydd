# نصب

## نام بسته‌ها

| مورد | توزیع PyPI | Import |
|------|------------|--------|
| دامپ وب (این بسته) | **`pydd-web`** | `import pydd` |
| هسته ترمینال (وابستگی) | **`pydump-dd`** | `import pydump` |

با نصب `pydd-web`، `pydump-dd` خودکار نصب می‌شود.

## نصب پایه

```bash
pip install pydd-web
```

## extraهای فریم‌ورک

```bash
pip install "pydd-web[fastapi]"
pip install "pydd-web[flask]"
pip install "pydd-web[django]"
pip install "pydd-web[all]"
```

| Extra | اضافه می‌کند |
|-------|-------------|
| `fastapi` | FastAPI >= 0.100 |
| `flask` | Flask >= 2.3 |
| `django` | Django >= 4.2 |
| `all` | هر سه فریم‌ورک |
| `dev` | pytest، httpx، fastapi[standard] (فقط توسعه) |

## pip + محیط مجازی

```bash
cd myapp
python -m venv .venv
source .venv/bin/activate        # ویندوز: .venv\Scripts\activate
pip install pydd-web
```

## uv

```bash
cd myapp
uv add pydd-web
# یا با extra
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

اجرا:

```bash
uv run uvicorn main:app --reload
```

## فقط ترمینال (بدون وب)

اگر فقط دامپ CLI/اسکریپت می‌خواهید، pydump را مستقیم نصب کنید:

```bash
pip install pydump-dd
```

[مستندات pydump](https://ardavanshamroshan.github.io/pydump/).

## نصب برای توسعه

```bash
git clone https://github.com/ardavanshamroshan/pydd.git
cd pydd
pip install -e ".[dev]"
# یا
uv sync --extra dev
uv run pytest -q
```

## نیازمندی‌ها

- **پایتون** >= 3.10
- **وابستگی runtime:** `pydump-dd>=0.2.4`
- بسته‌های فریم‌ورک اختیاری‌اند مگر آن integration را استفاده کنید

## تأیید نصب

```bash
python -c "import pydd; print(pydd.__version__)"
```

خروجی مورد انتظار: `0.2.4` (یا نسخهٔ نصب‌شده).

## لینک‌ها

- **PyPI:** [pypi.org/project/pydd-web](https://pypi.org/project/pydd-web/)
- **GitHub:** [github.com/ardavanshamroshan/pydd](https://github.com/ardavanshamroshan/pydd)
- **Issues:** [github.com/ardavanshamroshan/pydd/issues](https://github.com/ardavanshamroshan/pydd/issues)
