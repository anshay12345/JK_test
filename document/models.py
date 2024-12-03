from django.db import models
import os
from pgvector.django import VectorField
# Create your models here.

class UploadedDocument(models.Model):
    """
    Model for storing details of the file.
    file_name: Name of the file
    file_path: Local Path of the file(Store it somewhere in cloud for production)
    date_uploaded: Date for the file upload
    """
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


class Embeddings(models.Model):
    """
    Model for storing embeddings of "UploadedDocument" instance.
    embedding: Stores the embeddings of the chunks of the content of document.
    uploaded_document: Many-to-one relationship, where multiple embeddings can be associated with a single uploaded document.
    embedding_creation_date: Datetime of embedding creation. 
    """

    embedding = VectorField(dimensions=1536)
    uploaded_document = models.ForeignKey(UploadedDocument, on_delete=models.CASCADE, related_name='embeddings')
    embedding_creation_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    
    def __str__(self):
        return f"Embeddings for {self.uploaded_document.file_name}"
    