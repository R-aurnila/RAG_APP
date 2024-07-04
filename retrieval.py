import os
import logging
from typing import List
from qdrant_client import QdrantClient
from langchain_qdrant import Qdrant
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.schema import SystemMessage, HumanMessage
import re
import textwrap
from langchain_core.messages.ai import AIMessage

# Configure logging
# logging.basicConfig(level=logging.DEBUG)

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
    embeddings=gemini_embeddings
)

# Define the Retriever
retriever = vector_store.as_retriever()

# Define the System Prompt
sys_prompt = """
You are a helpful assistant to answer and guide for Gigalogy Company. Always answer as helpful and as relevant
as possible, while being informative. Keep answer length about 100-200 words.

If you don't know the answer to a question, please don't share false information.
"""

# Function to perform search and generate response using LLM
def perform_search(query: str):
    # logging.debug(f"Performing search for query: {query}")
    if not isinstance(query, str):
        query = str(query)
    try:
        # Retrieve relevant documents from the vector store
        results = retriever.invoke(query)  # Pass the query directly as a string
        # logging.debug(f"Results from retriever: {results}")

        # Extract the relevant content from the documents
        context = ' '.join([doc.page_content for doc in results if doc.page_content])
        # logging.debug(f"Context extracted from documents: {context}")

        # Construct the prompt using SystemMessage and HumanMessage
        prompt_messages = [
            SystemMessage(content=sys_prompt),
            HumanMessage(content=f"CONTEXT:\n\n{context}\n\nQuery: {query}\n")
        ]

        # Generate the response using the LLM with the context
        response = llm(prompt_messages)
        # logging.debug(f"Generated response: {response}")

    except Exception as e:
        logging.error(f"Error occurred while performing search: {e}")
        raise e
    
    return response

def display_content(text, width=80):
    # Use regular expressions to split on either single or double newlines
    delimiters = r'(\n\n|\n)'
    tokens = re.split(delimiters, text)

    # Initialize a list to store the wrapped lines
    wrapped_lines = []

    for token in tokens:
        # Check if the token is a delimiter
        if token in ['\n', '\n\n']:
            # Add the delimiter directly to the list
            wrapped_lines.append(token)
        else:
            # Wrap the text token to the specified width
            wrapped_text = textwrap.fill(token, width=width)
            wrapped_lines.append(wrapped_text)

    # Join the wrapped lines, preserving double newlines where appropriate
    formatted_text = ''.join(wrapped_lines)
    
    return formatted_text

# Function to handle AIMessage and display its content
def handle_result(result):
    if isinstance(result, AIMessage):
        content = result.content  # Extract the content from the AIMessage
        response = display_content(content)
        return response
    else:
        print("The result is not an instance of AIMessage.")

# Example query
# query_text = "What are the company policies on remote work?"
# if not isinstance(query_text, str):
#     query_text = str(query_text)
# result = perform_search(query_text)
# handle_result(result)
