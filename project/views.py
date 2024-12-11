# File: views.py
# Author: Edward Marecos (emarecos@bu.edu), 12/1/2024
# Description: Contains all the view classes for the project app. These classes handle the logic for displaying pages, processing forms, and managing interactions like likes, bookmarks, comments, and profile views.

from django.http import *  # Importing all HTTP-related utilities from Django
from django.shortcuts import *  # Importing all shortcut utilities from Django
from django.views.generic import *  # Importing generic views from Django
from .models import *  # Importing all models from the local app

from django.contrib.auth import login  # Used to log in the user after successful registration
from django.utils import timezone  # Used for handling date and time-related operations
from django.urls import reverse, reverse_lazy  # Used to reverse-resolve URLs dynamically
from django.contrib.auth.mixins import LoginRequiredMixin  # Ensures users are logged in for certain views
from django.contrib.auth.forms import UserCreationForm  # Built-in user registration form from Django
from .forms import *  # Importing all custom forms from the my app

# display main page

class HomeView(TemplateView):
    """Display the main page of the app."""
    template_name = 'project/home.html'

    def get_context_data(self, **kwargs):
        """Return context data for the home view, including top notes and suggested users to follow."""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            current_profile = self.request.user.project_profile  # Profile of the current logged-in user
            context['notes'] = Note.objects.order_by('-like_count')[:10]  # Top 10 notes ordered by likes
            all_users = Profile.objects.exclude(user=self.request.user)  # All profiles except the current user's profile

            for user in all_users:
                # Check if the current user follows this user
                user.is_followed = current_profile.following.filter(id=user.id).exists()

            context['users'] = all_users  # Add the list of users to context
            context['categories'] = Category.objects.all()  # Add all categories to context
        return context


# relevant views for categories
class CategoryListView(ListView):
    """Display a list of all categories."""
    model = Category
    template_name = 'project/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    """Display details for a specific category, including its subjects and notes."""
    model = Category
    template_name = 'project/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        """Return context data for the category detail view."""
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        # All subjects related to this category
        subjects = Subject.objects.filter(category=category)
        context['subjects'] = subjects
        # All notes under this category
        context['all_notes'] = Note.objects.filter(topic__parent_subject__category=category)
        # Notes grouped by subject
        context['notes_by_subject'] = {
            subject: Note.objects.filter(topic__parent_subject=subject) for subject in subjects
        }
        return context

class AddCategoryView(LoginRequiredMixin, CreateView):
    """View to create a new category. Restricted to logged-in users."""
    model = Category
    fields = ['name', 'graphic']     # Fields required to create a category
    template_name = 'project/add_category_form.html'
    success_url = reverse_lazy('category-list')  # Redirect to the category list after adding a category

    def form_valid(self, form):
        return super().form_valid(form)

    
