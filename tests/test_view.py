from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from document.models import UploadedDocument, Embeddings

class FileUploadViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('file-upload')

    def test_file_upload_success(self):
        # Use a valid PDF file for testing
        with open('/home/centos/Test/JK_test/media/document_storage/test.pdf', 'rb') as pdf_file:
            pdf_content = pdf_file.read()
            pdf_file = SimpleUploadedFile("test.pdf", pdf_content, content_type="application/pdf")

            # Make a POST request with the file
            response = self.client.post(self.url, {'file_path': pdf_file}, format='multipart')

            # Check that the response is 201 CREATED
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            # Check that the document was created in the database
            self.assertTrue(UploadedDocument.objects.filter(file_name="test.pdf").exists())

            # Check that embeddings were created
            uploaded_document = UploadedDocument.objects.get(file_name="test.pdf")
            self.assertTrue(Embeddings.objects.filter(uploaded_document=uploaded_document).exists())
    

    def test_file_upload_no_file(self):
        # Make a POST request without a file
        response = self.client.post(self.url, {}, format='multipart')

        # Check that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'No file provided')

    def test_file_upload_duplicate_file(self):
        # Create and save a document with the same name to simulate a duplicate
        existing_document = UploadedDocument.objects.create(
            file_name="test.pdf",
            file_path="document_storage/test.pdf"
        )

        # Use a valid PDF file for testing
        with open('/home/centos/Test/JK_test/media/document_storage/test.pdf', 'rb') as pdf_file:
            pdf_content = pdf_file.read()
            pdf_file = SimpleUploadedFile("test.pdf", pdf_content, content_type="application/pdf")

            # Make a POST request with the file
            response = self.client.post(self.url, {'file_path': pdf_file}, format='multipart')

            # Check that the response is 400 BAD REQUEST
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('A document with the same name already exists', response.data['error'])