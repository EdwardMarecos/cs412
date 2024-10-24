## mini_fb/porms.py
## description: forms for the mini_fb app

from django import forms
from .models import Profile, StatusMessage
import datetime

class CreateProfileForm(forms.ModelForm):
    ''' 
    a form for creating a new Profile object. 
    this form collects the following data from the user:
        - First Name
        - Last Name
        - City
        - Email Address
        - Birth Date
        - Profile Image URL / file

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

    birth_date = forms.DateField(
        label="Birth Date",
        widget=forms.SelectDateWidget(
            attrs={'class': 'form-select'}
        )
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

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email_address', 'birth_date', 'profile_img_url', 'profile_img_file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the initial year to 2025 to avoid scrolling
        today = datetime.date.today()
        self.fields['birth_date'].widget.years = range(today.year+1, 1899, -1)

class CreateStatusMessageForm(forms.ModelForm):
    ''' 
    a form for creating a new StatusMessage object.
    '''
    class Meta:
        model = StatusMessage
        fields = ['message']  

class UpdateProfileForm(forms.ModelForm):
    '''
    a form for updating a profile
    '''
    
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

    birth_date = forms.DateField(
        label="Birth Date",
        widget=forms.SelectDateWidget(
            attrs={'class': 'form-select'}
        )
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

    class Meta:
        model = Profile
        fields = ['city', 'email_address', 'birth_date', 'profile_img_url', 'profile_img_file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the initial year to 2025 to avoid scrolling
        today = datetime.date.today()
        self.fields['birth_date'].widget.years = range(today.year+1, 1899, -1)
        # i had to specify here because it wouldnt let me use the today in the date above, and
        # def not backwards. i tried the -1 and it was odd, didnt work