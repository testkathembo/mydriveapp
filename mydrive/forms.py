from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import AuthenticationForm  # Import built-in authentication form
from .models import Profile  # Import your custom Profile model

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
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'file']
        
class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Profile  # Make sure this references your Profile model
        fields = ['file']  # Only include the file field for upload
        

