from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import UploadedFile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'ex: Kathembo'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'ex: Tsongo'}),
            'username': forms.TextInput(attrs={'placeholder': 'ex: Dieudonne'}),
            'email': forms.EmailInput(attrs={'placeholder': 'address@gmail.com'}),
        }
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
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    
class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file', 'name', 'original_location']  # `original_location` can be optional depending on your design

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
    

class FileRenameForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['name']  # Assuming 'name' is the field you want to change


