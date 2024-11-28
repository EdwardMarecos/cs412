from django.http import *
from django.shortcuts import *
from django.views.generic import *
from .models import *

from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .forms import *

# display main pages

class HomeView(TemplateView):
    template_name = 'project/home.html'


# relevant views for categories
class CategoryListView(ListView):
    model = Category
    template_name = 'project/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'project/category_detail.html'

class NoteListView(ListView):
    model = Note
    template_name = 'project/note_list.html'
    context_object_name = 'notes'
    paginate_by = 50

    def get_queryset(self):
        queryset = Note.objects.all()

        # Filters
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(topic__parent_subject__category_id=category_id)

        subject_id = self.request.GET.get('subject')
        if subject_id:
            queryset = queryset.filter(topic__parent_subject_id=subject_id)

        topic_id = self.request.GET.get('topic')
        if topic_id:
            queryset = queryset.filter(topic_id=topic_id)

        author_username = self.request.GET.get('author')
        if author_username:
            queryset = queryset.filter(author__user__username__icontains=author_username)

        # Sorting
        sort_by = self.request.GET.get('sort', 'upload_date')
        return queryset.order_by(sort_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['subjects'] = Subject.objects.all()
        context['topics'] = Topic.objects.all()
        context['get_params'] = self.request.GET.copy()

        # Ensure 'author' is always set, even if missing
        if 'author' not in context['get_params']:
            context['get_params']['author'] = ''
        
        return context

class NoteDetailView(DetailView):
    model = Note
    template_name = 'project/note_detail.html'

class CreateNoteView(CreateView):
    model = Note
    form_class = CreateNoteForm
    template_name = 'project/create_note_form.html'

    def form_valid(self, form):
        # Set the author to the logged-in user's profile
        form.instance.author = self.request.user.project_profile
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the detail page of the created note
        return reverse_lazy('note-detail', kwargs={'pk': self.object.pk})

# profile creation / display / update views

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'project/create_profile_form.html'
    success_url = reverse_lazy('home')  # Redirect to the home page upon success

    def form_valid(self, form):
        # Link the profile to the logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'project/profile_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch notes related to this profile, ordered by most recent
        context['notes'] = Note.objects.filter(author=self.object).order_by('-upload_date')
        return context

class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'project/update_profile_form.html'

    def get_success_url(self):
        # Redirect to the profile-detail page of the updated profile
        return reverse('profile-detail', kwargs={'pk': self.object.id})

    def get_object(self, queryset=None):
        # Ensure the user can only update their own profile
        return self.request.user.project_profile