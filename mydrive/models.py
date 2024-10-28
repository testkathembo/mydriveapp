from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UploadedFile(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)  # Allow blanks for name
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    last_modified = models.DateTimeField(auto_now=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)  # File size can be null or blank
    original_location = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to='uploads/')  # File upload path


    def __str__(self):
        return self.name if self.name else "Unnamed File"

    def save(self, *args, **kwargs):
        # This ensures file_size is updated every time you save the object
        if self.file:
            self.file_size = self.file.size  # Update file_size
        super().save(*args, **kwargs)
