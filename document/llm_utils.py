from langchain_community.document_loaders import PyMuPDFLoader
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()



import os
import asyncio

class PDFProcessor:
    def __init__(self):
        self.engine = os.getenv('TEXT_EMBEDDING_ENGINE')
        self.openai = AzureOpenAI(
            azure_endpoint=os.getenv('AZUREOPENAI_HOST'),
            api_key=os.getenv('AZUREOPENAI_KEY'),
            api_version=os.getenv('API_VERSION')
        )

    def read_and_chunk_pdf(self, file_path):
        """
        Reads a PDF file and returns a list of text chunks.
        """
        loader = PyMuPDFLoader(file_path)
        documents = loader.load()
        documents_content = [document.page_content for document in documents]
        return documents_content

    def get_embedding(self, text):
        """
        Create embeddings using AzureOpenAI
        """
        engine = self.engine
        openai_instance = self.openai
        response = openai_instance.embeddings.create(input=text, model=engine)
        return response.data[0].embedding

    def generate_answer(self, user_query, relevant_chunks):
        content = "You answer the question asked. Give the answer from the given text input."
        
        introduction = """
        Use the information provided from the PDF as given below and answer the following question.
        ***IMPORTANT POINTS FOR ANSWERING THE QUESTION***
        1: Read the information provided very carefully and answer from it only. Do not create your own answer which is not present in the context provided.
        2: Give the answer only from the information provided in the below context passed.
        3: If you could not find answer, just write "I could not find an answer."
        """

        question = f"\n\nQuestion: {user_query}"
        message = introduction
        
        for content in relevant_chunks:
            next_article = f'\n\n Content from the PDF\n"""\n{content}\n"""'
            message += next_article

        answer = self.chat(message + question, content=content)
        return answer

    def chat(self, query, content):
        """Answers a query using GPT and a dataframe of relevant texts and embeddings."""
        messages = [
            {"role": "system", "content": content},
            {"role": "user", "content": query},
        ]
        response = self.openai.chat.completions.create(
            model='gpt-35-turbo-16k',
            messages=messages,
            temperature=0
        )

        response_message = response.choices[0].message.content
        return response_message
    