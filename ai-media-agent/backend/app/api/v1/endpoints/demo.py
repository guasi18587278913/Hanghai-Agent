"""
Demo API端点 - 30分钟快速版本
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from app.services.simple_chat_service import SimpleChatService

router = APIRouter()
chat_service = SimpleChatService()

# 请求/响应模型
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "demo_user"

class ChatResponse(BaseModel):
    answer: str
    type: str
    data: Optional[Dict] = None
    suggestions: Optional[List[str]] = None
    source: Optional[str] = None

class ProgressResponse(BaseModel):
    user_id: str
    current_day: int
    total_days: int
    progress_percentage: int
    current_stage: str

class AnalyzeRequest(BaseModel):
    content: str
    platform: str = "小红书"

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """智能问答接口"""
    try:
        result = await chat_service.chat(request.message, request.user_id)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/progress/{user_id}", response_model=ProgressResponse)
async def get_progress(user_id: str):
    """获取学习进度"""
    try:
        result = await chat_service.get_learning_progress(user_id)
        return ProgressResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze")
async def analyze_content(request: AnalyzeRequest):
    """分析内容质量（爆款预测）"""
    try:
        result = await chat_service.analyze_content(request.content, request.platform)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cases")
async def get_cases(limit: int = 5):
    """获取爆款案例"""
    try:
        import pandas as pd
        cases_df = pd.read_csv('../data/cases.csv')
        cases = cases_df.head(limit).to_dict('records')
        return {"cases": cases, "total": len(cases_df)}
    except Exception as e:
        return {"cases": [], "error": str(e)}

@router.get("/learning-path")
async def get_learning_path():
    """获取完整学习路径"""
    try:
        import json
        with open('../data/learning_path.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/quick-demo")
async def quick_demo():
    """快速演示所有功能"""
    return {
        "message": "AI自媒体学习Agent Demo已启动！",
        "features": {
            "1_智能问答": {
                "endpoint": "/api/v1/demo/chat",
                "example": {"message": "什么是AI自媒体？"},
                "description": "基于知识库的智能问答"
            },
            "2_学习进度": {
                "endpoint": "/api/v1/demo/progress/{user_id}",
                "example": "/api/v1/demo/progress/demo_user",
                "description": "21天学习路径管理"
            },
            "3_爆款分析": {
                "endpoint": "/api/v1/demo/analyze",
                "example": {"content": "测试内容", "platform": "小红书"},
                "description": "内容质量分析和爆款预测"
            },
            "4_案例库": {
                "endpoint": "/api/v1/demo/cases",
                "description": "查看爆款案例库"
            },
            "5_学习路径": {
                "endpoint": "/api/v1/demo/learning-path",
                "description": "查看完整21天计划"
            }
        },
        "test_urls": [
            "http://localhost:8000/api/v1/demo/quick-demo",
            "http://localhost:8000/api/v1/demo/chat",
            "http://localhost:8000/api/v1/demo/progress/demo_user",
            "http://localhost:8000/api/v1/demo/cases"
        ]
    }