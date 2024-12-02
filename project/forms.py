## project/forms.py
## description: forms for the project app

from django import forms
from .models import *
import datetime

class CreateProfileForm(forms.ModelForm):
    """
    Form for creating a new Profile object. Collects the following data:
    - First Name
    - Last Name
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
        fields = ['first_name', 'last_name', 'email_address', 'bio', 'profile_img_file', 'major', 'minor', 'school', 'class_year']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name', 'class': 'form-control'}),
            'email_address': forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Tell us about yourself', 'class': 'form-control', 'rows': 4}),
            'profile_img_file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'major': forms.TextInput(attrs={'placeholder': 'Enter your major', 'class': 'form-control'}),
            'minor': forms.TextInput(attrs={'placeholder': 'Enter your minor', 'class': 'form-control'}),
            'school': forms.TextInput(attrs={'placeholder': 'Enter your school', 'class': 'form-control'}),
            'class_year': forms.NumberInput(attrs={'placeholder': 'Class Year', 'class': 'form-control'}),
        }

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
