#!/usr/bin/env python3
"""
创建数据库表结构脚本
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import text
from app.db.base import engine, Base
from app.db.models import *  # 导入所有模型
from app.core.logging import setup_logging


async def create_tables():
    """创建所有表"""
    try:
        print("🗄️ Creating database tables...")
        
        async with engine.begin() as conn:
            # 创建pgvector扩展
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            print("✅ pgvector extension created")
            
            # 创建所有表
            await conn.run_sync(Base.metadata.create_all)
            print("✅ All tables created successfully")
            
            # 显示创建的表
            result = await conn.execute(text("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public' 
                ORDER BY tablename
            """))
            
            tables = [row[0] for row in result.fetchall()]
            print(f"📊 Created tables: {', '.join(tables)}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False


async def main():
    """主函数"""
    setup_logging()
    
    print("🚀 Starting database table creation...")
    
    success = await create_tables()
    
    if success:
        print("✅ Database setup completed successfully!")
    else:
        print("❌ Database setup failed!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())