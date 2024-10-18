from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import register, login_view, home_view, logout_view, upload_file, browse_files, update_profile
from .views import manage_files  # Import the manage_files view


    

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('upload/', upload_file, name='upload'),
    path('browse/', browse_files, name='browse'),
    path('profile/update/', update_profile, name='update_profile'),
    path('manage/', manage_files, name='manage_files'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
