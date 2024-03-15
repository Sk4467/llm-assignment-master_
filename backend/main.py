# from dotenv import load_dotenv
# from typing import Any
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import RAG
# # Load environment variables from .env file (if any)
# load_dotenv()


# class Response(BaseModel):
#     result: str | None

# class UserQuery(BaseModel):
#     messages: str

# origins = [
#     "http://localhost",
#     "http://localhost:8080",
#     "http://localhost:3000"
# ]

# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# initialize_model()
# # @app.post("/predict", response_model = Response)
# # def predict() -> Any:
  
# #   #implement this code block
  
# #   return {"result": "hello world!"}
# # @app.get("/hello")
# # async def hello():
# #     return 'Hello World'
# @app.post("/home")
# def home_route(home: UserQuery):
#     try:
#         if not home.messages:
#             raise HTTPException(status_code=400, detail="Empty value")

#         # Call the custom function to generate a response using RetrievalQA
#         answer, generation = generate_response(home.messages)

#         return {"response": answer, "reasoning": generation}
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")
    

from file_processing import load_documents, chunk_documents, create_embeddings
from query_processing import load_qa_chain, process_query
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    file_path = r'C:\Users\sksha\Desktop\llm-assignment-master\llm-assignment-master\backend\files\Option for Residence Accommodation.pdf'
    collection_name = 'my_collection'

    # Load documents
    documents = load_documents(file_path)

    # Chunk documents
    chunked_docs = chunk_documents(documents, chunk_size=500, chunk_overlap=100)

    # Create embeddings and store in Chroma
    vector_store = create_embeddings(chunked_docs, collection_name)

    # Load the RetrievalQA chain
    qa_chain = load_qa_chain(collection_name)

    # Process user queries
    while True:
        query = input("Enter your query (or 'exit' to quit): ")
        if query.lower() == 'exit':
            break

        result = process_query(query, qa_chain)
        print(result)

if __name__ == '__main__':
    main()