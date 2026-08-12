# راهنمای ارتقا

ارتقای امن **pydd-web** و وابستگی **pydump-dd**.

## نسخه فعلی

**0.2.4** — PyPI: [pydd-web](https://pypi.org/project/pydd-web/)

## ارتقای سریع

```bash
pip install -U pydd-web
```

با uv:

```bash
uv add "pydd-web>=0.2.4"
```

## تغییر نام PyPI (0.2.2)

| قبل | بعد |
|-----|-----|
| `pip install pydd` (نام قدیم) | **`pip install pydd-web`** |
| path محلی pydump | **`pydump-dd` از PyPI** |

**Import عوض نشده:** `import pydd`

```diff
- pydd>=0.2.1
+ pydd-web>=0.2.4
```

pydump خودکار نصب می‌شود.

## 0.2.3 → 0.2.4

- سایت مستندات + URLهای PyPI
- نیاز: `pydump-dd>=0.2.4`
- بدون تغییر کد

## 0.2.2 → 0.2.3

- مستندات نصب PyPI
- نیاز: `pydump-dd>=0.2.3`

بدون تغییر کد.

## 0.2.1 → 0.2.2

### اضافه
- tipهای HTML: `$variable · kind · type`
- فایل LICENSE MIT

### تغییر
- نام توزیع: **`pydd-web`**
- وابستگی: **`pydump-dd>=0.2.2`**

### اقدام

```bash
pip uninstall pydd pydd-web 2>/dev/null; pip install pydd-web
```

## 0.2.0 → 0.2.1

### اضافه
- builtins شبیه Laravel
- `install_helpers()`

### رفع
- boot دیگر مرورگر باز نمی‌کند
- `dd(var)` بیرون درخواست دیگر `last_app()` نمی‌گیرد
- جداسازی بصری چند دامپ HTML
- tipها در HTML و ترمینال

### اقدام
در boot mode تب را دستی refresh کنید.

## 0.1.0 → 0.2.x

1. `pip install pydd-web`
2. `import pydd` در entrypoint FastAPI (یا Flask/Django)
3. `print()` دیباگ → `dd()`

## pin نسخه

در production از `dd()` استفاده نکنید. برای dev:

```toml
"pydd-web>=0.2.4,<0.3"
```

## عیب‌یابی

| مشکل | راه‌حل |
|------|--------|
| `ModuleNotFoundError: pydd` | **`pydd-web`** نصب کنید |
| tip به `pydd/api.py` | ارتقا به >= 0.2.1 |
| دامپ HTML ادغام | >= 0.2.1 |
| بدون `$variable` در tip | pydump >= 0.2.2 |

## لینک‌ها

- [تغییرات](changelog.md)
- [PyPI — pydd-web](https://pypi.org/project/pydd-web/)
- [Releaseهای GitHub](https://github.com/ardavanshamroshan/pydd/releases)
- [راهنمای ارتقای pydump](https://ardavanshamroshan.github.io/pydump/fa/upgrade/)
