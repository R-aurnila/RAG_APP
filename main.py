import os
from fastapi import APIRouter, HTTPException, FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from retrieval import perform_search, handle_result
from scraping import scrape_website
from vectorise import vectorise
import asyncio

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


@router.post("/URL")
async def scrape(url: InputData):
    try:
        await scrape_website(url.input_text)
        return {"message": "Scraping completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
    
@router.post("/collection")
async def ask(collection_name: InputData):
    try:
        return vectorise(collection_name.input_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))     

@router.post("/ask")
async def ask(question: InputData):
    try:
        result = perform_search(question.input_text)
        response = handle_result(result)  # Get the handled result
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Initialize FastAPI app
app = FastAPI()
app.include_router(router)
