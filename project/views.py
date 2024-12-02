from django.http import *
from django.shortcuts import *
from django.views.generic import *
from .models import *

from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .forms import *

# display main page

class HomeView(TemplateView):
    template_name = 'project/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            current_profile = self.request.user.project_profile
            context['notes'] = Note.objects.order_by('-like_count')[:10]  # Top 10 notes by likes
            all_users = Profile.objects.exclude(user=self.request.user)
            # Add an attribute `is_followed` to each user for the template
            for user in all_users:
                user.is_followed = current_profile.following.filter(id=user.id).exists()
            context['users'] = all_users
            context['categories'] = Category.objects.all()
        return context


# relevant views for categories
class CategoryListView(ListView):
    model = Category
    template_name = 'project/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'project/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
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
    model = Category
    fields = ['name', 'graphic']
    template_name = 'project/add_category_form.html'
    success_url = reverse_lazy('category-list')  # Redirect to the category list after adding a category

    def form_valid(self, form):
        # Optionally, you can add custom logic here before saving the category
        return super().form_valid(form)

    
# subjects
class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    fields = ['name']
    template_name = 'project/add_subject_form.html'

    def form_valid(self, form):
        category = get_object_or_404(Category, id=self.kwargs['category_id'])
        form.instance.category = category
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('category-detail', kwargs={'pk': self.kwargs['category_id']})
    
class SubjectListView(ListView):
    model = Subject
    template_name = 'project/subject_list.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return Subject.objects.filter(category=category)
    
# topics
class TopicCreateView(LoginRequiredMixin, CreateView):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        note = self.get_object()
        context['comments'] = Comment.objects.filter(note=note).order_by('-date')
        context['comment_form'] = CommentForm()
        return context

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

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = CreateNoteForm  # Reuse your existing form
    template_name = 'project/update_note_form.html'

    def get_queryset(self):
        # Restrict updates to the note's author
        return Note.objects.filter(author=self.request.user.project_profile)

    def get_success_url(self):
        # Redirect to the note detail page after update
        return reverse('note-detail', kwargs={'pk': self.object.pk})


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'project/note_confirm_delete.html'
    context_object_name = 'note'

    def get_queryset(self):
        # Restrict deletion to the note's author
        return Note.objects.filter(author=self.request.user.project_profile)

    def get_success_url(self):
        # Redirect to the note list after deletion
        return reverse('note-list')


# toggle likes / bookmarks

class ToggleLikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        note = get_object_or_404(Note, pk=pk)
        profile = request.user.project_profile

        if profile in note.liked_by.all():
            note.unlike(profile)
        else:
            note.like(profile)

        return redirect('note-detail', pk=note.pk)
    
class ToggleBookmarkView(LoginRequiredMixin, View):
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
    model = Profile
    template_name = 'project/followers_list.html'
    context_object_name = 'followers'

    def get_queryset(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return profile.followers.all()


class FollowingListView(ListView):
    model = Profile
    template_name = 'project/following_list.html'
    context_object_name = 'following'

    def get_queryset(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return profile.following.all()

class FollowProfileView(LoginRequiredMixin, ListView):
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
    model = Comment
    form_class = CommentForm
    template_name = 'project/edit_comment_form.html'

    def get_success_url(self):
        return reverse('note-detail', kwargs={'pk': self.object.note.pk})

    def get_queryset(self):
        # Restrict to the user's own comments
        return Comment.objects.filter(user=self.request.user.project_profile)
    
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'project/delete_comment_confirm.html'

    def get_success_url(self):
        return reverse('note-detail', kwargs={'pk': self.object.note.pk})

    def get_queryset(self):
        # Restrict to the user's own comments
        return Comment.objects.filter(user=self.request.user.project_profile)

