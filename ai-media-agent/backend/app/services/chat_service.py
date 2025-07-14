"""
聊天服务核心实现
"""
import logging
from typing import List, Dict, Optional
from app.services.rag_service import RAGService
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)


class ChatService:
    """聊天服务"""
    
    def __init__(self):
        self.rag_service = RAGService()
        self.llm_service = LLMService()
    
    async def process_question(
        self,
        message: str,
        user_id: Optional[str] = None,
        context: List[Dict] = []
    ) -> Dict:
        """
        处理用户问题
        
        Args:
            message: 用户消息
            user_id: 用户ID
            context: 对话上下文
            
        Returns:
            包含答案、来源和建议的字典
        """
        try:
            # 1. 检索相关知识
            relevant_docs = await self.rag_service.search(message)
            
            # 2. 构建提示词
            prompt = self._build_prompt(message, relevant_docs, context)
            
            # 3. 生成回答
            answer = await self.llm_service.generate(prompt)
            
            # 4. 提取来源信息
            sources = self._extract_sources(relevant_docs)
            
            # 5. 生成相关建议
            suggestions = self._generate_suggestions(message, answer)
            
            return {
                "answer": answer,
                "sources": sources,
                "suggestions": suggestions
            }
            
        except Exception as e:
            logger.error(f"Error processing question: {e}")
            return {
                "answer": "抱歉，处理您的问题时出现了错误。请稍后重试。",
                "sources": [],
                "suggestions": []
            }
    
    def _build_prompt(
        self,
        question: str,
        documents: List[Dict],
        context: List[Dict]
    ) -> str:
        """构建LLM提示词"""
        
        # 整理文档内容
        doc_content = "\n\n".join([
            f"【{doc['metadata']['source']}】\n{doc['content']}"
            for doc in documents
        ])
        
        # 整理对话上下文
        context_str = "\n".join([
            f"用户：{msg['user']}\n助手：{msg['assistant']}"
            for msg in context[-3:]  # 只保留最近3轮对话
        ])
        
        prompt = f"""你是AI自媒体学习助手，专门帮助圈友学习AI自媒体项目。

参考资料：
{doc_content}

历史对话：
{context_str}

用户问题：{question}

请根据参考资料回答用户问题。如果资料中有具体章节或页码，请在回答中引用。
如果参考资料不足以回答问题，请诚实告知用户，并建议查看相关章节。

回答要求：
1. 准确引用资料来源
2. 给出具体可操作的建议
3. 语言友好、易懂
"""
        return prompt
    
    def _extract_sources(self, documents: List[Dict]) -> List[Dict]:
        """提取文档来源信息"""
        sources = []
        for doc in documents[:3]:  # 只返回前3个最相关的来源
            sources.append({
                "title": doc['metadata'].get('source', '未知来源'),
                "content": doc['content'][:200] + "...",
                "relevance": doc.get('score', 0.0)
            })
        return sources
    
    def _generate_suggestions(self, question: str, answer: str) -> List[str]:
        """生成相关建议"""
        # TODO: 基于问题和答案生成智能建议
        suggestions = [
            "查看航海手册第2章了解详细的定位方法",
            "参考爆款案例库中的成功案例",
            "加入今晚的直播答疑了解更多"
        ]
        return suggestions[:3]