# subjects
class SubjectCreateView(LoginRequiredMixin, CreateView):
    """View to create a new subject within a specific category."""
    model = Subject
    fields = ['name']
    template_name = 'project/add_subject_form.html'

    def form_valid(self, form):
        """Set the category for the subject based on the URL parameter."""
        category = get_object_or_404(Category, id=self.kwargs['category_id'])
        form.instance.category = category
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the detail page for the associated category."""
        return reverse_lazy('category-detail', kwargs={'pk': self.kwargs['category_id']})
    
class SubjectListView(ListView):
    """Display a list of subjects."""
    model = Subject
    template_name = 'project/subject_list.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return Subject.objects.filter(category=category)
    
# topics
class TopicCreateView(LoginRequiredMixin, CreateView):
    """ create a topic """
    model = Topic
    fields = ['title', 'parent_subject']
    template_name = 'project/add_topic_form.html'

    def form_valid(self, form):
        category = get_object_or_404(Category, id=self.kwargs['category_id'])
        # Ensure the selected subject belongs to the category
        if form.instance.parent_subject.category != category:
            return HttpResponseForbidden("Invalid parent subject for this category.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('category-detail', kwargs={'pk': self.kwargs['category_id']})

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        category = get_object_or_404(Category, id=self.kwargs['category_id'])
        form.fields['parent_subject'].queryset = Subject.objects.filter(category=category)
        return form
    
class TopicCreateFromNoteView(LoginRequiredMixin, CreateView):
    model = Topic
    fields = ['title', 'parent_subject']
    template_name = 'project/add_topic_form_from_note.html'

    def form_valid(self, form):
        # Ensure the selected subject is valid
        if not form.instance.parent_subject:
            return HttpResponseBadRequest("A valid subject must be selected.")
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to a page of your choice after successfully creating the topic
        return reverse_lazy('home')  # Adjust as needed

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # Filter subjects to include only valid options
        form.fields['parent_subject'].queryset = Subject.objects.all()
        return form

# note views
class NoteListView(ListView):
    """Display a list of notes, supporting filtering and sorting options."""
    model = Note
    template_name = 'project/note_list.html'
    context_object_name = 'notes'
    paginate_by = 50

    def get_queryset(self):
        """Return the queryset for the list of notes, applying filters from query parameters."""
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
        """Return context data, including categories, subjects, and topics for filtering options."""
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
    """Display the detail page for a single note, including its comments."""
    model = Note
    template_name = 'project/note_detail.html'

    def get_context_data(self, **kwargs):
        """Return context data for the note detail view, including comments and the comment form."""
        context = super().get_context_data(**kwargs)
        note = self.get_object()
        context['comments'] = Comment.objects.filter(note=note).order_by('-date')
        context['comment_form'] = CommentForm()
        return context

class CreateNoteView(CreateView):
    """View to create a new note. Users must be logged in to access this view."""
    model = Note
    form_class = CreateNoteForm
    template_name = 'project/create_note_form.html'

    def form_valid(self, form):
        """Set the author of the note to the currently logged-in user."""
        form.instance.author = self.request.user.project_profile
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the detail page of the created note after successful creation."""
        return reverse_lazy('note-detail', kwargs={'pk': self.object.pk})

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    """View to update an existing note. Users can only update notes they authored."""
    model = Note
    form_class = CreateNoteForm  # Reuse your existing form
    template_name = 'project/update_note_form.html'

    def get_queryset(self):
        """Restrict updates to notes authored by the current user."""
        return Note.objects.filter(author=self.request.user.project_profile)

    def get_success_url(self):
        """Redirect to the note detail page after successful update."""
        return reverse('note-detail', kwargs={'pk': self.object.pk})


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    """View to delete an existing note. Only the author of the note can delete it."""
    model = Note
    template_name = 'project/note_confirm_delete.html'
    context_object_name = 'note'

    def get_queryset(self):
        """Restrict deletion to notes authored by the current user."""
        return Note.objects.filter(author=self.request.user.project_profile)

    def get_success_url(self):
        """Redirect to the note list after successful deletion."""
        return reverse('note-list')


# toggle likes / bookmarks

class ToggleLikeView(LoginRequiredMixin, View):
    """View to toggle the like status of a note. Users can like or unlike a note."""
    def post(self, request, pk, *args, **kwargs):
        note = get_object_or_404(Note, pk=pk)
        profile = request.user.project_profile

        if profile in note.liked_by.all():
            note.unlike(profile)
        else:
            note.like(profile)

        return redirect('note-detail', pk=note.pk)
    
class ToggleBookmarkView(LoginRequiredMixin, View):
    """View to toggle the bookmark status of a note. Users can bookmark or remove a bookmark."""
    def post(self, request, pk, *args, **kwargs):
        note = get_object_or_404(Note, pk=pk)
        profile = request.user.project_profile

        if profile in note.bookmarked_by.all():
            note.unbookmark(profile)
        else:
            note.bookmark(profile)

        return redirect('note-detail', pk=note.pk)


# profile creation / display / update views

