import os
import google.generativeai as gemini_client
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from back_end.scraping import path

def vectorise(collection_name: str):  
    # Load environment variables from .env file
    load_dotenv()

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_URL = os.getenv("QDRANT_URL")

    # Configure Gemini client
    gemini_client.configure(api_key=GEMINI_API_KEY)

    # Initialize Qdrant client
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    # Function to split text into chunks
    def make_chunks(inptext: str):
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n"],
            chunk_size=1000,
            chunk_overlap=20,
            length_function=len,
        )
        chunks = text_splitter.create_documents([inptext])
        return chunks

    # Load texts from the provided file
    file_path = path
    with open(file_path, 'r', encoding='utf-8') as file:
        full_text = file.read()

    texts = make_chunks(full_text)

    # Generate embeddings using Gemini
    results = [
        gemini_client.embed_content(
            model="models/embedding-001",
            content=chunk.page_content,
            task_type="retrieval_document",
            title="Qdrant x Gemini",
        )
        for chunk in texts
    ]

    # Check if the collection already exists
    try:
        client.get_collection(collection_name=str(collection_name))
        print("Collection already exists.")
    except Exception as e:
        print("Creating collection...")
        client.create_collection(
            collection_name=str(collection_name),
            vectors_config=VectorParams(size=768, distance=Distance.COSINE)
        )

    # Prepare points to be inserted into Qdrant
    points = [
        PointStruct(
            id=idx,
            vector=result['embedding'],
            payload={"text": chunk.page_content},
        )
        for idx, (result, chunk) in enumerate(zip(results, texts))
    ]

    # Insert the points into the Qdrant collection
    client.upsert(
        collection_name=str(collection_name),
        points=points
    )

    print("Collection created and points upserted.")

    return collection_name  




