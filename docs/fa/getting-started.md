# شروع سریع

این راهنما شما را در کمتر از پنج دقیقه به یک دامپ HTML در FastAPI می‌رساند.

## پیش‌نیاز

- پایتون **۳.۱۰+**
- یک فریم‌ورک وب (FastAPI، Flask یا Django)

## ۱. نصب

```bash
pip install pydd-web
```

برای FastAPI با وابستگی‌های سرور:

```bash
pip install "pydd-web[fastapi]"
```

راهنمای کامل [نصب](installation.md) برای pip، uv و extraهای فریم‌ورک.

## ۲. اپ حداقلی FastAPI

فایل `main.py`:

```python
from pathlib import Path
from fastapi import FastAPI
from pydd import configure, dd

configure(project_root=Path(__file__).resolve().parent)

app = FastAPI()

@app.get("/debug")
def debug_route():
    user = {"id": 1, "name": "Ada", "roles": ["admin", "editor"]}
    dd(user)
```

## ۳. اجرای سرور

```bash
uvicorn main:app --reload
```

## ۴. فراخوانی دامپ

در مرورگر [http://127.0.0.1:8000/debug](http://127.0.0.1:8000/debug) را باز کنید.

باید ببینید:

- وضعیت HTTP **500** (عادی است — `dd()` درخواست را متوقف می‌کند)
- **دامپ HTML تعاملی** با تم تیره و باز/بسته کردن دادهٔ تو در تو
- خط tip مثل `// main.py:14 · user · container · dict`

## ۵. globals شبیه Laravel (اختیاری)

به‌جای `from pydd import dd` می‌توانید از builtins استفاده کنید:

```python
import pydd  # یک‌بار، مثلاً در main.py

# در هر ماژول دیگر — بدون import
dd(some_value)
```

!!! note "ویرایشگر / linter"
    Ruff و type checkerها builtins تزریق‌شده را نمی‌بینند. `[tool.ruff] builtins = ["dd", "dump"]` اضافه کنید یا import صریح. [مرجع API — تنظیم ویرایشگر](api.md#editor-and-linter).

## گام بعد

- [راهنمای FastAPI](frameworks/fastapi.md) — boot mode، تأیید، TestClient
- [راهنمای Flask](frameworks/flask.md) — `install_flask(app)`
- [راهنمای Django](frameworks/django.md) — middleware
- [دمو](demo.md) — مثال‌های آماده برای همه فریم‌ورک‌ها
- [امکانات](features.md) — فهرست کامل قابلیت‌ها

## لینک‌ها

| منبع | آدرس |
|------|------|
| PyPI | [pypi.org/project/pydd-web](https://pypi.org/project/pydd-web/) |
| GitHub | [github.com/ardavanshamroshan/pydd](https://github.com/ardavanshamroshan/pydd) |
| مستندات pydump | [ardavanshamroshan.github.io/pydump](https://ardavanshamroshan.github.io/pydump/) |
