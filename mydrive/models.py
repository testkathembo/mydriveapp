from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='Unnamed')  # Set a default value for existing records
    file = models.FileField(upload_to='uploads/', default=None, blank=True, null=True)  # Allow file to be optional
    uploaded_at = models.DateTimeField(auto_now=True)
    storage_used = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name



class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.file.name