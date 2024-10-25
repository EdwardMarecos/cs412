## mini_fb/urls.py
## description: url patterns for the mini_fb app

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ShowAllView, ShowProfilePage, CreateProfileView, CreateStatusMessageView, UpdateProfileView, UpdateStatusMessageView, DeleteStatusMessageView, CreateFriendView

# all of urls part of this app
urlpatterns = [
    path ('', ShowAllView.as_view(), name='base'),
    path ('profile/<int:pk>/', ShowProfilePage.as_view(), name="show_profile"),
    path ('create_profile/', CreateProfileView.as_view(), name="create_profile"),
    path ('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
    path ('profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile'),
    path ('profile/<int:profile_pk>/status/<int:pk>/update/', UpdateStatusMessageView.as_view(), name='update_status'),
    path ('profile/<int:profile_pk>/status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='remove_status'),
    path ('profile/<int:pk>/add_friend/<int:other_pk>/', CreateFriendView.as_view(), name='add_friend'),
]