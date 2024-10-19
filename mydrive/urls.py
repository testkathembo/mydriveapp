from django.urls import path
from .views import register, login_view, home_view, logout_view, upload_file, browse_files, update_profile, manage_files, create_folder, browse_folders

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('upload/', upload_file, name='upload'),
    path('browse/', browse_files, name='browse'),
    path('profile/update/', update_profile, name='update_profile'),
    path('manage/', manage_files, name='manage_files'),  # View for managing files
    path('folders/<int:folder_id>/', browse_folders, name='browse_folder'),  # Add this line for the browse_folders view
]
