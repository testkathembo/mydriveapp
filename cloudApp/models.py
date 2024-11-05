from django.db import models

# Create your models here.
# models.py
from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='folders', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    folder = models.ForeignKey(Folder, related_name='files', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class SharedFile(models.Model):
    file = models.ForeignKey(File, related_name='shared_with', on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User, related_name='shared_files', on_delete=models.CASCADE)
    permission = models.CharField(max_length=20, choices=[('view', 'View'), ('edit', 'Edit')])

    def __str__(self):
        return f"Shared with {self.shared_with.username}"
