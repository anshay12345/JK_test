from django.contrib import admin
from .models import UploadedDocument,Embeddings
# Register your models here.
admin.site.register(UploadedDocument)
admin.site.register(Embeddings)