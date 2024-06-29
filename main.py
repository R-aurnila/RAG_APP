import os
from fastapi import APIRouter, HTTPException, FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from retrieval import perform_search

# Initialize FastAPI router
router = APIRouter()

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")

# Initialize Qdrant client
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

class InputData(BaseModel):
    input_text: str

@router.post("/ask")
async def ask(question: InputData):
    try:
        result = perform_search(client, question.input_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Initialize FastAPI app
app = FastAPI()
app.include_router(router)
