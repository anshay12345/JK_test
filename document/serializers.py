from rest_framework import serializers
from .models import UploadedDocument
from .api_exceptions import FileNotUploadedException


class UploadedDocumentSerializer(serializers.ModelSerializer):

    def validate(self, data):
        """
        Overriding the default validator.
        FileNotUploadedException: Customised exception created
        """
        if 'file_path' not in data.keys() or data['file_path'] is None:
            raise FileNotUploadedException()

        return data

    class Meta:
        model=UploadedDocument
        fields=['id', 'file_name', 'file_path', 'date_uploaded']
        extra_kwargs={
            'file_name': {'required': False},
        }
