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
        """
        Handle POST request for accepting PDF file, creating and storing embeddings along with file details.
        Note: ***This post method is asynchronous for future reference where any call to llm function might become asynchronous.***
        """
        try:
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
                # Save the uploaded document asynchronously, this will save the data into the model table
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
                return Response(serializer.data,status=status.HTTP_201_CREATED)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {
                    'error': 'An unexpected error occurred. Please try again later.',
                    'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AsyncQuestionAnsweringView(APIView):
    """
    Asynchronous classbased view for handling the incoming request for question asked, and answers the question from the PDF using RAG.
    post: Accepts the PDF name and question asked.
    """
    
    async def post(self, request):
        """
        Handle POST request to answer a question based on the content of a specified PDF.
        Note: ***This post method is asynchronous for future reference where any call to llm function might become asynchronous.***
        """

        try:
            pdf_name = request.data.get('pdf_name')
            question = request.data.get('question')
            pdf_processor = PDFProcessor()

            if not pdf_name or not question:
                return Response({'error': 'PDF name and question are required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Retrieve the UploadedDocument instance asynchronously
            uploaded_document = await sync_to_async(get_object_or_404)(UploadedDocument, file_name=pdf_name)
            
            # Generate embeddings for the question
            question_embedding = pdf_processor.get_embedding(question)

            # Retrieve and annotate embeddings with cosine similarity
            document_embeddings = await sync_to_async(list)(
                Embeddings.objects.filter(uploaded_document=uploaded_document).annotate(
                    distance=CosineDistance("embedding", question_embedding)
                ).order_by('distance')
            )

            # Extract the most relevant chunks based on the annotated distance
            relevant_chunks = [embedding.content for embedding in document_embeddings[:3]]  # Top 3 relevant chunks

            # Generate an answer using the relevant chunks
            answer = pdf_processor.generate_answer(question, relevant_chunks)

            return Response(
                {   
                    'answer': answer,
                    'status_code': status.HTTP_200_OK
                }, 
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {
                    'error': 'An unexpected error occurred. Please try again later.',
                    'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )    



