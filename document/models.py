from django.db import models

# Create your models here.

class UploadedDocument(models.Model):
    file_name=models.CharField(max_length=255)
    file_path=models.FileField(upload_to='document_storage/')
    date_uploaded=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name