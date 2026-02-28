# DjangoPolls: Example app using Django

# Part 1: Writing your first Django app

## Setup django using `uv`

```sh
uv init [project-name]
cd [project-name]
uv add django
```

## Creating a project

```sh
uv run django-admin startproject [project-name]
# The project name for startproject can be anything, i've using my initial name
# Make sure to replace hypens with underscores, e.g.: django-polls -> django_polls
```

## Dev server

```sh
uv run manage.py runserver
# Don’t use this server in anything resembling a production environment
```

## Creating apps

**Projects vs. apps**: Project is a collection of configurations and apps. Apps are invidual systems
that do something - e.g. cms for a blog, simple polls app with voting, project management app with tickets.

```sh
uv run manage.py startapp [app-name]
# startproject is used to setup the configuration of the whole systems
# startapp creates a bolierplate for invidual apps
```

## Creating views

First we create a view, which is a Python function that gets a `request` and returns a `response`.

```py
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

To access this view, we need to map it to a url like `/polls/` in `/[app-name]/urls.py`:

```py
urlpatterns = [
    path("", views.index, name="index"),
]
```

We just configured the path to our view, we also need to make sure that our project recognizes our
app urls in `/[project-name]/urls.py`:

```py
from django.urls import include, path

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
]
```

After this, every time we add a new url to our polls app, it will be accessible under `/polls/`, for
example:

```py
from . import views
# or invidual: from view import index, detail, results
# 
urlpatterns = [
    path("", views.index, name="index"), # -> /polls/
    path("/<int:id>", views.detail, name="detail"), # -> /polls/1
    path("/<int:id>/results", views.results, name="results"), # -> /polls/1/results
]
```
