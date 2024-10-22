## mini_fb/urls.py
## description: url patterns for the mini_fb app

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ShowAllView, ShowProfilePage, CreateProfileView, CreateStatusMessageView

# all of urls part of this app
urlpatterns = [
    path ('', ShowAllView.as_view(), name='base'),
    path ('profile/<int:pk>', ShowProfilePage.as_view(), name="show_profile"),
    path ('create_profile', CreateProfileView.as_view(), name="create_profile"),
    path ('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)