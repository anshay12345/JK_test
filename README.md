# Project Name
## Easy Installation Steps
1. **Clone the code from the Git repository:**
   git clone https://github.com/anshay12345/JK_test.git
2. **Setup .env variables from .env_example.**
3. **Install the dependencies:**
   
bash
   pip install -r requirements.txt
   
4. **Run migration commands:**
   
bash
   python manage.py makemigrations
   python manage.py migrate
   
5. **Post migration, tables will be created in the Postgres database.**
6. **Run the bash script to start the application:**
   
bash
   sh trigger.sh
   
## Easy Deployment Using Docker
1. **Run the following command to create a container and run the application:**
   
bash
   docker-compose up --build -d
   
   This command will run the container in detached mode.
2. **Check the logs of the container:**
   
bash
   docker-compose logs web
   
3. **List the containers and their status:**
   
bash
   docker-compose ps
   
4. **Stop all the containers:**
   
bash
   docker-compose down
   
   Once Docker is up, it can be accessed through the IP of the server on which it is deployed.
## Documentation
### 1. Model
- **UploadedDocument Model:**
  - Stores the local file path, name of the file, and the date of the file uploaded.
    
python
    file_name = models.CharField(max_length=255, blank=True)
    file_path = models.FileField(upload_to='document_storage/')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    
  - Customized the default save method for the UploadedDocument model. The file_name is retrieved from the file_path. This model only requires the file_path in the request to create and save an instance.
- **Embeddings Model:**
  - Stores the embeddings of the chunks created from the PDF content along with the content.
    
python
    embedding = VectorField(dimensions=1536)
    uploaded_document = models.ForeignKey(UploadedDocument, on_delete=models.CASCADE, related_name='embeddings')
    embedding_creation_date = models.DateTimeField(auto_now_add=True)
    
  - uploaded_document: Takes the reference from the UploadedDocument.
### 2. Views
- Views are asynchronous. As of now, DRF does not have much compatibility with async/await, hence a third-party library "adrf: Async Django REST framework" is used. A better approach would be to create a custom package for async/await to be used in production to avoid any end-time issues of package depreciation.
- **FileUploadView:**
  - This asynchronous class-based view accepts the file, loads it into a path, and dumps details such as file_name, file_path, and date_uploaded into the database. Once the dump is done, this view creates the embeddings of the PDF chunks and stores them in the Embeddings model. This view will throw an error response if the same file is sent again, as per the requirement of an ideal chatbot.
- **AsyncQuestionAnsweringView:**
  - This asynchronous class-based view accepts the following parameters:
    - question: Question asked by the user.
    - pdf_name: Name of the PDF from which the answer is to be given.
  - The view creates an embedding of the question and follows the RAG algorithm to find the cosine distance to fetch the most relevant document as content to be passed to the LLM and fetch the answer.
### 3. Middleware
- **ExceptionHandlingMiddleware:** Catches any exceptions created in the request/response cycle.
- **LoggingMiddleware:** Prints all the logs of the application into a file logs/application.log.
### 4. Custom Exceptions
- **BaseCustomException:** Base class for creating custom exceptions.
- **FileNotUploadedException:** Used for data validation in serializers.
### 5. Serializers
- Used for validating and serializing the data.

