# API routes for chat requests.
from fastapi import APIRouter

from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chatbot_service import chat_with_metadata

router = APIRouter()


@router.post("/", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    Handle a chat request and return the generated answer.
    """
    result = chat_with_metadata(request.question, top_k=request.top_k)
    return ChatResponse(
        answer=result.answer,
        answer_mode=result.answer_mode,
        source_chunks=result.source_chunks,
    )
