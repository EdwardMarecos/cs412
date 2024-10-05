## mini_fb/urls.py
## description: url patterns for the mini_fb app

from django.urls import path
from django.conf import settings
from . import views
from .views import ShowAllView

# all of urls part of this app
urlpatterns = [
    path ('', ShowAllView.as_view(), name='base'),
    # path ('main/', views.main, name="main"),
    # path ('order/', views.order, name="order"),
    # path ('confirmation/', views.confirmation, name="confirmation"),
]