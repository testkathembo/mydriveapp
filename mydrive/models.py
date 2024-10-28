from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UploadedFile(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    last_modified = models.DateTimeField(auto_now=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)
    original_location = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.name if self.name else "Unnamed File"

    def save(self, *args, **kwargs):
        # This ensures file_size is updated every time you save the object
        if self.file:
            self.file_size = self.file.size  # Update file_size
        super().save(*args, **kwargs)
