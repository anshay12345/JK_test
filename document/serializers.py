from rest_framework import serializers
from .models import UploadedDocument

class UploadedDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model=UploadedDocument
        fields=['id', 'file_name', 'file_path', 'date_uploaded']
        extra_kwargs={
            'file_name': {'required': False},
        }
