from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (UserRegistrationForm, UserLoginForm, FileUploadForm,)
from django.contrib.auth.models import User
from .models import UploadedFile  # Make sure this import is added
from django.http import HttpResponse
from .forms import FileRenameForm  # Ensure you have a form for renaming
from django.http import FileResponse



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


@login_required
def home_view(request):
    # Fetch all files for the current user or all files if admin
    files = UploadedFile.objects.all() if request.user.is_superuser else UploadedFile.objects.filter(owner=request.user)
    # Prepare the full name of the user
    full_name = f"{request.user.first_name} {request.user.last_name}"
    # Pass it along with other context data to the template
    context = {
        'files': files,
        'name': full_name  # Passing user's full name to the template
    }
    return render(request, 'home.html', context)



@login_required
def upload_file_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            if not file_instance.name:  # Ensure name is set
                file_instance.name = file_instance.file.name
            file_instance.owner = request.user  # Setting the owner
            file_instance.save()
            messages.success(request, 'File uploaded successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Upload failed. Please check the form.')
    else:
        form = FileUploadForm()
    return render(request, 'upload_file.html', {'form': form})

def rename_file(request, file_id):
    file = get_object_or_404(UploadedFile, pk=file_id)
    if request.method == 'POST':
        new_name = request.POST.get('new_name', '')
        if new_name:
            file.name = new_name
            file.save()
            messages.success(request, "File renamed successfully.")
        return redirect('home')
    else:
        return render(request, 'rename_file.html', {'file': file})


def delete_file(request, file_id):
    file = get_object_or_404(UploadedFile, pk=file_id)
    file.delete()
    messages.success(request, "File deleted successfully.")
    return redirect('home')


    

def download_file(request, file_id):
    # Retrieve the file instance
    file_instance = get_object_or_404(UploadedFile, pk=file_id)
    
    # Serve the file
    response = FileResponse(file_instance.file.open(), as_attachment=True, filename=file_instance.name)
    
    return response


