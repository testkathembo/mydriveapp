from django.urls import path
from .views import (
    register,
    login_view,
    home_view,
    logout_view,
    upload_file,
    browse_files,
    update_profile,
    manage_files,
    create_folder,
    browse_folders,
    move_file, 
    copy_file,
    delete_file,
    delete_folder,
    share_file,
    share_folder
    
    )

urlpatterns = [
    # User authentication URLs
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # User dashboard URLs
    path('home/', home_view, name='home'),
    
    # File management URLs
    path('upload/', upload_file, name='upload'),
    path('browse/', browse_files, name='browse'),
    path('manage/', manage_files, name='manage_files'),  # View for managing files

    # Profile management URLs
    path('profile/update/', update_profile, name='update_profile'),

    # Folder management URLs
    path('folders/<int:folder_id>/', browse_folders, name='browse_folder'),  # View for browsing folders
    path('create-folder/', create_folder, name='create_folder'),  # Added route for folder creation
    
    # Management of copies of files and folders
    path('move-file/<int:file_id>/', move_file, name='move_file'),
    path('copy-file/<int:file_id>/', copy_file, name='copy_file'),
    path('delete-file/<int:file_id>/', delete_file, name='delete_file'),
    path('delete-folder/<int:folder_id>/', delete_folder, name='delete_folder'),  # New delete folder path
    
    # Share files and folders
    path('share-file/<int:file_id>/', share_file, name='share_file'),  # URL for sharing files
    path('share-folder/<int:folder_id>/', share_folder, name='share_folder'),  # URL f
]


