# امکانات

## قابلیت‌های اصلی

- **دو حالت، یک API** — دامپ HTML در درخواست HTTP؛ دامپ ترمینال در بقیه جاها
- **helperهای شبیه Laravel** — یک‌بار `import pydd`، بعد `dd` / `dump` به‌صورت builtin در کل پروژه
- **HTML تعاملی** — تم تیره شبیه Symfony با باز/بسته کردن ساختارهای تو در تو
- **هسته inspection مشترک** — همان درخت `DumpNode` مثل [pydump](https://pypi.org/project/pydump-dd/)
- **tip محل فراخوانی** — `$variable · kind · type` و `// file:line` در HTML و ترمینال
- **چند مقدار** — آرگومان positional و keyword؛ هر کدام بلوک دامپ جدا
- **FastAPI بدون تنظیم** — middleware و handler با `import pydd`
- **Flask / Django صریح** — `install_flask(app)` و `PyddMiddleware`
- **Boot mode (FastAPI)** — `dd(app)` HTML را روی هر درخواست آماده می‌کند؛ سرور زنده می‌ماند
- **شامل pydump** — دیباگ ترمینال بدون وابستگی دوم

## جدول رفتار

| فراخوانی | در HTTP | CLI / اسکریپت | boot با `dd(app)` |
|----------|---------|---------------|-------------------|
| `dd(x)` | HTML 500 | stderr + خروج 1 | آماده HTML (refresh) |
| `dump(x)` | فقط stderr | فقط stderr | فقط stderr |
| `render_html(x)` | رشته | رشته | رشته |
| `render_text(x)` | رشته | رشته | رشته |

## یکپارچه‌سازی فریم‌ورک

### FastAPI

- patch خودکار `FastAPI.__init__` برای middleware و handler مربوط به `DdException`
- پرچم محدود به درخواست با `ContextVar` (سازگار با async)
- Boot mode قبل از routeها HTML آماده‌شده را برمی‌گرداند
- جایگزین دستی: `install_fastapi(app)` بدون side effect import

### Flask

- `before_request` / `teardown_request` برای تشخیص درخواست
- error handler برای `DdException` با `(html, 500)`
- هنوز boot mode ندارد

### Django

- `PyddMiddleware` context را در `__call__` تنظیم می‌کند
- `DdException` را می‌گیرد و `HttpResponse(status=500)` برمی‌گرداند
- نیاز به middleware در `settings.py`

## امکانات دامپ HTML

- باز/بسته کردن containerهای تو در تو (کلیک روی `▶` یا header)
- بلوک `<pre class="sf-dump">` جدا برای چند مقدار
- tip روی header وقتی بسته: `[▶] // file:line`
- tip بعد از `[▼` وقتی باز است
- عمق پیش‌فرض بسته: `max_depth=1` در مرورگر (ترمینال کامل باز می‌شود)

## fallback ترمینال

وقتی در HTTP نیستید و app FastAPI به `dd()` داده نشده:

- فرمت ANSI pydump روی stderr
- فریم‌های داخلی pydd در tip رد می‌شوند
- `dd()` بعد از چاپ `SystemExit(1)` می‌دهد

## پیکربندی

- `configure(project_root=Path(...))` — مسیر نسبی در tipهای `//`
- URL boot از env: `HOST`, `PORT`, `UVICORN_HOST`, `UVICORN_PORT`

## pydd چه نیست

!!! warning "فقط برای توسعه"
    - **برای production نیست** — درخواست را با 500 متوقف می‌کند
    - **Boot mode همه routeها را می‌گیرد** تا restart
    - **در ترمینال collapse HTML نیست** — برای درخت کامل `render_text`
    - **introspection محدود** — همان قوانین pydump (فقط attributeهای public)

## بسته‌های مرتبط

| بسته | PyPI | مستندات |
|------|------|---------|
| pydd | [pydd-web](https://pypi.org/project/pydd-web/) | همین‌جا |
| pydump | [pydump-dd](https://pypi.org/project/pydump-dd/) | [مستندات pydump](https://ardavanshamroshan.github.io/pydump/) |
