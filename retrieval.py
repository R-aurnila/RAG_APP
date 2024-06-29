import os
from typing import Dict
from qdrant_client import QdrantClient
from google.generativeai import embed_content
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain.vectorstores import Qdrant

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GEMINI_API_KEY, temperature=0.9, max_output_tokens=1024, convert_system_message_to_human=True)


# Generate Prompt Template
sys_prompt = """
You are a helpful assistant to answer and guide for Gigalogy Company. Always answer as helpful and as relevant
as possible, while being informative. Keep answer length about 100-200 words.

If you don't know the answer to a question, please don't share false information.
"""
instruction = """CONTEXT:\n\n {context}\n\nQuery: {question}\n"""

QA_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=sys_prompt),
    HumanMessage(content=instruction)
])



# Initialize Qdrant client
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

# Define embedding function
def embedding_function(text: str) -> list:
    embedding = embed_content(
        model="models/embedding-001",
        content=text,
        task_type="retrieval_query",
    )["embedding"]
    return embedding

# Define vector store using the existing collection
vector_store = Qdrant(
    client=client,
    collection_name="gigalogy_rag",
    embedding_function=embedding_function
)

# Create retriever from the vector store
retriever = vector_store.as_retriever()

# Create RetrievalQA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,  # Get source
    chain_type_kwargs={"prompt": QA_prompt}
)
# Function to perform search and generate response using LLM
def perform_search(query_text: str) -> Dict:
    # Generate query embedding
    query_embedding = embedding_function(query_text)

    # Search the vector store
    search_results = client.search(
        collection_name="gigalogy_rag",
        query_vector=query_embedding,
        limit=3  # Retrieve top 3 results
    )

    # Format search results into context
    context = " ".join([result.payload["text"] for result in search_results])

    # Use the RetrievalQA chain to get the LLM response
    llm_res = qa_chain({"context": context, "question": query_text})
    return llm_res

# Example usage
if __name__ == "__main__":
    query = "What are the company policies on remote work?"
    result = perform_search(query)
    print(result)
