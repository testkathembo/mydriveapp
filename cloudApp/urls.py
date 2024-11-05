# urls.py
from django.urls import path
from . import views

app_name = 'cloudApp'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_file, name='upload_file'),
    path('file/<int:file_id>/', views.file_details, name='file_details'),
]
