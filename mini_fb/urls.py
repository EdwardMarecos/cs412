## mini_fb/urls.py
## description: url patterns for the mini_fb app

from django.urls import path
from django.conf import settings
from . import views
from .views import ShowAllView, ShowProfilePage

# all of urls part of this app
urlpatterns = [
    path ('', ShowAllView.as_view(), name='base'),
    path ('profile/<int:pk>', ShowProfilePage.as_view(), name="show_profile"),
    # path ('order/', views.order, name="order"),
    # path ('confirmation/', views.confirmation, name="confirmation"),
]