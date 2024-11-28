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
    """
    Form to create a new Note with dynamic Category, Subject, and Topic selection.
    """
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )
    topic = forms.ModelChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )

    class Meta:
        model = Note
        fields = ['title', 'content', 'category', 'subject', 'topic']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter note title', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your note here...', 'class': 'form-control', 'rows': 20}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Handle pre-filtering for subject and topic if category/subject data exists
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subject'].queryset = Subject.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        if 'subject' in self.data:
            try:
                subject_id = int(self.data.get('subject'))
                self.fields['topic'].queryset = Topic.objects.filter(parent_subject_id=subject_id)
            except (ValueError, TypeError):
                pass
        # Default empty queryset for filtered fields if no initial data is provided
        self.fields['subject'].queryset = Subject.objects.all()
        self.fields['topic'].queryset = Topic.objects.all()















