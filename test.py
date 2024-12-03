from langchain_community.document_loaders import PyMuPDFLoader

#from project.app import MyDocument

file_path = "/home/centos/Test/JK_test/media/document_storage/Anshay_Rastogi_Resume_FW7xW5k.pdf"
loader = PyMuPDFLoader(file_path)
documents = loader.load() 
documents_content = [document.page_content for document in documents]
print(len(documents_content))
#print(documents)