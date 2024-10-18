from django.urls import path
from .views import register, login_view, home_view, logout_view  # Import the logout_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='logout'),  # Add this line for logout
]
