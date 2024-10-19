# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm  # Import built-in authentication form
from .models import Profile, UploadedFile, Folder  # Import your custom models

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number']
        # Customize widgets and hide help text
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'ex: Kathembo'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'ex: Tsongo'}),
            'username': forms.TextInput(attrs={'placeholder': 'ex: Dieudonne'}),
            'email': forms.EmailInput(attrs={'placeholder': 'address@gmail.com'}),
        }
        
        # If you want to remove all help_texts from the fields
        help_texts = {
            'username': '',
            'first_name': '',
            'last_name': '',
            'email': '',
            'phone_number': '',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")

    def save(self, commit=True):
        user = super().save(commit=False)  # Create a user instance but don't save yet
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()  # Save the user to the database
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    
class FileUploadForm(forms.ModelForm):
    folder = forms.ModelChoiceField(queryset=Folder.objects.none(), required=True)  # Initially empty

    class Meta:
        model = UploadedFile  # Use the UploadedFile model
        fields = ['file', 'folder']  # Include folder in the fields

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from the kwargs
        super().__init__(*args, **kwargs)

        if user is not None:
            # Filter folders for the specific user
            self.fields['folder'].queryset = Folder.objects.filter(profile=user.profile)




class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile  # Use the Profile model
        fields = ['name']  # Only include fields from Profile that you want to update
