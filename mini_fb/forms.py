## mini_fb/porms.py
## description: forms for the mini_fb app

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    ''' 
    a form for creating a new Profile object. 
    this form collects the following data from the user:
        - First Name
        - Last Name
        - City
        - Email Address
        - Profile Image URL

    submission means a new Profile instance will be created using 
    the provided data and stored in the database.
    '''

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

    city = forms.CharField(
        label="City", 
        max_length=100, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your city',
            'class': 'form-control'
        })
    )

    email_address = forms.EmailField(
        label="Email Address", 
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'class': 'form-control'
        })
    )

    profile_img_url = forms.URLField(
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

    birth_date = forms.DateField(
        label="Birth Date",
        widget=forms.SelectDateWidget(
            years=range(1900, 2025),
            attrs={'class': 'form-select'}
        )
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_img_url', 'birth_date']

class CreateStatusMessageForm(forms.ModelForm):
    ''' 
    a form for creating a new StatusMessage object.
    '''
    class Meta:
        model = StatusMessage
        fields = ['message']  