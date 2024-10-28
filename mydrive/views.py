from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (UserRegistrationForm, UserLoginForm, FileUploadForm,)
from django.contrib.auth.models import User
from .models import UploadedFile  # Make sure this import is added

def register(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    """Handles user login."""
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Logs out the user and redirects to the login page."""
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')


def home_view(request):
    files = UploadedFile.objects.filter(owner=request.user)  # Example usage
    return render(request, 'home.html', {'files': files})


@login_required
def upload_file_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.owner = request.user  # Set the owner to the current user
            uploaded_file.original_location = uploaded_file.file.name  # Example of setting original location
            uploaded_file.save()
            return redirect('home')  # Redirect to a success page
        else:
            return render(request, 'upload_form.html', {'form': form})
    else:
        form = FileUploadForm()
        return render(request, 'upload_form.html', {'form': form})