class CreateProfileView(CreateView):
    """
    View to handle both user registration and profile creation.
    """
    model = Profile
    form_class = CreateProfileForm
    template_name = 'project/create_profile_form.html'
    success_url = reverse_lazy('home')  # Redirect to home after successful registration

    def get_context_data(self, **kwargs):
        """
        Add the UserCreationForm to the context.
        """
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST request with both UserCreationForm and CreateProfileForm.
        """
        self.object = None
        user_form = UserCreationForm(self.request.POST)
        profile_form = self.get_form()

        if user_form.is_valid() and profile_form.is_valid():
            return self.form_valid(user_form, profile_form)
        else:
            return self.form_invalid(user_form, profile_form)

    def form_valid(self, user_form, profile_form):
        """
        If both forms are valid, save the user and profile.
        """
        # Save the user
        user = user_form.save()
        user.email = profile_form.cleaned_data.get('email_address')
        user.first_name = profile_form.cleaned_data.get('first_name')
        user.last_name = profile_form.cleaned_data.get('last_name')
        user.save()

        # Save the profile
        profile = profile_form.save(commit=False)
        profile.user = user

        # Handle profile image logic
        profile_image_url = profile_form.cleaned_data.get('profile_image_url')
        profile_img_file = self.request.FILES.get('profile_img_file')

        if profile_image_url:
            profile.profile_img_url = profile_image_url
        elif profile_img_file:
            profile.profile_img_file = profile_img_file
        else:
            profile.profile_img_url = '/media/profile_images/default_pfp.jpg'

        profile.save()

        # Log in the user
        login(self.request, user)

        return super().form_valid(profile_form)

    def form_invalid(self, user_form, profile_form):
        """
        If the forms are invalid, re-render the page with errors.
        """
        return self.render_to_response(
            self.get_context_data(
                form=profile_form,
                user_form=user_form
            )
        )

    def get_success_url(self):
        """
        Redirect to the home page or any other page after successful registration.
        """
        return reverse('home')

class ProfileDetailView(DetailView):
    """View to display the details of a user's profile."""
    model = Profile
    template_name = 'project/profile_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.object

        # Notes authored by the profile
        context['notes'] = Note.objects.filter(author=user_profile).order_by('-upload_date')
        context['notes_count'] = context['notes'].count()

        # Notes liked and bookmarked by the profile
        context['liked_notes_count'] = user_profile.liked_notes.count()
        context['bookmarked_notes_count'] = user_profile.bookmarked_notes.count()
        context['bookmarks'] = user_profile.bookmarked_notes.all()

        # Total likes received on the user's notes
        context['total_likes_received'] = sum(note.like_count for note in context['notes'])

        # Followers and following counts
        context['followers_count'] = user_profile.followers.count()
        context['following_count'] = user_profile.following.count()

        return context



class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View to update a user's profile."""
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'project/update_profile_form.html'

    def get_success_url(self):
        # Redirect to the profile-detail page of the updated profile
        return reverse('profile-detail', kwargs={'pk': self.object.id})

    def get_object(self, queryset=None):
        # Ensure the user can only update their own profile
        return self.request.user.project_profile
    
# followers / following

class FollowersListView(ListView):
    """View to look at followers"""
    model = Profile
    template_name = 'project/followers_list.html'
    context_object_name = 'followers'

    def get_queryset(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return profile.followers.all()


class FollowingListView(ListView):
    """same as before but following"""
    model = Profile
    template_name = 'project/following_list.html'
    context_object_name = 'following'

    def get_queryset(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return profile.following.all()

class FollowProfileView(LoginRequiredMixin, ListView):
    """view to follow a profile"""
    def post(self, request, pk, *args, **kwargs):
        profile_to_follow = get_object_or_404(Profile, pk=pk)
        current_user_profile = request.user.project_profile

        if profile_to_follow in current_user_profile.following.all():
            current_user_profile.following.remove(profile_to_follow)
        else:
            current_user_profile.following.add(profile_to_follow)

        return redirect('profile-detail', pk=pk)
    
# comments

class CommentCreateView(LoginRequiredMixin, View):
    """view to make a comment"""
    def post(self, request, pk, *args, **kwargs):
        note = get_object_or_404(Note, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.note = note
            comment.user = request.user.project_profile
            comment.save()
            return redirect('note-detail', pk=pk)
        return render(request, 'project/note_detail.html', {
            'note': note,
            'comments': Comment.objects.filter(note=note).order_by('-date'),
            'comment_form': form
        })

class CommentEditView(LoginRequiredMixin, UpdateView):
    """view to edit a comment"""
    model = Comment
    form_class = CommentForm
    template_name = 'project/edit_comment_form.html'

    def get_success_url(self):
        return reverse('note-detail', kwargs={'pk': self.object.note.pk})

    def get_queryset(self):
        # Restrict to the user's own comments
        return Comment.objects.filter(user=self.request.user.project_profile)
    
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    """view to delete a comment"""
    model = Comment
    template_name = 'project/delete_comment_confirm.html'

    def get_success_url(self):
        return reverse('note-detail', kwargs={'pk': self.object.note.pk})

    def get_queryset(self):
        # Restrict to the user's own comments
        return Comment.objects.filter(user=self.request.user.project_profile)

