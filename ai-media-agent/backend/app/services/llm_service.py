"""
LLM服务实现
"""
import logging
from typing import Optional, Dict, Any
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.schema import HumanMessage, SystemMessage
from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """大语言模型服务"""
    
    def __init__(self):
        self.provider = settings.LLM_PROVIDER.lower()
        self.model_name = settings.LLM_MODEL
        
        # 初始化模型
        if self.provider == "openai":
            self.llm = ChatOpenAI(
                model_name=self.model_name,
                openai_api_key=settings.OPENAI_API_KEY,
                temperature=0.1,
                max_tokens=2000
            )
        elif self.provider == "anthropic":
            self.llm = ChatAnthropic(
                model=self.model_name,
                anthropic_api_key=settings.ANTHROPIC_API_KEY,
                temperature=0.1,
                max_tokens=2000
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
        
        logger.info(f"Initialized LLM: {self.provider}/{self.model_name}")
    
    async def generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        生成回答
        
        Args:
            prompt: 用户提示
            system_prompt: 系统提示
            **kwargs: 其他参数
            
        Returns:
            生成的回答
        """
        try:
            messages = []
            
            # 添加系统提示
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            else:
                messages.append(SystemMessage(content=self._get_default_system_prompt()))
            
            # 添加用户提示
            messages.append(HumanMessage(content=prompt))
            
            # 生成回答
            response = await self.llm.agenerate([messages])
            answer = response.generations[0][0].text.strip()
            
            logger.info(f"Generated response length: {len(answer)}")
            return answer
            
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            return "抱歉，我现在无法回答您的问题。请稍后重试。"
    
    async def chat(
        self,
        messages: list,
        **kwargs
    ) -> str:
        """
        多轮对话
        
        Args:
            messages: 对话历史
            **kwargs: 其他参数
            
        Returns:
            生成的回答
        """
        try:
            # 构建对话消息
            chat_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    chat_messages.append(SystemMessage(content=msg["content"]))
                elif msg["role"] == "user":
                    chat_messages.append(HumanMessage(content=msg["content"]))
                # 注意: 这里可能需要根据具体模型API调整
            
            # 生成回答
            response = await self.llm.agenerate([chat_messages])
            answer = response.generations[0][0].text.strip()
            
            return answer
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return "抱歉，对话过程中出现了错误。"
    
    async def summarize(self, text: str, max_length: int = 200) -> str:
        """
        文本摘要
        
        Args:
            text: 原文本
            max_length: 最大长度
            
        Returns:
            摘要文本
        """
        try:
            prompt = f"""请为以下文本生成一个简洁的摘要，不超过{max_length}字：

{text}

摘要："""
            
            summary = await self.generate(prompt)
            return summary
            
        except Exception as e:
            logger.error(f"Summarization error: {e}")
            return text[:max_length] + "..."
    
    async def extract_keywords(self, text: str, num_keywords: int = 5) -> list:
        """
        提取关键词
        
        Args:
            text: 文本内容
            num_keywords: 关键词数量
            
        Returns:
            关键词列表
        """
        try:
            prompt = f"""从以下文本中提取{num_keywords}个最重要的关键词，用逗号分隔：

{text}

关键词："""
            
            keywords_text = await self.generate(prompt)
            keywords = [kw.strip() for kw in keywords_text.split(",")]
            return keywords[:num_keywords]
            
        except Exception as e:
            logger.error(f"Keyword extraction error: {e}")
            return []
    
    def _get_default_system_prompt(self) -> str:
        """获取默认系统提示"""
        return """你是AI自媒体学习助手，专门帮助圈友学习AI自媒体项目。

你的特点：
1. 专业：对AI自媒体领域有深入了解
2. 友好：语言温和、易懂，像朋友一样交流
3. 实用：给出具体可操作的建议
4. 准确：基于提供的资料回答，不编造信息

回答要求：
- 如果有参考资料，请准确引用来源
- 给出具体可执行的步骤
- 语言简洁明了，避免过于技术化
- 如果不确定，请诚实告知用户"""
    
    async def classify_intent(self, message: str) -> Dict[str, Any]:
        """
        意图分类
        
        Args:
            message: 用户消息
            
        Returns:
            意图分析结果
        """
        try:
            prompt = f"""分析以下用户消息的意图，从这些类别中选择：
1. 基础咨询 - 询问基本概念和方法
2. 实操指导 - 需要具体操作步骤
3. 问题诊断 - 遇到问题需要解决
4. 进度查询 - 了解学习进度和任务
5. 案例分析 - 想了解成功案例
6. 其他

用户消息：{message}

请以JSON格式回答：
{{"intent": "类别名称", "confidence": 0.9, "keywords": ["关键词1", "关键词2"]}}"""
            
            result = await self.generate(prompt)
            # TODO: 解析JSON结果
            return {
                "intent": "基础咨询",
                "confidence": 0.8,
                "keywords": []
            }
            
        except Exception as e:
            logger.error(f"Intent classification error: {e}")
            return {
                "intent": "其他",
                "confidence": 0.5,
                "keywords": []
            }