## quotes/urls.py
## description: url patterns for the quotes app

from django.urls import path
from django.conf import settings
from . import views

# all of urls part of this app
urlpatterns = [
    path ('', views.quote, name='quote'),
    path ('quote/', views.quote, name="quote"),
    path ('show_all/', views.show_all, name="show_all"),
    path ('about/', views.about, name="about"),
]