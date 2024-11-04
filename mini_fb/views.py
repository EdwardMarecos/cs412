# mini_fb/views.py
# define the views for the mini_fb app

from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, StatusMessage, Image, Friend
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.exceptions import PermissionDenied
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm # import the form
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.utils import timezone

# Create your views here.

class ShowAllView(ListView):
    '''Create a subclass of ListView to display all blog articles.'''
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # how to find the data in the template file

class ShowProfilePage(DetailView):
    ''' obtain data for one Profile record, and to deleguate work 
    to a template called show_profile.html to display that Profile.'''
    model = Profile  # Retrieve a single Profile object
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'  # Used to access profile data in the template

    def get_object(self, queryset=None):
        # Retrieve the Profile object based on the provided `pk` in the URL.
        # If a `pk` is provided, return that user's profile;
        # otherwise, return the logged-in user's profile.
        if 'pk' in self.kwargs:
            return get_object_or_404(Profile, pk=self.kwargs['pk'])
        elif self.request.user.is_authenticated:
            return get_object_or_404(Profile, user=self.request.user)
        else:
            # If no pk is provided and the user is not logged in, raise 404.
            raise Http404("Profile not found.")
        
    def get_context_data(self, **kwargs):
        """Add extra context to indicate if this is the logged-in user's profile and if they are friends."""
        context = super().get_context_data(**kwargs)

        # Add context only if the user is authenticated
        if self.request.user.is_authenticated:
            current_user_profile = get_object_or_404(Profile, user=self.request.user)
            profile_viewed = self.get_object()
            context['is_own_profile'] = profile_viewed.user == self.request.user
            context['is_friend'] = profile_viewed in current_user_profile.get_friends()
        else:
            # For unauthenticated users, set `is_own_profile` and `is_friend` to False
            context['is_own_profile'] = False
            context['is_friend'] = False

        return context

