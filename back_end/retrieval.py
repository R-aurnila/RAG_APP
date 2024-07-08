import os
import logging
from qdrant_client import QdrantClient
import google.generativeai as gemini_client
from langchain_qdrant import Qdrant
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.schema import SystemMessage, HumanMessage
import re
import textwrap
from langchain_core.messages.ai import AIMessage

# Configure logging
# logging.basicConfig(level=logging.DEBUG)

def load_environment_variables():
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_URL = os.getenv("QDRANT_URL")
    return GEMINI_API_KEY, QDRANT_API_KEY, QDRANT_URL

def initialize_llm(gemini_api_key):
    return ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=gemini_api_key,
        temperature=0.9,
        max_output_tokens=1024,
        convert_system_message_to_human=True
    )

def perform_search(collection_name, query):
    # Load environment variables
    GEMINI_API_KEY, QDRANT_API_KEY, QDRANT_URL = load_environment_variables()
    llm = initialize_llm(GEMINI_API_KEY)
 
    
    # Define the System Prompt
    sys_prompt = """
        You are a helpful assistant for Gigalogy Company, dedicated to providing accurate and relevant information within the context provided."
        "Please aim for answers between 100-300 words, prioritizing helpfulness and accuracy. If a question falls outside the 'Context' given, "
        "look for the closest match in the context and if that makes sense use that or else avoid providing inaccurate information. "
        "Instead, politely indicate that the question is beyond the scope of the provided context."
        "If you don't know the answer, just say that you don't know. Do not try to make up an answer."
        "if you find the accurate answer, please just say that and you can also give some additional information related to the context."
    """
    
    try:
        # Retrieve relevant documents from the vector store
        # results = retriever.invoke(query)
        gemini_client.configure(api_key=GEMINI_API_KEY)
        client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

        results = client.search(
            collection_name=collection_name,
            query_vector=gemini_client.embed_content(
                model="models/embedding-001",
                content=query,
                task_type="retrieval_query",
            )["embedding"],
        )
        
        # Extract the relevant content from the documents
        # context = ' '.join([doc.payload['content'] for doc in results if 'content' in doc.payload])
       
        # print(results)
        
        # Construct the prompt using SystemMessage and HumanMessage
        prompt_messages = [
            SystemMessage(content=sys_prompt),
            HumanMessage(content=f"CONTEXT:\n\n{results}\n\nQuery: {query}\n")
        ]
        
        # Generate the response using the LLM with the context
        response = llm(prompt_messages)
        
    except Exception as e:
        print(f"Error occurred while performing search: {e}")
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

#Example query
# collection_name = "gigalogy_rag"
# query = "tell me about career in gigalogy"
# response = perform_search(collection_name, query)
# # print(response)

# result = handle_result(response)
# print(result)

