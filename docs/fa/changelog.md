# تغییرات

تغییرات مهم **pydd-web** اینجا ثبت می‌شود.

## [0.2.4] - 2026-08-12

### اضافه
- سایت مستندات دوزبانه (انگلیسی + فارسی) روی GitHub Pages

### تغییر
- URLهای Homepage / Documentation در PyPI
- لینک‌های README
- نیاز: `pydump-dd>=0.2.4`

## [0.2.3] - 2026-08-12

### رفع
- مستندات نصب: PyPI `pydd-web` و `pydump-dd` به‌جای path محلی
- نیاز: `pydump-dd>=0.2.3`

## [0.2.2] - 2026-08-12

### اضافه
- tipهای HTML: `$variable · kind · type`
- فایل MIT `LICENSE`

### تغییر
- نام PyPI: **`pydd-web`** (`import pydd` بدون تغییر)
- وابستگی **`pydump-dd>=0.2.2`** از PyPI

## [0.2.1] - 2026-07-23

### اضافه
- helperهای global شبیه Laravel
- `install_helpers()`

### رفع
- boot دیگر مرورگر باز نمی‌کند
- `dd(var)` بیرون درخواست دیگر via `last_app()` hijack نمی‌شود
- جداسازی بصری چند دامپ HTML
- tipهای `// file:line` در HTML
- tip ترمینال دیگر `pydd/api.py` نیست

### تغییر
- مستندات Ruff / IDE برای builtins

## [0.2.0] - 2026-07-23

### یادداشت
- tag `v0.2.0`؛ ترجیح `v0.2.1`

## [0.1.0] - 2026-07-22

### اضافه
- انتشار اول: HTML `dd` برای FastAPI / Flask / Django روی pydump

---

[0.2.4]: https://github.com/ardavanshamroshan/pydd/releases/tag/v0.2.4
[0.2.3]: https://github.com/ardavanshamroshan/pydd/releases/tag/v0.2.3
[0.2.2]: https://github.com/ardavanshamroshan/pydd/releases/tag/v0.2.2
[0.2.1]: https://github.com/ardavanshamroshan/pydd/releases/tag/v0.2.1

همچنین: [راهنمای ارتقا](upgrade.md) · [PyPI](https://pypi.org/project/pydd-web/) · [GitHub](https://github.com/ardavanshamroshan/pydd)
