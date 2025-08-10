"""
API路由配置
"""
from fastapi import APIRouter
from app.api.v1.endpoints import chat, knowledge, progress, demo

api_router = APIRouter()

# 注册各模块路由
api_router.include_router(demo.router, prefix="/demo", tags=["快速Demo"])
api_router.include_router(chat.router, prefix="/chat", tags=["聊天问答"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["知识库管理"])
api_router.include_router(progress.router, prefix="/progress", tags=["学习进度"])


@api_router.get("/")
async def api_root():
    return {"message": "AI Media Agent API v1"}