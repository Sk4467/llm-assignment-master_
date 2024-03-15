from langchain.document_loaders import PyPDFLoader, PDFMinerLoader, DirectoryLoader
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from os.path import join
import os
openai_api_key = os.environ.get('OPENAI_API_KEY')
from langchain.document_loaders import TextLoader, PDFMinerLoader, UnstructuredWordDocumentLoader, CSVLoader

def load_documents(file_path):
    if file_path.endswith('.txt'):
        loader = TextLoader(file_path)
    elif file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.doc') or file_path.endswith('.docx'):
        loader = UnstructuredWordDocumentLoader(file_path)
    elif file_path.endswith('.csv'):
        loader = CSVLoader(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")

    documents = loader.load()
    return documents
# from langchain.docstore.document import Document
# import chardet

# def load_documents(file):
#     content = file.file.read()
#     encoding = chardet.detect(content)['encoding']
#     if encoding is None:
#         encoding = 'utf-8'  # Fallback encoding
#     try:
#         content = content.decode(encoding)
#     except UnicodeDecodeError:
#         content = content.decode('latin-1')  # Fallback encoding for decoding errors
#     metadata = {'source': file.filename}
#     document = Document(page_content=content, metadata=metadata)
#     return [document]

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