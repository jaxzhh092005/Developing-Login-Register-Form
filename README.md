# Setup

pip install django pillow
django-admin startproject config .
python manage.py startapp accounts        # or copy this accounts/ folder over the generated one

## config/settings.py
INSTALLED_APPS += ["accounts"]
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"

## config/urls.py
from django.urls import include, path
urlpatterns = [path("admin/", admin.site.urls), path("", include("accounts.urls"))]

## Image
Put your pebble photo at accounts/static/accounts/img/pebbles.jpg

## Run
python manage.py makemigrations accounts
python manage.py migrate
python manage.py runserver   # open /register/
