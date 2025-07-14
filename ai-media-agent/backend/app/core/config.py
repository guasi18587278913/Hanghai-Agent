"""
配置管理
"""
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """应用配置"""
    
    # API配置
    API_HOST: str = Field(default="0.0.0.0")
    API_PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=True)
    
    # LLM配置
    LLM_PROVIDER: str = Field(default="anthropic")
    LLM_MODEL: str = Field(default="claude-3-opus-20240229")
    OPENAI_API_KEY: Optional[str] = Field(default=None)
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None)
    
    # 数据库配置
    DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/ai_media_agent"
    )
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    
    # 向量存储配置
    EMBEDDING_MODEL: str = Field(default="text-embedding-ada-002")
    CHUNK_SIZE: int = Field(default=1000)
    CHUNK_OVERLAP: int = Field(default=200)
    
    # 知识库路径
    KNOWLEDGE_BASE_PATH: str = Field(default="../data")
    MANUAL_PATH: str = Field(default="../航海书册-AI自媒体")
    QA_PATH: str = Field(default="../data/qa.json")
    CASES_PATH: str = Field(default="../data/cases.csv")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()