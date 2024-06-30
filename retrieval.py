import os
from typing import List
from qdrant_client import QdrantClient
from langchain_qdrant import Qdrant
from langchain_core.runnables import RunnableLambda
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=GEMINI_API_KEY,
    temperature=0.9,
    max_output_tokens=1024,
    convert_system_message_to_human=True
)

# Define the Google Generative AI Embeddings with the specified model
gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GEMINI_API_KEY)

# Define vector store using the existing collection and the embeddings instance
vector_store = Qdrant(
    client=QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY),
    collection_name="gigalogy_rag",
    embeddings=gemini_embeddings  # Pass the embeddings instance
)

# Define the Retriever
retriever = vector_store.as_retriever()

# Define the Prompt Template
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

# Define the RunnableSequence
qa_chain = (
    # Step to retrieve relevant documents
    RunnableLambda(
        func=lambda inputs: retriever.invoke({'query': inputs['question']})
    )
    # Step to generate the context
    | RunnableLambda(
        func=lambda inputs: {
            'context': ' '.join([doc.page_content for doc in inputs['results']]),
            'question': inputs['question']
        }
    )
    # Step to format the context and question for the LLM
    | RunnableLambda(
        func=lambda inputs: QA_prompt.format_prompt(
            context=inputs['context'],
            question=inputs['question']
        )
    )
    # Step to generate the answer using LLM
    | llm
)

# Function to perform search and generate response using LLM
def perform_search(query_text: str) -> str:
    result = qa_chain.invoke({'question': query_text})
    return result['text']

# Example usage
if __name__ == "__main__":
    query = "What are the company policies on remote work?"
    result = perform_search(query)
    print(result)
