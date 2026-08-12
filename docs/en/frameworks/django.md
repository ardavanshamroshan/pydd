# Django

Django uses **`PyddMiddleware`** in your `MIDDLEWARE` setting. Boot mode is not available yet.

## Install and run

```bash
pip install "pydd-web[django]"
python manage.py migrate
python manage.py runserver
```

## Settings

```python
# config/settings.py
from pathlib import Path
from pydd import configure

BASE_DIR = Path(__file__).resolve().parent.parent
configure(project_root=BASE_DIR)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # ... your other middleware ...
    "pydd.integrations.django.PyddMiddleware",
]
```

Place `PyddMiddleware` near the end of the stack (after session/auth if you want request context populated).

## Views

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

## URLs

```python
# debugapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("dd/", views.debug_dump),
]
```

Visit `/dd/` to trigger the HTML dump.

## What the middleware does

`PyddMiddleware.__call__`:

1. Sets the in-request flag
2. Calls `get_response(request)`
3. Catches `DdException` → `HttpResponse(html, status=500)`
4. Resets the flag in `finally`

`process_exception` is kept for compatibility with older Django patterns.

## Laravel-style globals

```python
# settings.py or wsgi.py
import pydd

# in any view
dd(request.session)
```

## Links

- [Getting started](../getting-started.md)
- [Demo](../demo.md)
- [PyPI — pydd-web](https://pypi.org/project/pydd-web/)
- [GitHub — pydd](https://github.com/ardavanshamroshan/pydd)
