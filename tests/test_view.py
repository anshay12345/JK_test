from django.test import TestCase, AsyncClient
from rest_framework import status
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from document.models import UploadedDocument, Embeddings
from asgiref.sync import sync_to_async
import numpy as np
from django.shortcuts import get_object_or_404


class FileUploadViewTest(TestCase):
    """
    Test case for the asynchronous file upload view.
    """

    def setUp(self):
        """
        Set up the test client and URL for the file upload view.
        """
        self.client = AsyncClient()
        self.url = reverse('file-upload')

    async def test_file_upload_success(self):
        """
        Test successful file upload.

        This test uploads a valid PDF file and checks if the file is successfully
        stored in the database and if embeddings are created.
        """
        # Use a valid PDF file for testing
        with open('/home/centos/Test/JK_test/media/document_storage/STPH_JIRA.pdf', 'rb') as pdf_file:
            pdf_content = pdf_file.read()
            pdf_file = SimpleUploadedFile("test.pdf", pdf_content, content_type="application/pdf")

            # Make a POST request with the file
            response = await self.client.post(self.url, {'file_path': pdf_file}, format='multipart')

            # Check that the response is 201 CREATED
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            # Check that the document was created in the database
            document_exists = await sync_to_async(UploadedDocument.objects.filter(file_name="test.pdf").exists)()
            self.assertTrue(document_exists)

            # Check that embeddings were created
            uploaded_document = await sync_to_async(UploadedDocument.objects.get)(file_name="test.pdf")
            embeddings_exist = await sync_to_async(Embeddings.objects.filter(uploaded_document=uploaded_document).exists)()
            self.assertTrue(embeddings_exist)

    async def test_file_upload_no_file(self):
        """
        Test file upload with no file provided.

        This test attempts to upload without a file and checks if the response
        indicates a bad request due to missing file.
        """
        # Make a POST request without a file
        response = await self.client.post(self.url, {}, format='multipart')

        # Check that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'No file provided')

    async def test_file_upload_duplicate_file(self):
        """
        Test file upload with a duplicate file name.

        This test uploads a file with a name that already exists in the database
        and checks if the response indicates a bad request due to duplication.
        """
        # Create and save a document with the same name to simulate a duplicate
        await sync_to_async(UploadedDocument.objects.create)(
            file_name="test.pdf",
            file_path="document_storage/test.pdf"
        )

        # Use a valid PDF file for testing
        with open('/home/centos/Test/JK_test/media/document_storage/STPH_JIRA.pdf', 'rb') as pdf_file:
            pdf_content = pdf_file.read()
            pdf_file = SimpleUploadedFile("test.pdf", pdf_content, content_type="application/pdf")

            # Make a POST request with the file
            response = await self.client.post(self.url, {'file_path': pdf_file}, format='multipart')

            # Check that the response is 400 BAD REQUEST
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('A document with the same name already exists', response.data['error'])




class AsyncQuestionAnsweringViewTest(TestCase):
    
    def setUp(self):
        
        self.pdf_name = 'STPH_JIRA.pdf'
        self.question = 'What is the main topic of the document?'
        self.client = AsyncClient()
        self.url = reverse('question-answer')

    async def test_post_question_answering(self):
        
        # Assuming the PDF file is already uploaded and processed
        uploaded_document = await sync_to_async(get_object_or_404)(UploadedDocument, file_name=self.pdf_name)
        

        # Create a dummy 1536-dimensional embedding for testing
        dummy_embedding = np.random.rand(1536).tolist()  # Generates a random vector with 1536 dimensions

        # Create some dummy embeddings for testing
        await sync_to_async(Embeddings.objects.create)(
            uploaded_document=uploaded_document,
            embedding=dummy_embedding,  # Example embedding vector
            content='This is a relevant chunk of text from the PDF.'
        )

        
        response = await self.client.post(self.url, data={
            'pdf_name': self.pdf_name,
            'question': self.question
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('answer', response.json())
        self.assertIn('status_code', response.json())
        self.assertEqual(response.json()['status_code'], 200)

