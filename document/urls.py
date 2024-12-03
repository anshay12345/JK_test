from django.urls import path
from .views import FileUploadView, AsyncQuestionAnsweringView

urlpatterns=[
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('question-answer/', AsyncQuestionAnsweringView.as_view(), name='question-answer')
]