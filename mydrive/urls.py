from django.urls import path
from .views import register, login_view, logout_view, home_view, upload_file_view  # Include home_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),  # Correct path for the home view
    path('upload/', upload_file_view, name='upload_file'),
    # Add other URLs as needed
]

