from fastapi import APIRouter
from app.services.query_engine import handle_query
from app.models.request_models import ChatRequest

router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest):
    result = await handle_query(request.question)
    return result