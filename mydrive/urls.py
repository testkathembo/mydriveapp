from django.urls import path
from .views import register, login_view, logout_view, home_view, upload_file_view  # Include home_view
from . import views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),  # Correct path for the home view
    path('upload/', upload_file_view, name='upload_file'),
    path('download/<int:file_id>/', views.download_file, name='download'),
    path('rename/<int:file_id>/', views.rename_file, name='rename'),
    path('delete/<int:file_id>/', views.delete_file, name='delete'),
    
]



