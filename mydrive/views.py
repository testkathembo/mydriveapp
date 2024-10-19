from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm, FileUploadForm
from .models import Profile, UploadedFile, Folder  # Ensure UploadedFile and Folder are imported

def register(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user first
            Profile.objects.create(user=user)  # Create the profile linked to the user
            Folder.objects.create(profile=user.profile, name='Root Folder')  # Create a root folder for the user
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
    try:
        profile = Profile.objects.get(user=request.user)  # Ensure we get the user's profile
    except Profile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('home')  # Redirect if profile does not exist

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
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES, user=request.user)  # Pass user
        if form.is_valid():
            uploaded_file = form.save(commit=False)  # Don't save yet
            uploaded_file.folder = form.cleaned_data['folder']  # Set folder from form
            uploaded_file.save()  # Save the uploaded file instance
            messages.success(request, 'File uploaded successfully!')
            return redirect('browse')  # Redirect to browse view after upload
    else:
        form = FileUploadForm(user=request.user)  # Pass user

    return render(request, 'upload.html', {'form': form})



@login_required
def browse_files(request):
    """Handles browsing uploaded files for logged-in users."""
    try:
        profile = Profile.objects.get(user=request.user)
        uploaded_files = UploadedFile.objects.filter(folder__profile=profile)  # Fetch files related to the user's profile
        folders = profile.folders.all()  # Fetch all folders related to the user's profile

        return render(request, 'browse.html', {
            'uploaded_files': uploaded_files,
            'folders': folders,  # Pass the folders to the template if needed
        })
    except Profile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('home')


@login_required
def manage_files(request):
    """Handles file management for logged-in users."""
    try:
        profile = Profile.objects.get(user=request.user)  # Get the user's profile
        uploaded_files = UploadedFile.objects.filter(folder__profile=profile)  # Fetch files related to the profile

        if request.method == 'POST':
            action = request.POST.get('action')
            file_id = request.POST.get('file_id')
            new_name = request.POST.get('new_name')

            try:
                uploaded_file = UploadedFile.objects.get(id=file_id, folder__profile=profile)  # Adjusted for folder

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

        return render(request, 'manage_files.html', {'uploaded_files': uploaded_files})

    except Profile.DoesNotExist:
        messages.error(request, 'Profile not found for the user.')
        return redirect('home')

@login_required
def create_folder(request):
    """Handles folder creation for logged-in users."""
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        parent_id = request.POST.get('parent_id')  # If you're allowing nested folders

        parent_folder = None
        if parent_id:
            parent_folder = Folder.objects.get(id=parent_id)  # Get the parent folder if provided

        # Use 'parent_folder' instead of 'parent'
        folder = Folder(name=folder_name, profile=request.user.profile, parent_folder=parent_folder)
        folder.save()
        messages.success(request, 'Folder created successfully!')
        return redirect('browse')  # Redirect to the browse view

    return render(request, 'create_folder.html')


@login_required
def browse_folders(request, folder_id):
    """Handles displaying the contents of a specific folder for logged-in users."""
    try:
        folder = Folder.objects.get(id=folder_id, profile=request.user.profile)  # Ensure to link it with the user's profile

        # Fetch the files and subfolders in the folder
        files = folder.files.all()  # Get all files associated with this folder
        subfolders = folder.subfolders.all()  # Get all subfolders within this folder

        return render(request, 'browse_folder.html', {
            'folder': folder,
            'files': files,
            'subfolders': subfolders,
        })
    except Folder.DoesNotExist:
        messages.error(request, 'Folder not found.')
        return redirect('browse')  # Redirect to the browse view if folder not found