class CreateProfileView(CreateView):
    '''Display a form to create a new Profile object.'''
    model = Profile  # Use the Profile model
    form_class = CreateProfileForm  # Use the CreateProfileForm to generate the form
    template_name = 'mini_fb/create_profile_form.html'  # Template for the form
    success_url = reverse_lazy('base')

    def get_context_data(self, **kwargs):
        """Add the UserCreationForm to the context data."""
        context = super().get_context_data(**kwargs)
        # Include the user form in context to populate fields upon re-render
        if 'user_form' not in context:
            context['user_form'] = kwargs.get('user_form') or UserCreationForm()
        return context

    def form_valid(self, form):
        # Reconstruct the UserCreationForm with POST data
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            # Save the user and get the instance
            user = user_form.save()
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email_address']
            user.save()

            # Attach the user to the profile
            form.instance.user = user

            # Handle the profile image logic
            profile_image_url = form.cleaned_data.get('profile_image_url')
            profile_img_file = self.request.FILES.get('profile_img_file')

            if profile_image_url:
                form.instance.profile_img_url = profile_image_url
            elif profile_img_file:
                form.instance.profile_img_file = profile_img_file
            else:
                form.instance.profile_img_url = '/media/profile_images/default_pfp.jpg'

            # Save the profile instance and log in the user
            response = super().form_valid(form)
            login(self.request, user)
            return response
        else:
            # Re-render the form with user form errors if invalid
            return self.render_to_response(
                self.get_context_data(form=form, user_form=user_form)
            )

    def get_success_url(self):
        """Redirect to the new profile's detail view after creation."""
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''A view to create a status message for a Profile.'''
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        """Override to add the profile context for the logged-in user."""
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, user=self.request.user)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        # Set the profile attribute on the StatusMessage object before saving
        form.instance.profile = get_object_or_404(Profile, user=self.request.user)
        # Set the current timestamp for the status message
        form.instance.timestamp = timezone.now()
        # Save the StatusMessage object and get a reference to it
        sm = form.save()

        # Get the list of uploaded files
        files = self.request.FILES.getlist('files')  
        for f in files:
            # Create an Image object for each file
            image = Image(image=f, message=sm)  
            # Save the Image object to the database
            image.save()  

        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the profile page of the Profile after a successful status message creation
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_object(self, queryset=None):
        """Ensure the logged-in user can only update their own profile."""
        return get_object_or_404(Profile, user=self.request.user)

    def form_valid(self, form):
        profile = form.save(commit=False)

        if form.cleaned_data.get('clear_profile_image'):
            profile.profile_img_url = '/media/profile_images/default_pfp.jpg'  # Set default URL for default pfp
            profile.profile_img_file = None

        profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        ''' Redirect to the profile page after a successful update. '''
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/update_status_message_form.html'

    def get_object(self, queryset=None):
        """
        Override get_object to return the StatusMessage object for the logged-in user.
        """
        # Use custom get_object_or_404 to retrieve the status message for the logged-in user
        return get_object_or_404(StatusMessage, pk=self.kwargs['pk'], profile__user=self.request.user)

    def form_valid(self, form):
        # Save the updated status message object
        sm = form.save()

        # Get the list of uploaded files
        files = self.request.FILES.getlist('files')
        for f in files:
            # Create an Image object for each file and link it to the updated status message
            image = Image(image=f, message=sm)
            image.save()

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the profile page of the related profile after update."""
        # Get the profile associated with the status message being updated
        profile_pk = self.object.profile.pk
        # Redirect to the correct profile page
        return reverse('show_profile', kwargs={'pk': profile_pk})

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_object(self, queryset=None):
        # Use custom get_object_or_403 to retrieve the status message for the logged-in user
        return get_object_or_404(StatusMessage, pk=self.kwargs['pk'], profile__user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the related profile's pk to the context
        context['profile_pk'] = self.get_object().profile.pk
        return context

    def get_success_url(self):
        '''
        return the URL to which the user should be redirected after a successful 
        delete operation. Specifically, when a StatusMessage is deleted, the user 
        should be redirected to the profile page for whom the status message was deleted.
        '''
        # Use the profile's pk for the redirect, not the status message's pk
        return reverse('show_profile', kwargs={'pk': self.get_object().profile.pk})

class CreateFriendView(LoginRequiredMixin, CreateView):
    ''' Implement/override the dispatch method, in 
    which we can read the URL parameters (from self.kwargs), 
    use the object manager to find the requisite Profile objects, 
    and then call the Profile‘s add_friend method (from step 2, 
    above). Finally, we can redirect the user back to the profile 
    page. '''
    def dispatch(self, request, *args, **kwargs):
        # Retrieve both profiles
        profile = get_object_or_404(Profile, user=self.request.user)
        
        # Update to retrieve other_profile by primary key
        other_profile = get_object_or_404(Profile, pk=self.kwargs['other_pk'])

        # Ensure they aren't the same profile (no self-friending)
        if profile != other_profile:
            profile.add_friend(other_profile)  # Add the friend

        # Check for a "next" parameter to determine redirection behavior
        next_url = self.request.GET.get('next')
        if next_url:
            return redirect(next_url)

        # Default redirection to the user's own profile page
        return redirect('show_profile', pk=profile.pk)

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    ''' display the friend suggestions for a single profile
    along with links to add friends'''
    model = Profile  # Retrieve the Profile object
    template_name = 'mini_fb/friend_suggestions.html'  # Template to render
    context_object_name = 'befriend'

    def get_object(self, queryset=None):
        """Return the profile of the logged-in user."""
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Add friend suggestions to the context.
        """
        context = super().get_context_data(**kwargs)
        context['profile_pk'] = self.object.pk  # Pass the profile's primary key for the cancel link
        return context

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    ''' displays the news feed for a single Profile '''
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'news'

    def get_object(self, queryset=None):
        """Return the profile of the logged-in user."""
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        '''Provide context for the news feed view.'''
        context = super().get_context_data(**kwargs)
        # Add the profile of the logged-in user to the context
        context['profile_pk'] = self.object.pk
        return context
