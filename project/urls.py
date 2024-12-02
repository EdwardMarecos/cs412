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

    # categories
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/add/', AddCategoryView.as_view(), name='add-category'),

    # subject and topic
    path('categories/<int:category_id>/add-subject/', SubjectCreateView.as_view(), name='add-subject'),
    path('categories/<int:category_id>/add-topic/', TopicCreateView.as_view(), name='add-topic'),

    path('add-topic/', TopicCreateFromNoteView.as_view(), name='add-topic-from-note'),

    # notes
    path('notes/', NoteListView.as_view(), name='note-list'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
    path('note/create/', CreateNoteView.as_view(), name='create-note'),
    path('notes/<int:pk>/delete/', NoteDeleteView.as_view(), name='note-delete'),
    path('notes/<int:pk>/update/', NoteUpdateView.as_view(), name='note-update'),

    # user to user interaction on notes
    path('notes/<int:pk>/toggle-like/', ToggleLikeView.as_view(), name='toggle-like'),
    path('notes/<int:pk>/toggle-bookmark/', ToggleBookmarkView.as_view(), name='toggle-bookmark'),

    # comments (still user interaction but a bit more complicated)
    path('notes/<int:pk>/comments/add/', CommentCreateView.as_view(), name='add-comment'),
    path('comments/<int:pk>/edit/', CommentEditView.as_view(), name='edit-comment'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete-comment'),

    # profile
    path('profile/create/', CreateProfileView.as_view(), name='create-profile'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/update/', ProfileUpdateView.as_view(), name='update-profile'),

    # follow / followers
    path('profile/<int:pk>/followers/', FollowersListView.as_view(), name='followers-list'),
    path('profile/<int:pk>/following/', FollowingListView.as_view(), name='following-list'),
    path('profile/<int:pk>/follow/', FollowProfileView.as_view(), name='follow-profile'),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'),
]