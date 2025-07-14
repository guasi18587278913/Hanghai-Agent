"""
知识库数据加载服务
"""
import logging
import os
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
from app.services.rag_service import RAGService
from app.core.config import settings

logger = logging.getLogger(__name__)


class KnowledgeLoader:
    """知识库数据加载器"""
    
    def __init__(self):
        self.rag_service = RAGService()
    
    async def load_all(self) -> bool:
        """加载所有知识库数据"""
        try:
            logger.info("Starting knowledge base loading...")
            
            # 1. 加载航海手册
            await self.load_manual()
            
            # 2. 加载Q&A数据
            await self.load_qa_data()
            
            # 3. 加载爆款案例
            await self.load_popular_cases()
            
            # 4. 加载社群帖子（如果有）
            await self.load_community_posts()
            
            logger.info("Knowledge base loading completed!")
            return True
            
        except Exception as e:
            logger.error(f"Knowledge base loading failed: {e}")
            return False
    
    async def load_manual(self) -> bool:
        """加载航海手册"""
        try:
            manual_path = Path(settings.MANUAL_PATH)
            if not manual_path.exists():
                logger.warning(f"Manual file not found: {manual_path}")
                return False
            
            logger.info("Loading manual from: " + str(manual_path))
            
            # 读取手册内容
            with open(manual_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 按章节分割（简单实现）
            sections = self._split_manual_by_sections(content)
            
            # 添加到知识库
            for i, (title, section_content) in enumerate(sections):
                await self.rag_service.add_document(
                    content=section_content,
                    source=f"航海手册-{title}",
                    metadata={
                        "source_type": "manual",
                        "section_title": title,
                        "section_index": i,
                        "priority": "high"
                    }
                )
            
            logger.info(f"Manual loaded: {len(sections)} sections")
            return True
            
        except Exception as e:
            logger.error(f"Manual loading error: {e}")
            return False
    
    async def load_qa_data(self) -> bool:
        """加载Q&A数据"""
        try:
            qa_path = Path(settings.QA_PATH)
            if not qa_path.exists():
                logger.warning(f"Q&A file not found: {qa_path}")
                return False
            
            logger.info("Loading Q&A data...")
            
            with open(qa_path, 'r', encoding='utf-8') as f:
                qa_data = json.load(f)
            
            # 添加Q&A到知识库
            for i, qa in enumerate(qa_data):
                content = f"问题：{qa['question']}\n\n答案：{qa['answer']}"
                
                await self.rag_service.add_document(
                    content=content,
                    source=f"百问百答-{i+1}",
                    metadata={
                        "source_type": "qa",
                        "category": qa.get("category", "general"),
                        "priority": "medium"
                    }
                )
            
            logger.info(f"Q&A data loaded: {len(qa_data)} items")
            return True
            
        except Exception as e:
            logger.error(f"Q&A loading error: {e}")
            return False
    
    async def load_popular_cases(self) -> bool:
        """加载爆款案例"""
        try:
            cases_path = Path(settings.CASES_PATH)
            if not cases_path.exists():
                logger.warning(f"Cases file not found: {cases_path}")
                return False
            
            logger.info("Loading popular cases...")
            
            # 读取CSV数据
            df = pd.read_csv(cases_path)
            
            for index, row in df.iterrows():
                # 构建案例内容
                content = self._format_case_content(row)
                
                await self.rag_service.add_document(
                    content=content,
                    source=f"爆款案例-{row.get('account_name', index)}",
                    metadata={
                        "source_type": "case",
                        "platform": row.get("platform"),
                        "content_type": row.get("content_type"),
                        "likes_count": int(row.get("likes_count", 0)),
                        "priority": "high"
                    }
                )
            
            logger.info(f"Popular cases loaded: {len(df)} items")
            return True
            
        except Exception as e:
            logger.error(f"Cases loading error: {e}")
            return False
    
    async def load_community_posts(self) -> bool:
        """加载社群帖子"""
        try:
            posts_dir = Path(settings.KNOWLEDGE_BASE_PATH) / "posts"
            if not posts_dir.exists():
                logger.info("No community posts directory found")
                return True
            
            logger.info("Loading community posts...")
            
            post_count = 0
            for post_file in posts_dir.glob("*.txt"):
                with open(post_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                await self.rag_service.add_document(
                    content=content,
                    source=f"社群帖子-{post_file.stem}",
                    metadata={
                        "source_type": "post",
                        "filename": post_file.name,
                        "priority": "medium"
                    }
                )
                post_count += 1
            
            logger.info(f"Community posts loaded: {post_count} items")
            return True
            
        except Exception as e:
            logger.error(f"Community posts loading error: {e}")
            return False
    
    def _split_manual_by_sections(self, content: str) -> List[tuple]:
        """按章节分割手册"""
        sections = []
        
        # 简单的章节分割逻辑
        lines = content.split('\n')
        current_section = ""
        current_title = "开始"
        
        for line in lines:
            # 检测章节标题（可以根据实际格式调整）
            if line.startswith('##') or line.startswith('第') and ('章' in line or '节' in line):
                # 保存上一章节
                if current_section.strip():
                    sections.append((current_title, current_section.strip()))
                
                # 开始新章节
                current_title = line.strip()
                current_section = ""
            else:
                current_section += line + '\n'
        
        # 添加最后一个章节
        if current_section.strip():
            sections.append((current_title, current_section.strip()))
        
        return sections
    
    def _format_case_content(self, case_row) -> str:
        """格式化案例内容"""
        content = f"""
爆款案例分析

平台：{case_row.get('platform', 'N/A')}
账号：{case_row.get('account_name', 'N/A')}
内容类型：{case_row.get('content_type', 'N/A')}
标题：{case_row.get('title', 'N/A')}

数据表现：
- 点赞数：{case_row.get('likes_count', 0)}
- 播放量：{case_row.get('views_count', 0)}
- 评论数：{case_row.get('comments_count', 0)}

内容描述：
{case_row.get('description', 'N/A')}

使用的AI工具：
{case_row.get('ai_tools_used', 'N/A')}

成功要素：
{case_row.get('success_factors', 'N/A')}
"""
        return content.strip()
    
    async def rebuild_index(self) -> bool:
        """重建索引"""
        try:
            logger.info("Rebuilding knowledge base index...")
            
            # 清空现有数据
            # TODO: 实现清空逻辑
            
            # 重新加载所有数据
            return await self.load_all()
            
        except Exception as e:
            logger.error(f"Index rebuild error: {e}")
            return False