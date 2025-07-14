"""
数据库初始化
"""
import logging
from sqlalchemy import text
from app.db.base import engine

logger = logging.getLogger(__name__)


async def init_db():
    """初始化数据库"""
    try:
        # 创建pgvector扩展
        async with engine.begin() as conn:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise