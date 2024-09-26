## restaurant/urls.py
## description: url patterns for the restaurant app

from django.urls import path
from django.conf import settings
from . import views

# all of urls part of this app
urlpatterns = [
    path ('', views.main, name='main'),
    path ('main/', views.main, name="main"),
    path ('order/', views.order, name="order"),
    path ('confirmation/', views.confirmation, name="confirmation"),
]