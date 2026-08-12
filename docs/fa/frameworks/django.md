# Django

Django از **`PyddMiddleware`** در `MIDDLEWARE` استفاده می‌کند. boot mode هنوز نیست.

## نصب و اجرا

```bash
pip install "pydd-web[django]"
python manage.py migrate
python manage.py runserver
```

## تنظیمات

```python
# config/settings.py
from pathlib import Path
from pydd import configure

BASE_DIR = Path(__file__).resolve().parent.parent
configure(project_root=BASE_DIR)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # ... middlewareهای دیگر ...
    "pydd.integrations.django.PyddMiddleware",
]
```

`PyddMiddleware` را نزدیک انتهای لیست بگذارید.

## Viewها

```python
# debugapp/views.py
from django.http import HttpResponse
from pydd import dd

def home(request):
    return HttpResponse('<a href="/dd/">/dd/</a>')

def debug_dump(request):
    dd({
        "title": "Django dd test",
        "query": dict(request.GET),
        "user": str(request.user),
    })
```

## URLها

```python
# debugapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("dd/", views.debug_dump),
]
```

`/dd/` را باز کنید.

## middleware چه می‌کند

`PyddMiddleware.__call__`:

1. پرچم in-request
2. `get_response(request)`
3. `DdException` → `HttpResponse(html, status=500)`
4. reset در `finally`

`process_exception` برای سازگاری با الگوهای قدیمی Django مانده.

## globals شبیه Laravel

```python
# settings.py یا wsgi.py
import pydd

# در هر view
dd(request.session)
```

## لینک‌ها

- [شروع سریع](../getting-started.md)
- [دمو](../demo.md)
- [PyPI — pydd-web](https://pypi.org/project/pydd-web/)
- [GitHub — pydd](https://github.com/ardavanshamroshan/pydd)
