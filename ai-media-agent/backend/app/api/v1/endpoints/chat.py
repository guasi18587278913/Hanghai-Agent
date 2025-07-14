"""
聊天问答API
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.services.chat_service import ChatService

router = APIRouter()


class ChatRequest(BaseModel):
    """聊天请求"""
    message: str
    user_id: Optional[str] = None
    context: Optional[List[dict]] = []


class ChatResponse(BaseModel):
    """聊天响应"""
    answer: str
    sources: List[dict] = []
    suggestions: List[str] = []


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """处理用户问题"""
    service = ChatService()
    result = await service.process_question(
        message=request.message,
        user_id=request.user_id,
        context=request.context
    )
    return ChatResponse(**result)