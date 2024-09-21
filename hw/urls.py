## hw/urls.py
## description: url patterns for the hw app

from django.urls import path
from django.conf import settings
from . import views

# all of urls part of this app
urlpatterns = [
    path (r'', views.home, name="home"),
]