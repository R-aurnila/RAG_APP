import os
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Annotated
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import google.generativeai as gemini_client
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")

# Configure Gemini client
gemini_client.configure(api_key=GEMINI_API_KEY)

# Initialize Qdrant client
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

app = FastAPI()

class SearchQuery(BaseModel):
    query: str

class Document(BaseModel):
    text: str

class SearchResults(BaseModel):
    results: List[Document]

def get_client() -> QdrantClient:
    return client

@app.post("/search")
def search(query: SearchQuery, client: Annotated[QdrantClient, Depends(get_client)]) -> SearchResults:
    try:
        query_embedding = gemini_client.embed_content(
            model="models/embedding-001",
            content=query.query,
            task_type="retrieval_query",
        )["embedding"]

        search_results = client.search(
            collection_name="gigalogy_rag",
            query_vector=query_embedding,
            limit=1  # Retrieve top 5 results
        )

        return SearchResults(
            results=[
                Document(
                    text=result.payload["text"],
                    source_url=result.payload.get("source_url", "")
                )
                for result in search_results
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))