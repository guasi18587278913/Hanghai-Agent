"""
数据库模型定义
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
import uuid

from app.db.base import Base


class KnowledgeChunk(Base):
    """知识库文档块"""
    __tablename__ = "knowledge_chunks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False, comment="文本内容")
    source = Column(String(255), nullable=False, comment="来源")
    source_type = Column(String(50), nullable=False, comment="来源类型")
    chunk_index = Column(Integer, nullable=False, comment="块索引")
    total_chunks = Column(Integer, nullable=False, comment="总块数")
    embedding = Column(Vector(1536), comment="向量表示")  # OpenAI embedding维度
    metadata = Column(JSON, comment="元数据")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(100), unique=True, nullable=False, comment="用户ID")
    nickname = Column(String(100), comment="昵称")
    avatar = Column(String(255), comment="头像URL")
    current_day = Column(Integer, default=1, comment="当前学习天数")
    selected_track = Column(String(50), comment="选择的赛道")
    target_platform = Column(String(50), comment="目标平台")
    profile = Column(JSON, comment="用户画像")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class LearningProgress(Base):
    """学习进度"""
    __tablename__ = "learning_progress"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(100), nullable=False, comment="用户ID")
    day = Column(Integer, nullable=False, comment="学习天数")
    phase = Column(String(50), nullable=False, comment="学习阶段")
    tasks_completed = Column(Integer, default=0, comment="已完成任务数")
    tasks_total = Column(Integer, default=0, comment="总任务数")
    completion_rate = Column(Float, default=0.0, comment="完成率")
    notes = Column(Text, comment="学习笔记")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ChatHistory(Base):
    """对话历史"""
    __tablename__ = "chat_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(100), nullable=False, comment="用户ID")
    session_id = Column(String(100), nullable=False, comment="会话ID")
    message_type = Column(String(20), nullable=False, comment="消息类型(user/assistant)")
    content = Column(Text, nullable=False, comment="消息内容")
    intent = Column(String(50), comment="意图分类")
    sources = Column(JSON, comment="参考来源")
    feedback_score = Column(Integer, comment="用户反馈评分")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PopularCase(Base):
    """爆款案例"""
    __tablename__ = "popular_cases"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    platform = Column(String(50), nullable=False, comment="平台")
    account_name = Column(String(100), comment="账号名称")
    content_type = Column(String(50), comment="内容类型")
    title = Column(String(255), comment="标题")
    description = Column(Text, comment="描述")
    likes_count = Column(Integer, comment="点赞数")
    views_count = Column(Integer, comment="播放量")
    comments_count = Column(Integer, comment="评论数")
    publish_date = Column(DateTime, comment="发布时间")
    ai_tools_used = Column(JSON, comment="使用的AI工具")
    tags = Column(JSON, comment="标签")
    success_factors = Column(JSON, comment="成功要素")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Task(Base):
    """任务表"""
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    day = Column(Integer, nullable=False, comment="学习天数")
    phase = Column(String(50), nullable=False, comment="学习阶段")
    title = Column(String(255), nullable=False, comment="任务标题")
    description = Column(Text, comment="任务描述")
    task_type = Column(String(50), comment="任务类型")
    estimated_time = Column(Integer, comment="预估时间(分钟)")
    priority = Column(String(20), default="medium", comment="优先级")
    prerequisites = Column(JSON, comment="前置条件")
    resources = Column(JSON, comment="相关资源")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserTask(Base):
    """用户任务关联"""
    __tablename__ = "user_tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(100), nullable=False, comment="用户ID")
    task_id = Column(UUID(as_uuid=True), nullable=False, comment="任务ID")
    status = Column(String(20), default="pending", comment="状态")
    started_at = Column(DateTime, comment="开始时间")
    completed_at = Column(DateTime, comment="完成时间")
    notes = Column(Text, comment="任务笔记")
    result = Column(JSON, comment="任务结果")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())