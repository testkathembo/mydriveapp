from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm, FileUploadForm
from .models import Profile, UploadedFile, Folder  # Ensure UploadedFile and Folder are imported
from django.contrib.auth.models import User  # Make sure this is included



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
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)  # Don't save yet
            uploaded_file.folder = form.cleaned_data['folder']  # Set the folder from the form
            uploaded_file.save()  # Save the uploaded file instance
            messages.success(request, 'File uploaded successfully!')
            return redirect('browse')  # Redirect to browse view after upload
    else:
        form = FileUploadForm()

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
        parent_id = request.POST.get('parent_id')  # Get parent folder ID if provided

        parent_folder = None
        if parent_id:
            parent_folder = Folder.objects.get(id=parent_id)  # Get the parent folder object

        # Create the folder with the optional parent folder
        folder = Folder(name=folder_name, profile=request.user.profile, parent_folder=parent_folder)
        folder.save()
        messages.success(request, 'Folder created successfully!')
        return redirect('browse')  # Redirect to the browse view

    # Fetch the folders to populate the dropdown
    folders = Folder.objects.filter(profile=request.user.profile)  # Fetch folders for the logged-in user
    return render(request, 'create_folder.html', {'folders': folders})  # Render the folder creation form


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


@login_required
def move_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    
    if request.method == 'POST':
        target_folder_id = request.POST.get('target_folder')  # Get the folder from the form
        target_folder = get_object_or_404(Folder, id=target_folder_id)

        # Move the file to the selected folder
        file.folder = target_folder
        file.save()
        messages.success(request, 'File moved successfully!')
        return redirect('browse')  # Redirect to the browse view

    folders = Folder.objects.filter(profile=request.user.profile)  # Get user folders for selection
    return render(request, 'move_file.html', {'file': file, 'folders': folders})

@login_required
def copy_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)

    if request.method == 'POST':
        target_folder_id = request.POST.get('target_folder')  # Get the folder from the form
        target_folder = get_object_or_404(Folder, id=target_folder_id)

        # Create a copy of the file
        copied_file = UploadedFile(
            file=file.file,  # Copy the file
            folder=target_folder  # Assign to the selected folder
        )
        copied_file.save()
        messages.success(request, 'File copied successfully!')
        return redirect('browse')  # Redirect to the browse view

    folders = Folder.objects.filter(profile=request.user.profile)  # Get user folders for selection
    return render(request, 'copy_file.html', {'file': file, 'folders': folders})


@login_required
def copy_file(request, file_id):
    """Handles copying files for logged-in users."""
    try:
        file_to_copy = UploadedFile.objects.get(id=file_id)
        folders = Folder.objects.filter(profile=request.user.profile)  # Get all folders for the user

        if request.method == 'POST':
            new_folder_id = request.POST.get('folder_id')  # Get the target folder ID
            new_folder = Folder.objects.get(id=new_folder_id)

            # Create a copy of the file
            uploaded_file_copy = UploadedFile(
                folder=new_folder,
                file=file_to_copy.file,  # Use the same file
            )
            uploaded_file_copy.save()
            messages.success(request, 'File copied successfully!')
            return redirect('browse')  # Redirect to the browse view

        return render(request, 'copy_file.html', {
            'file': file_to_copy,
            'folders': folders,
        })
    except UploadedFile.DoesNotExist:
        messages.error(request, 'File not found.')
        return redirect('browse')
    except Folder.DoesNotExist:
        messages.error(request, 'Target folder not found.')
        return redirect('browse')


from django.shortcuts import get_object_or_404

@login_required
def delete_file(request, file_id):
    """Handles file deletion for logged-in users."""
    file = get_object_or_404(UploadedFile, id=file_id)

    if request.method == 'POST':
        file.delete()  # Delete the file instance
        messages.success(request, 'File deleted successfully!')
        return redirect('browse')  # Redirect to the browse view

    return render(request, 'confirm_delete_file.html', {'file': file})

@login_required
def delete_folder(request, folder_id):
    """Handles folder deletion for logged-in users."""
    folder = get_object_or_404(Folder, id=folder_id)

    if request.method == 'POST':
        folder.delete()  # Delete the folder instance
        messages.success(request, 'Folder deleted successfully!')
        return redirect('browse')  # Redirect to the browse view

    return render(request, 'confirm_delete_folder.html', {'folder': folder})


@login_required
def share_file(request, file_id):
    """Share a file with another user via email."""
    file_to_share = get_object_or_404(UploadedFile, id=file_id)

    if request.method == 'POST':
        recipient_email = request.POST.get('email')  # Get email from form
        subject = f"Shared File: {file_to_share.file.name}"
        message = f"You have been shared a file: {file_to_share.file.name}\n\nDownload it here: {file_to_share.file.url}"

        try:
            # Send the email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email])
            messages.success(request, f'File shared successfully with {recipient_email}!')
            return redirect('browse')
        except Exception as e:
            messages.error(request, f'Error sharing file: {e}')
            return redirect('browse')

    return render(request, 'share_file.html', {'file': file_to_share})



@login_required
def share_folder(request, folder_id):
    """Handles sharing a folder with another user."""
    folder = get_object_or_404(Folder, id=folder_id)

    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user_to_share = User.objects.get(email=email)
            folder.shared_with.add(user_to_share)
            messages.success(request, f'Folder shared successfully with {user_to_share.username}.')
        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')

        return redirect('browse')  # Redirect to the browse view after sharing

    return render(request, 'share_folder.html', {'folder': folder})