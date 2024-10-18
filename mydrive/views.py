from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm, FileUploadForm
from .models import Profile

def register(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
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

@login_required
def home_view(request):
    """Renders the home page for logged-in users."""
    return render(request, 'home.html')

def logout_view(request):
    """Logs out the user and redirects to the login page."""
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')

@login_required
def update_profile(request):
    """Handles profile updates for logged-in users."""
    profile, created = Profile.objects.get_or_create(user=request.user)  # Automatically create a profile if it doesn't exist

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('home')
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'update_profile.html', {'form': form})

@login_required
def upload_file(request):
    """Handles file uploads for logged-in users."""
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            # Validate that the upload does not exceed storage limit
            if profile.storage_used + file.size <= 100 * 1024 * 1024:  # 100MB limit
                profile.file = file
                profile.storage_used += file.size
                profile.save()
                messages.success(request, 'File uploaded successfully!')
                return redirect('browse')  # Redirect to browse page
            else:
                messages.error(request, 'Storage limit exceeded.')
    else:
        form = FileUploadForm()

    return render(request, 'upload.html', {'form': form})

@login_required
def browse_files(request):
    """Handles browsing uploaded files for logged-in users."""
    profile = Profile.objects.get(user=request.user)
    uploaded_files = []  # Adjust this logic to handle multiple files as necessary

    if profile.file:
        uploaded_files.append(profile.file)

    return render(request, 'browse.html', {'uploaded_files': uploaded_files})

@login_required
def manage_files(request):
    """Allows users to manage their uploaded files."""
    uploaded_files = UploadedFile.objects.filter(user=request.user)  # Get files for the logged-in user

    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        action = request.POST.get('action')

        # Handle delete action
        if action == 'delete':
            file_to_delete = UploadedFile.objects.get(id=file_id, user=request.user)
            file_to_delete.file.delete()  # Delete the file from the filesystem
            file_to_delete.delete()  # Remove the record from the database
            messages.success(request, 'File deleted successfully!')

        # Handle rename action
        elif action == 'rename':
            new_name = request.POST.get('new_name')
            file_to_rename = UploadedFile.objects.get(id=file_id, user=request.user)
            file_to_rename.file.name = f'uploads/{new_name}'  # Adjust the path if necessary
            file_to_rename.save()
            messages.success(request, 'File renamed successfully!')

    return render(request, 'manage_files.html', {'uploaded_files': uploaded_files})

