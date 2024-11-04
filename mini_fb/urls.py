## mini_fb/urls.py
## description: url patterns for the mini_fb app

from django.urls import path
from django.contrib.auth import views as auth_views #django auth view
from django.conf import settings
from django.conf.urls.static import static
from .views import (ShowAllView, ShowProfilePage, CreateProfileView, 
                    CreateStatusMessageView, UpdateProfileView, 
                    UpdateStatusMessageView, DeleteStatusMessageView, 
                    CreateFriendView, ShowFriendSuggestionsView, ShowNewsFeedView,)

# all of urls part of this app

urlpatterns = [
    path('', ShowAllView.as_view(), name='base'),
    path('profile/<int:pk>', ShowProfilePage.as_view(), name="show_profile"),
    path('create_profile/', CreateProfileView.as_view(), name="create_profile"),
    path('profile/status/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/status/<int:pk>/update/', UpdateStatusMessageView.as_view(), name='update_status'),
    path('profile/status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='remove_status'),
    path('profile/add_friend/<int:other_pk>/', CreateFriendView.as_view(), name='add_friend'),
    path('profile/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'),
]