from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
import os
openai_api_key = os.environ.get('OPENAI_API_KEY')
def load_qa_chain(collection_name):
    # Load the vector store from disk
    vector_store = Chroma(collection_name=collection_name, embedding_function=OpenAIEmbeddings())

    # Create an instance of OpenAI language model
    llm = OpenAI(openai_api_key=openai_api_key)
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    # Create a RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="map_reduce",
        retriever=vector_store.as_retriever()
    )

    return qa_chain

def process_query(query, qa_chain):
    # Run the query through the RetrievalQA chain
    result = qa_chain.run(query)

    return result