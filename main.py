import os
from fastapi import APIRouter, HTTPException, FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from back_end.retrieval import perform_search, handle_result
from back_end.scraping import scrape_website
from back_end.vectorise import vectorise


global_collection_name = None

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
async def vectorize(collection_name: InputData):
    global global_collection_name
    try:
        global_collection_name = vectorise(collection_name.input_text)
        return {"message": "Vectorization completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))     

@router.post("/ask")
async def ask(question: InputData):
    global global_collection_name
    try:
        if global_collection_name is None:
            raise HTTPException(status_code=400, detail="Collection name not set")
        result = perform_search(global_collection_name, question.input_text)
        response = handle_result(result)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Initialize FastAPI app
app = FastAPI()
app.include_router(router)

# Serve static files from the frontend build directory
app.mount("/", StaticFiles(directory="front_end/dist", html=True), name="static")
