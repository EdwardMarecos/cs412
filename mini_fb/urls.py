## mini_fb/urls.py
## description: url patterns for the mini_fb app

from django.urls import path
from django.contrib.auth import views as auth_views #django auth view
from django.conf import settings
from django.conf.urls.static import static
from mini_fb.views import custom_access_denied_view
from .views import (ShowAllView, ShowProfilePage, CreateProfileView, 
                    CreateStatusMessageView, UpdateProfileView, 
                    UpdateStatusMessageView, DeleteStatusMessageView, 
                    CreateFriendView, ShowFriendSuggestionsView, ShowNewsFeedView,)

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
    path ('profile/<int:pk>/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path ('profile/<int:pk>/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='base'), name='logout'),
    path('access_denied/', custom_access_denied_view, name='access_denied'),

]
handler403 = 'mini_fb.views.custom_permission_denied_view'
