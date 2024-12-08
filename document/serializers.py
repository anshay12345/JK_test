from rest_framework import serializers
from .models import UploadedDocument
from .api_exceptions import FileNotUploadedException, InvalidFileTypeException
import mimetypes

class UploadedDocumentSerializer(serializers.ModelSerializer):
    """
    A Serializer class to validate incoming JSON data before converting it into a model instance.
    """

    def validate_file_path(self, value):
        """
        Validate the uploaded file to ensure it is a PDF.

        Args:
            value: The uploaded file object.

        Returns:
            value: The validated file object.

        Raises:
            ValidationError: If the file is not a PDF.
        """
        # Check if the file is uploaded
        if not value:
            raise FileNotUploadedException()

        # Access the content type of the uploaded file
        content_type = value.content_type
        
        # Validate the content type
        if content_type != 'application/pdf':
            raise InvalidFileTypeException()

        return value

    class Meta:
        model = UploadedDocument
        fields = ['id', 'file_name', 'file_path', 'date_uploaded']
        extra_kwargs = {
            'file_name': {'required': False},
        }