from django.db import models
import os
# Create your models here.

class UploadedDocument(models.Model):
    file_name=models.CharField(max_length=255, blank=True)
    file_path=models.FileField(upload_to='document_storage/')
    date_uploaded=models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Override the save method to ensure that the file_name
        is set to the base name of the uploaded file_path.
        """
        if self.file_path:
            self.file_name = os.path.basename(self.file_path.name)  # Extract file name from file_path
        super().save(*args, **kwargs)  # Call the parent class's save method

    def __str__(self):
        return self.file_name