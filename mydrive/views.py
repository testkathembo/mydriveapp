from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm, FileUploadForm
from .models import Profile, UploadedFile  # Ensure UploadedFile is imported


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
    profile, created = Profile.objects.get_or_create(user=request.user)

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
def browse_files(request):
    """Handles browsing uploaded files for logged-in users."""
    profile = Profile.objects.get(user=request.user)
    uploaded_files = profile.uploadedfile_set.all()  # Fetch all uploaded files related to the profile

    return render(request, 'browse.html', {'uploaded_files': uploaded_files})

@login_required
def manage_files(request):
    """Handles file management for logged-in users."""
    profile = Profile.objects.get(user=request.user)  # Get the user's profile

    if request.method == 'POST':
        action = request.POST.get('action')
        file_id = request.POST.get('file_id')
        new_name = request.POST.get('new_name')

        try:
            uploaded_file = UploadedFile.objects.get(id=file_id, profile=profile)  # Fetch the uploaded file using profile

            if action == 'delete':
                uploaded_file.delete()  # Deletes the file instance
                messages.success(request, 'File deleted successfully.')
            elif action == 'rename':
                uploaded_file.file.name = new_name  # Update the name
                uploaded_file.save()  # Save changes
                messages.success(request, 'File renamed successfully.')

        except UploadedFile.DoesNotExist:
            messages.error(request, 'File not found.')
        except Exception as e:
            messages.error(request, str(e))

    # Fetch all uploaded files for the user's profile
    uploaded_files = UploadedFile.objects.filter(profile=profile)  # Use profile to filter

    return render(request, 'manage_files.html', {'uploaded_files': uploaded_files})

@login_required
def upload_file(request):
    """Handles file uploads for logged-in users."""
    profile = Profile.objects.get(user=request.user)  # Get the user's profile

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            # Check if the upload does not exceed storage limit
            if profile.storage_used + file.size <= 100 * 1024 * 1024:  # Assuming 100MB limit
                UploadedFile.objects.create(user=request.user, file=file)  # Save the file
                profile.storage_used += file.size
                profile.save()
                messages.success(request, 'File uploaded successfully!')
                return redirect('home')  # Redirect after successful upload
            else:
                messages.error(request, 'Storage limit exceeded.')
    else:
        form = FileUploadForm()

    return render(request, 'upload.html', {'form': form})
