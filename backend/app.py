from fastapi import FastAPI, File, UploadFile, Form
from file_processing import load_documents, chunk_documents, create_embeddings
from query_processing import load_qa_chain, process_query
from dotenv import load_dotenv
import os

load_dotenv(r'C:\Users\sksha\Desktop\llm-assignment-master\llm-assignment-master\llm-assignment-master_\backend\.env')

openai_api_key = os.environ.get('OPENAI_API_KEY')
print(openai_api_key)

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows only requests from your React app
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/process-file")
async def process_file(collection_name: str = Form(...), file: UploadFile = File(...)):
    print("Received collection_name:", collection_name)
    print("Received file:", file.filename)
    # Load documents
    documents = await load_documents(file)

    # Chunk documents
    chunked_docs = chunk_documents(documents, chunk_size=500, chunk_overlap=100)

    # Create embeddings and store in Chroma
    vector_store = create_embeddings(chunked_docs, collection_name)
    preview_length = 750  # Adjust based on desired preview size
    document_previews = [doc.page_content[:preview_length] for doc in documents]  # or whatever attribute holds the content

    # Return the success message along with the document previews
    return {"message": "File processed successfully", "document_preview": document_previews}
from pydantic import BaseModel

class QueryRequest(BaseModel):
    collection_name: str
    query: str
@app.post("/query")
async def query(request: QueryRequest):
    # Load the RetrievalQA chain
    print(request.dict())
    qa_chain = load_qa_chain(request.collection_name)

    # Process the query
    result = process_query(request.query, qa_chain)

    return {"result": result}