from django.shortcuts import render
import os
# Create your views here.
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import UploadedDocument, Embeddings
from .serializers import UploadedDocumentSerializer
from langchain_community.document_loaders import PyMuPDFLoader
from .llm_utils import PDFProcessor
from asgiref.sync import sync_to_async
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import F, Func, FloatField
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import sync_to_async
import asyncio
from adrf.views import APIView
from pgvector.django import CosineDistance


@method_decorator(csrf_exempt, name='dispatch')
class FileUploadView(APIView):
    """
    Asynchronous Classbased view for handling the PDF file received in the request, creating embeddings of it and storing them in the model tables. 
    post: Accepts the request and process the logic
    """
    parser_classes = [MultiPartParser, FormParser]

    async def post(self, request):
        file_obj = request.FILES.get('file_path')
        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Extract the filename from the file object
        file_name = file_obj.name

        # Check if a document with the same name already exists
        existing_document = await sync_to_async(UploadedDocument.objects.filter(file_name=file_name).exists)()
        if existing_document:
            return Response({'error': 'A document with the same name already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UploadedDocumentSerializer(data=request.data)

        if serializer.is_valid():
            # Save the uploaded document asynchronously
            uploaded_document = await sync_to_async(serializer.save)()

            # Retrieve the file object asynchronously
            file_obj = await sync_to_async(UploadedDocument.objects.get)(file_name=uploaded_document.file_name)

            pdf_processor = PDFProcessor()
            documents = pdf_processor.read_and_chunk_pdf(uploaded_document.file_path.path)

            for document in documents:
                # Get embedding asynchronously if possible
                embedding = pdf_processor.get_embedding(document)

                # Create embedding record asynchronously
                await sync_to_async(Embeddings.objects.create)(
                    embedding=embedding,
                    uploaded_document=file_obj,
                    content=document
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




