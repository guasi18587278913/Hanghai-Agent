#!/usr/bin/env python3
"""
初始化知识库数据脚本
"""
import asyncio
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.knowledge_loader import KnowledgeLoader
from app.utils.data_processor import DataProcessor
from app.core.config import settings
from app.core.logging import setup_logging


async def main():
    """主函数"""
    # 设置日志
    setup_logging()
    
    print("🚀 Initializing AI Media Agent knowledge base...")
    
    # 检查数据目录
    data_dir = Path(settings.KNOWLEDGE_BASE_PATH)
    data_dir.mkdir(exist_ok=True)
    
    # 如果没有示例数据，创建一些
    qa_file = Path(settings.QA_PATH)
    cases_file = Path(settings.CASES_PATH)
    
    if not qa_file.exists() or not cases_file.exists():
        print("📦 Creating sample data files...")
        DataProcessor.save_sample_data(data_dir)
    
    # 检查航海手册
    manual_file = Path(settings.MANUAL_PATH)
    if not manual_file.exists():
        print(f"⚠️  Manual file not found at: {manual_file}")
        print("Please make sure the manual file is in the correct location.")
        return False
    
    # 验证手册格式
    with open(manual_file, 'r', encoding='utf-8') as f:
        manual_content = f.read()
    
    validation_result = DataProcessor.validate_manual_format(manual_content)
    print(f"📊 Manual validation: {validation_result['stats']}")
    
    if not validation_result['is_valid']:
        print("⚠️  Manual format issues found:")
        for issue in validation_result['issues'][:5]:  # 只显示前5个问题
            print(f"   - {issue}")
    
    # 加载知识库
    loader = KnowledgeLoader()
    success = await loader.load_all()
    
    if success:
        print("✅ Knowledge base initialization completed!")
        
        # 显示统计信息
        stats = await loader.rag_service.get_stats()
        print(f"📈 Statistics: {stats}")
        
    else:
        print("❌ Knowledge base initialization failed!")
        return False
    
    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)