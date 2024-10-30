# mini_fb/views.py
# define the views for the mini_fb app

from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, StatusMessage, Image, Friend
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm # import the form
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
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

class CreateProfileView(CreateView):
    '''Display a form to create a new Profile object.'''
    model = Profile  # Use the Profile model
    form_class = CreateProfileForm  # Use the CreateProfileForm to generate the form
    template_name = 'mini_fb/create_profile_form.html'  # Template for the form

    def form_valid(self, form):
        # Check if both fields are empty before saving
        profile = form.save(commit=False)  # Don't save to the database just yet 
        # (i was having a bug that it was saving before applying changes if certain fields werent filled [fields i wanted optional])

        if not profile.profile_img_file and not profile.profile_img_url:
            profile.profile_img_url = '/media/profile_images/default_pfp.jpg'  # Set default URL for default pfp

        profile.save()  # Now save to the database
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the new profile's detail view after creation."""
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''A view to create a status message for a Profile.'''
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def dispatch(self, request, *args, **kwargs):
        """Override dispatch to handle permission denial"""
        try:
            # Get the profile object based on the primary key in the URL kwargs
            profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
            # Check if the profile belongs to the logged-in user
            if profile.user != self.request.user:
                raise PermissionDenied
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied:
            # Redirect to custom access denied page if permission is denied
            return redirect('access_denied')

    def get_context_data(self, **kwargs):
        # Get the context dictionary from the base implementation
        context = super().get_context_data(**kwargs)
        # Get the Profile object using the primary key from URL kwargs
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        # Add the Profile object to the context dictionary
        context['profile'] = profile
        return context

    def form_valid(self, form):
        # Set the profile attribute on the StatusMessage object before saving
        form.instance.profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
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
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def dispatch(self, request, *args, **kwargs):
        """Override dispatch to handle permission denial"""
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied:
            # Redirect to our custom access denied page if permission is denied
            return redirect('access_denied')

    def get_object(self, queryset=None):
        """Ensure the logged-in user can only update their own profile."""
        profile = super().get_object(queryset)
        if profile.user != self.request.user:
            raise PermissionDenied  # This will be caught by dispatch
        return profile

    def form_valid(self, form):
        profile = form.save(commit=False)

        # If the 'clear_profile_image' checkbox is checked, reset to default
        # there is a bug in which u reset, and then try to put a file and it asks for a url after. 
        # i cannot figure it out atm so it works if u just remove the default url (very easy for users)
        # also if u put a profile and check the box it returns default, i need some xor functionality for these lol
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

    def dispatch(self, request, *args, **kwargs):
        """Override dispatch to handle permission denial"""
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied:
            # Redirect to custom access denied page if permission is denied
            return redirect('access_denied')

    def get_object(self, queryset=None):
        """Ensure the logged-in user can only update their own status message."""
        status_message = super().get_object(queryset)
        if status_message.profile.user != self.request.user:
            raise PermissionDenied
        return status_message

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

    def dispatch(self, request, *args, **kwargs):
        """Override dispatch to handle permission denial"""
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied:
            # Redirect to custom access denied page if permission is denied
            return redirect('access_denied')

    def get_object(self, queryset=None):
        """
        Override get_object to ensure we retrieve the correct status message
        that matches both the profile and the status message ID.
        """
        status_message = super().get_object(queryset)
        if status_message.profile.user != self.request.user:
            raise PermissionDenied
        profile_pk = self.kwargs['profile_pk']
        status_pk = self.kwargs['pk']
        return get_object_or_404(StatusMessage, pk=status_pk, profile_id=profile_pk)
    
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
        profile_pk = self.get_object().profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})

class CreateFriendView(LoginRequiredMixin, CreateView):
    ''' Implement/override the dispatch method, in 
    which we can read the URL parameters (from self.kwargs), 
    use the object manager to find the requisite Profile objects, 
    and then call the Profile‘s add_friend method (from step 2, 
    above). Finally, we can redirect the user back to the profile 
    page. '''
    def dispatch(self, request, *args, **kwargs):
        # Retrieve both profiles
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        other_profile = get_object_or_404(Profile, pk=self.kwargs['other_pk'])

        # Ensure they aren't the same profile (no self-friending)
        if profile != other_profile:
            profile.add_friend(other_profile)  # Add the friend

        # Redirect back to the original profile's page
        return redirect('show_profile', pk=profile.pk)

class ShowFriendSuggestionsView(DetailView):
    ''' display the friend suggestions for a single profile
    along with links to add friends'''
    model = Profile  # Retrieve the Profile object
    template_name = 'mini_fb/friend_suggestions.html'  # Template to render
    context_object_name = 'befriend'  # Maintain consistency in naming

    def get_context_data(self, **kwargs):
        """
        Add friend suggestions to the context.
        """
        context = super().get_context_data(**kwargs)
        context['profile_pk'] = self.kwargs['pk']  # Pass the profile's primary key for the cancel link
        return context

class ShowNewsFeedView(DetailView):
    ''' displays the news feed for a single Profile '''
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        '''Provide context for the news feed view.'''
        context = super().get_context_data(**kwargs)
        context['ret_profile'] = self.kwargs['pk']  # return to profile from news
        return context

def custom_access_denied_view(request, exception=None):
    """Custom view for handling permission denied (403) errors."""
    print("Custom 403 view is being used")
    return render(request, 'mini_fb/403.html', status=403)

