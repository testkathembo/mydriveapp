from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255, default='Unnamed')
    uploaded_at = models.DateTimeField(auto_now=True)
    storage_used = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def update_storage(self, file_size):
        """Update storage used by adding the size of the uploaded file."""
        self.storage_used += file_size
        self.save()

class Folder(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='folders')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_folder = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subfolders')  # Corrected self-reference
    shared_with = models.ManyToManyField(User, related_name='shared_folders', blank=True)

    def __str__(self):
        return self.name

class UploadedFile(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='files')  # Correctly references Folder
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    shared_with = models.ManyToManyField(User, related_name='shared_files', blank=True)

    def __str__(self):
        return self.file.name

    def save(self, *args, **kwargs):
        """Override save method to update storage when a file is uploaded."""
        super().save(*args, **kwargs)
        # Update the storage used in the associated profile
        self.folder.profile.update_storage(self.file.size)
