from fastapi import FastAPI, File, UploadFile, Form
from file_processing import load_documents, chunk_documents, create_embeddings
from query_processing import load_qa_chain, process_query
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.environ.get('OPENAI_API_KEY')

app = FastAPI()

@app.post("/process-file")
async def process_file(collection_name: str = Form(...), file: UploadFile = File(...)):
    # Load documents
    documents = load_documents(file)

    # Chunk documents
    chunked_docs = chunk_documents(documents, chunk_size=500, chunk_overlap=100)

    # Create embeddings and store in Chroma
    vector_store = create_embeddings(chunked_docs, collection_name)

    return {"message": "File processed successfully"}

@app.post("/query")
async def query(collection_name: str = Form(...), query: str = Form(...)):
    # Load the RetrievalQA chain
    qa_chain = load_qa_chain(collection_name)

    # Process the query
    result = process_query(query, qa_chain)

    return {"result": result}