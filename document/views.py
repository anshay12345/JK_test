from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import UploadedDocument
from .serializers import UploadedDocumentSerializer


class FileUploadView(APIView):
    parser_classes=[MultiPartParser, FormParser]

    def post(self, request):
        file_obj=request.FILES.get('file_path')

        if not file_obj:
            return Response({'error':'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer=UploadedDocumentSerializer(
            data={
                "file_name": request.FILES['file_path'].name,
                "file_path": request.FILES['file_path']
            }
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
