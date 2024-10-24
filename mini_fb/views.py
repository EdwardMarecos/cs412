# mini_fb/views.py
# define the views for the mini_fb app

from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, StatusMessage, Image
from .forms import CreateProfileForm, CreateStatusMessageForm # import the form
from django.views.generic import ListView, DetailView, CreateView
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

class CreateStatusMessageView(CreateView):
    '''A view to create a status message for a Profile.'''
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

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