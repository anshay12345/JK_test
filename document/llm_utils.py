from langchain_community.document_loaders import PyMuPDFLoader
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()



class PDFProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.engine=os.getenv('TEXT_EMBEDDING_ENGINE')
        self.openai = AzureOpenAI(
            azure_endpoint = os.getenv('AZUREOPENAI_HOST'),
            api_key = os.getenv('AZUREOPENAI_KEY'),
            api_version = os.getenv('API_VERSION')
        )


    def read_and_chunk_pdf(self):
        """
        Reads a PDF file and returns a list of text chunks.
        """
        loader = PyMuPDFLoader(self.file_path)
        documents = loader.load() 
        documents_content = [document.page_content for document in documents]
        return documents_content

    def get_embedding(self, text):
        """
        Create embeddings using AzureOpenAI
        """
        engine=self.engine
        openai_instance=self.openai
        response = openai_instance.embeddings.create(input=text, model=engine)
        return response.data[0].embedding

    
    