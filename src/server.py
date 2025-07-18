from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import logging
import uvicorn

import sys
sys.path.append(".")
from src.squeeze_search import search_and_play_id

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Query API", version="1.0.0")

# Request model
class QueryRequest(BaseModel):
    device_id: str
    query: str

# Response model
class QueryResponse(BaseModel):
    status: str
    device_id: str
    query: str
    response_id: str
    message: str

@app.post("/api/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    try:
        # Log the request
        logger.info(f"Received request from device: {request.device_id}, query: {request.query}")
        msg = search_and_play_id(request.query)
        logger.info(msg)
        # Process the request (customize this part for your needs)
        response_data = QueryResponse(
            status="success",
            device_id=request.device_id,
            query=request.query,
            response_id=str(uuid.uuid4()),
            message=msg
        )
        
        return response_data
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)