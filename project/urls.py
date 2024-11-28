## project/urls.py
## description: url patterns for the project app

from django.urls import path
from django.contrib.auth import views as auth_views #django auth view
from django.conf import settings
from django.conf.urls.static import static
from .views import *

# all of urls part of this app

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Home screen

    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('notes/', NoteListView.as_view(), name='note-list'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
    path('note/create/', CreateNoteView.as_view(), name='create-note'),

    path('profile/create/', CreateProfileView.as_view(), name='create-profile'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/update/', ProfileUpdateView.as_view(), name='update-profile'),

    # path('', ShowAllView.as_view(), name='base'),
    # path('profile/<int:pk>', ShowProfilePage.as_view(), name="show_profile"),
    # path('create_profile/', CreateProfileView.as_view(), name="create_profile"),
    # path('profile/status/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
    # path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    # path('profile/status/<int:pk>/update/', UpdateStatusMessageView.as_view(), name='update_status'),
    # path('profile/status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='remove_status'),
    # path('profile/add_friend/<int:other_pk>/', CreateFriendView.as_view(), name='add_friend'),
    # path('profile/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    # path('profile/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'),
]