# File: forms.py
# Author: Edward Marecos (emarecos@bu.edu), 12/1/2024
# Description: Contains form classes for the project app. These forms are used to create and update instances of Profile, Note, and Comment models, and provide input validation and UI customization.

from django import forms  # Importing Django's form utilities
from .models import *  # Importing all models from the local app

class CreateProfileForm(forms.ModelForm):
    """
    Form for creating a new Profile object along with user information.
    """

    first_name = forms.CharField(
        label="First Name",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your first name',
            'class': 'form-control'
        })
    )

    last_name = forms.CharField(
        label="Last Name",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your last name',
            'class': 'form-control'
        })
    )

    email_address = forms.EmailField(
        label="Email Address",
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'class': 'form-control'
        })
    )

    bio = forms.CharField(
        label="Bio",
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Tell us about yourself',
            'class': 'form-control',
            'rows': 4
        })
    )

    profile_image_url = forms.URLField(
        label="Profile Image URL (Optional)",
        required=False,
        help_text="Provide a URL to an image if you prefer.",
        widget=forms.URLInput(attrs={
            'placeholder': 'Enter profile image URL',
            'class': 'form-control'
        })
    )

    profile_img_file = forms.ImageField(
        label="Or Upload a Profile Picture (Optional)",
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file'
        })
    )

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'email_address',
            'bio',
            'profile_img_file',
            'major',
            'minor',
            'school',
            'class_year'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class UpdateProfileForm(forms.ModelForm):
    """
    Form for updating a Profile object. Collects the following data:

    - Email Address
    - Bio
    - Profile Picture (optional)
    - Major
    - Minor
    - School
    - Class Year
    """

    class Meta:
        model = Profile
        fields = ['email_address', 'bio', 'profile_img_file', 'major', 'minor', 'school', 'class_year']
        widgets = {
            'email_address': forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Tell us about yourself', 'class': 'form-control', 'rows': 4}),
            'profile_img_file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'major': forms.TextInput(attrs={'placeholder': 'Enter your major', 'class': 'form-control'}),
            'minor': forms.TextInput(attrs={'placeholder': 'Enter your minor', 'class': 'form-control'}),
            'school': forms.TextInput(attrs={'placeholder': 'Enter your school', 'class': 'form-control'}),
            'class_year': forms.NumberInput(attrs={'placeholder': 'Class Year', 'class': 'form-control'}),
        }

class CreateNoteForm(forms.ModelForm):
    """Form for creating a new Note object."""
    class Meta:
        model = Note
        fields = ['topic', 'title', 'content']
        widgets = {
            'topic': forms.Select(attrs={
                'class': 'form-control',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control title-input',
                'placeholder': 'Enter title here...',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control content-textarea',
                'placeholder': 'Start writing your note...',
                'rows': 15,
            }),
        }

class CommentForm(forms.ModelForm):
    """Form for creating or editing a Comment object."""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Edit your comment...',
            }),
        }
