from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# views.py
from django.shortcuts import render, redirect
from .models import File, Folder, SharedFile
from django.contrib.auth.decorators import login_required
from .forms import FileUploadForm

@login_required
def dashboard(request):
    folders = Folder.objects.filter(user=request.user)
    files = File.objects.filter(user=request.user)
    return render(request, 'Templates/drive/dashboard.html', {'folders': folders, 'files': files})

@login_required
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        folder_id = request.POST.get('folder')
        folder = Folder.objects.get(id=folder_id) if folder_id else None
        new_file = File.objects.create(name=uploaded_file.name, file=uploaded_file, folder=folder, user=request.user)
        return redirect('drive:dashboard')
    return render(request, 'drive/upload_file.html')

@login_required
def file_details(request, file_id):
    file = File.objects.get(id=file_id)
    return render(request, 'drive/file_details.html', {'file': file})
