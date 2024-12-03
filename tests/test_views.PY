from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from document.models import UploadedDocument 

class FileUploadAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.upload_url = reverse('upload')

    def test_file_upload(self):
        # Creating a simple PDF file in memory with a specific filename
        file_content = b'%PDF-1.4\n%âãÏÓ\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n'
        file = SimpleUploadedFile("Anshay_Rastogi_Resume_BJCa2RA.pdf", file_content, content_type="application/pdf")

        # Make a POST request to the upload endpoint
        response = self.client.post(self.upload_url, {'file_path': file}, format='multipart')

        # Check that the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the file was saved in the database
        self.assertTrue(UploadedDocument.objects.filter(file_name="Anshay_Rastogi_Resume_BJCa2RA.pdf").exists())

    def test_duplicate_file_upload(self):
        # Create and upload a file
        file_content = b'%PDF-1.4\n%âãÏÓ\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n'
        file = SimpleUploadedFile("Anshay_Rastogi_Resume_BJCa2RA.pdf", file_content, content_type="application/pdf")
        self.client.post(self.upload_url, {'file_path': file}, format='multipart')

        # Attempt to upload the same file again
        response = self.client.post(self.upload_url, {'file_path': file}, format='multipart')

        # Check that the response status code is 400 Bad Request due to duplicate
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('A document with the same name already exists', response.data['error'])

class AsyncQuestionAnsweringViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('question-answer') 

        # Create a test PDF document
        self.uploaded_document = UploadedDocument.objects.create(
            file_name="Anshay_Rastogi_Resume_BJCa2RA.pdf",
            file_path=SimpleUploadedFile("Anshay_Rastogi_Resume_BJCa2RA.pdf", b"dummy content", content_type="application/pdf")
        )

        # Create test embeddings
        self.embeddings = [
            Embeddings.objects.create(
                uploaded_document=self.uploaded_document,
                embedding=np.random.rand(768).tolist(),  # Assuming 768-dimensional embeddings
                content="This is a test content chunk."
            )
            for _ in range(5)
        ]

    def test_question_answering(self):
        # Mock the PDFProcessor methods if necessary
        pdf_processor = PDFProcessor()
        pdf_processor.get_embedding = lambda x: np.random.rand(768).tolist()
        pdf_processor.generate_answer = lambda q, c: "This is a mock answer."

        # Send a POST request with a PDF name and a question
        response = self.client.post(self.url, {
            'pdf_name': "Anshay_Rastogi_Resume_BJCa2RA.pdf",
            'question': "What is the test content written in the file?"
        }, format='json')

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the answer in the response
        self.assertEqual(response.data['answer'], "This is a mock answer.")