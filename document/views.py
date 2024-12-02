from django.shortcuts import render
import os
# Create your views here.
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import UploadedDocument, Embeddings
from .serializers import UploadedDocumentSerializer
from langchain_community.document_loaders import PyMuPDFLoader
from .llm_utils import PDFProcessor
from asgiref.sync import sync_to_async

class FileUploadView(APIView):
    parser_classes=[MultiPartParser, FormParser]

    def post(self, request):
        file_obj=request.FILES.get('file_path')

        if not file_obj:
            return Response({'error':'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer=UploadedDocumentSerializer(data=request.data)

        if serializer.is_valid():
            uploaded_document=serializer.save()
            file_obj = UploadedDocument.objects.get(file_name=uploaded_document.file_name)
            pdf_processor = PDFProcessor(uploaded_document.file_path.path)
            documents=pdf_processor.read_and_chunk_pdf()
            for document in documents: 
                embedding=pdf_processor.get_embedding(document)   
                Embeddings.objects.create(
                    embedding=embedding, 
                    uploaded_document=file_obj, 
                    content=document
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


