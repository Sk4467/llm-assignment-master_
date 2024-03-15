from langchain.document_loaders import PyPDFLoader, PDFMinerLoader, DirectoryLoader
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from os.path import join
import os
openai_api_key = os.environ.get('OPENAI_API_KEY')
from langchain.document_loaders import TextLoader, PDFMinerLoader, UnstructuredWordDocumentLoader, CSVLoader

# def load_documents(file_path):
#     if file_path.endswith('.txt'):
#         loader = TextLoader(file_path)
#     elif file_path.endswith('.pdf'):
#         loader = PyPDFLoader(file_path)
#     elif file_path.endswith('.doc') or file_path.endswith('.docx'):
#         loader = UnstructuredWordDocumentLoader(file_path)
#     elif file_path.endswith('.csv'):
#         loader = CSVLoader(file_path)
#     else:
#         raise ValueError(f"Unsupported file format: {file_path}")

#     documents = loader.load()
#     return documents
from fastapi import UploadFile
import fitz  # PyMuPDF
from langchain.docstore.document import Document

def load_documents(file: UploadFile):
    # Assuming the input 'file' is an UploadFile from FastAPI which contains a PDF
    try:
        # Save temporary file to read with PyMuPDF
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(file.file.read())

        # Open the PDF with PyMuPDF
        doc = fitz.open(temp_file_path)
        content = ""
        for page in doc:
            content += page.get_text()

        # Cleanup: close the document and remove the temporary file
        doc.close()
        os.remove(temp_file_path)
    except Exception as e:
        # Handle exceptions, such as file read errors or if the file is not a PDF
        print(f"Error processing document: {e}")
        content = "Error processing document."

    metadata = {'source': file.filename}
    document = Document(page_content=content, metadata=metadata)
    return [document]


from langchain.text_splitter import CharacterTextSplitter

def chunk_documents(documents, chunk_size=1000, chunk_overlap=200):
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunked_docs = text_splitter.split_documents(documents)
    return chunked_docs


from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

def create_embeddings(chunked_docs, collection_name):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vector_store = Chroma.from_documents(chunked_docs, embeddings, collection_name=collection_name)
    vector_store.persist()

    return vector_store