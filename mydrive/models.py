from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    last_modified = models.DateTimeField(auto_now=True)
    file_size = models.PositiveIntegerField(blank=True, null=True)
    original_location = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to='uploads/')

    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size  # Automatically set file size
            self.original_location = self.file.name  # Set original location to file name
        super(UploadedFile, self).save(*args, **kwargs)
