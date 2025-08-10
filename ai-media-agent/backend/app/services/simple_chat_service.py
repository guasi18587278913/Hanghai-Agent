"""
简化版聊天服务 - 30分钟Demo版本
"""
import json
import random
from typing import Dict, List, Optional
import pandas as pd
from pathlib import Path

class SimpleChatService:
    """简化的聊天服务，用于快速Demo"""
    
    def __init__(self):
        # 加载知识库
        self.qa_data = self._load_qa()
        self.learning_path = self._load_learning_path()
        self.cases = self._load_cases()
        
    def _load_qa(self):
        """加载Q&A数据"""
        try:
            with open('../data/qa.json', 'r', encoding='utf-8') as f:
                return json.load(f)['qa_pairs']
        except:
            return []
    
    def _load_learning_path(self):
        """加载学习路径"""
        try:
            with open('../data/learning_path.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"stages": []}
    
    def _load_cases(self):
        """加载爆款案例"""
        try:
            return pd.read_csv('../data/cases.csv')
        except:
            return pd.DataFrame()
    
    async def chat(self, message: str, user_id: Optional[str] = None) -> Dict:
        """处理聊天消息"""
        message_lower = message.lower()
        
        # 智能问答
        if any(keyword in message_lower for keyword in ['什么是', '如何', '怎么', '为什么']):
            return await self._handle_qa(message)
        
        # 学习路径
        if any(keyword in message_lower for keyword in ['学习', '计划', '路径', '21天', '进度']):
            return await self._handle_learning_path(message, user_id)
        
        # 爆款案例
        if any(keyword in message_lower for keyword in ['爆款', '案例', '成功', '分析']):
            return await self._handle_cases(message)
        
        # 默认回复
        return {
            "answer": "我理解您的问题。让我为您提供一些建议：\n\n" +
                     "1. 您可以问我关于AI自媒体的基础知识\n" +
                     "2. 查看21天学习计划\n" +
                     "3. 了解爆款案例分析\n\n" +
                     "请问您想了解哪方面的内容？",
            "type": "default",
            "suggestions": ["什么是AI自媒体？", "查看学习计划", "分析爆款案例"]
        }
    
    async def _handle_qa(self, message: str) -> Dict:
        """处理Q&A问题"""
        # 简单匹配
        for qa in self.qa_data:
            if any(word in message for word in qa['question'].split()):
                return {
                    "answer": qa['answer'],
                    "type": "qa",
                    "source": f"知识库 - {qa['category']}",
                    "confidence": 0.85,
                    "related_questions": [q['question'] for q in self.qa_data if q['id'] != qa['id']][:3]
                }
        
        return {
            "answer": "这是一个很好的问题。基于我的知识库，AI自媒体是一个充满机会的领域。建议您从了解基础概念开始，然后选择适合的赛道。",
            "type": "qa",
            "suggestions": ["什么是AI自媒体？", "如何选择赛道？", "哪个平台适合新手？"]
        }
    
    async def _handle_learning_path(self, message: str, user_id: Optional[str] = None) -> Dict:
        """处理学习路径查询"""
        # 模拟用户进度
        current_day = random.randint(1, 21)
        current_stage = 1 if current_day <= 4 else (2 if current_day <= 11 else 3)
        
        stage_info = self.learning_path['stages'][current_stage - 1]
        today_task = None
        
        for task in stage_info['tasks']:
            if task['day'] == current_day:
                today_task = task
                break
        
        return {
            "answer": f"您当前处于【{stage_info['name']}】（第{current_day}天）\n\n" +
                     f"今日任务：{today_task['title'] if today_task else '继续昨天的任务'}\n" +
                     f"具体内容：{today_task['content'] if today_task else '保持内容输出节奏'}\n\n" +
                     f"整体进度：{int(current_day/21*100)}%",
            "type": "learning_path",
            "data": {
                "current_day": current_day,
                "current_stage": stage_info['name'],
                "progress": int(current_day/21*100),
                "today_task": today_task
            },
            "next_steps": ["查看明天任务", "回顾昨天内容", "查看阶段目标"]
        }
    
    async def _handle_cases(self, message: str) -> Dict:
        """处理爆款案例分析"""
        if not self.cases.empty:
            # 随机选择一个案例进行分析
            case = self.cases.sample(1).iloc[0]
            
            return {
                "answer": f"为您分析一个爆款案例：\n\n" +
                         f"【{case['title']}】\n" +
                         f"平台：{case['platform']}\n" +
                         f"数据：{case['views']}播放，{case['likes']}点赞\n" +
                         f"类型：{case['content_type']}\n\n" +
                         f"成功要素：{case['success_factors']}\n\n" +
                         f"建议您参考这个案例的标题结构和内容形式，创作类似内容。",
                "type": "case_analysis",
                "data": case.to_dict(),
                "recommendations": [
                    "分析更多同类案例",
                    "查看爆款标题公式",
                    "了解平台算法规则"
                ]
            }
        
        return {
            "answer": "爆款案例的核心要素包括：吸引力标题、精准痛点、视觉冲击、实用价值。",
            "type": "case_analysis"
        }
    
    async def get_learning_progress(self, user_id: str) -> Dict:
        """获取学习进度"""
        # 模拟数据
        current_day = random.randint(1, 21)
        completed_tasks = current_day - 1
        
        return {
            "user_id": user_id,
            "current_day": current_day,
            "total_days": 21,
            "progress_percentage": int(current_day/21*100),
            "completed_tasks": completed_tasks,
            "total_tasks": 21,
            "current_stage": "定位阶段" if current_day <= 4 else ("搭建阶段" if current_day <= 11 else "运营阶段")
        }
    
    async def analyze_content(self, content: str, platform: str = "小红书") -> Dict:
        """分析内容质量"""
        # 简单的内容分析
        score = random.randint(70, 95)
        
        suggestions = [
            "标题可以更吸引眼球",
            "添加更多实用技巧",
            "配图要更清晰",
            "结尾加上行动号召"
        ]
        
        return {
            "score": score,
            "platform": platform,
            "suggestions": random.sample(suggestions, 2),
            "predicted_performance": "中等" if score < 80 else "良好"
        }