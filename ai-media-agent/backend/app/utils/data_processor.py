"""
数据处理工具
"""
import re
import json
from typing import List, Dict, Any
from pathlib import Path


class DataProcessor:
    """数据处理工具类"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """清理文本"""
        if not text:
            return ""
        
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        
        # 移除特殊字符（保留中文、英文、数字、常用标点）
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s\.,!?;:""''()【】\-]', '', text)
        
        return text.strip()
    
    @staticmethod
    def extract_manual_metadata(content: str) -> Dict[str, Any]:
        """从手册内容中提取元数据"""
        metadata = {
            "chapter": None,
            "section": None,
            "subsection": None,
            "keywords": [],
            "difficulty": "medium"
        }
        
        lines = content.split('\n')[:10]  # 只检查前10行
        
        for line in lines:
            line = line.strip()
            
            # 提取章节信息
            if re.match(r'^第?[一二三四五六七八九十\d]+[章节]', line):
                if '章' in line:
                    metadata["chapter"] = line
                elif '节' in line:
                    metadata["section"] = line
            
            # 提取小节信息
            elif re.match(r'^\d+\.\d+', line):
                metadata["subsection"] = line
        
        return metadata
    
    @staticmethod
    def create_sample_qa_data() -> List[Dict]:
        """创建示例Q&A数据"""
        return [
            {
                "question": "什么是AI自媒体？",
                "answer": "AI自媒体是指利用人工智能工具来创作、优化和运营自媒体内容的方式。包括AI写作、AI绘画、AI视频制作等。",
                "category": "基础概念",
                "keywords": ["AI自媒体", "定义", "概念"]
            },
            {
                "question": "如何选择AI自媒体的赛道？",
                "answer": "选择赛道需要考虑：1)个人兴趣和专长 2)市场需求和竞争情况 3)变现潜力 4)内容创作难度。建议从AI工具分享、AI技术解读、AI创业副业等方向选择。",
                "category": "定位策略",
                "keywords": ["赛道选择", "定位", "策略"]
            },
            {
                "question": "新手如何开始做AI自媒体？",
                "answer": "新手建议按以下步骤：1)确定内容方向和目标平台 2)研究对标账号 3)准备基础设备和工具 4)制作第一批内容 5)持续优化和改进。",
                "category": "新手指导",
                "keywords": ["新手", "入门", "步骤"]
            }
        ]
    
    @staticmethod
    def create_sample_cases_data() -> List[Dict]:
        """创建示例爆款案例数据"""
        return [
            {
                "platform": "小红书",
                "account_name": "AI工具小助手",
                "content_type": "AI工具分享",
                "title": "这个AI工具竟然能一键生成PPT！",
                "description": "介绍了一款AI PPT生成工具，通过简单的文字描述就能自动生成精美的演示文稿。",
                "likes_count": 15200,
                "views_count": 89000,
                "comments_count": 340,
                "ai_tools_used": ["ChatGPT", "Gamma"],
                "success_factors": ["标题吸引人", "工具实用性强", "演示效果好", "评论区互动"]
            },
            {
                "platform": "抖音",
                "account_name": "AI创业分享",
                "content_type": "AI副业教程",
                "title": "用AI做自媒体，3个月收入过万",
                "description": "分享了利用AI工具创作内容，从0到月入过万的完整过程和经验。",
                "likes_count": 32100,
                "views_count": 256000,
                "comments_count": 890,
                "ai_tools_used": ["Midjourney", "Claude", "剪映"],
                "success_factors": ["真实案例", "数据展示", "方法可复制", "评论引导"]
            }
        ]
    
    @staticmethod
    def save_sample_data(data_dir: Path):
        """保存示例数据"""
        data_dir.mkdir(exist_ok=True)
        
        # 保存Q&A数据
        qa_data = DataProcessor.create_sample_qa_data()
        with open(data_dir / "qa.json", 'w', encoding='utf-8') as f:
            json.dump(qa_data, f, ensure_ascii=False, indent=2)
        
        # 保存案例数据为CSV格式
        import pandas as pd
        cases_data = DataProcessor.create_sample_cases_data()
        df = pd.DataFrame(cases_data)
        df.to_csv(data_dir / "cases.csv", index=False, encoding='utf-8')
        
        print(f"Sample data saved to {data_dir}")
    
    @staticmethod
    def validate_manual_format(content: str) -> Dict[str, Any]:
        """验证手册格式"""
        result = {
            "is_valid": True,
            "issues": [],
            "stats": {
                "total_chars": len(content),
                "total_lines": len(content.split('\n')),
                "chapters": 0,
                "sections": 0
            }
        }
        
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # 统计章节
            if re.match(r'^第?[一二三四五六七八九十\d]+章', line):
                result["stats"]["chapters"] += 1
            elif re.match(r'^第?[一二三四五六七八九十\d]+[节]', line):
                result["stats"]["sections"] += 1
            
            # 检查潜在问题
            if len(line) > 1000:
                result["issues"].append(f"Line {i+1}: Line too long ({len(line)} chars)")
            
            if line and not re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9\s\.,!?;:""''()【】\-#]', line):
                result["issues"].append(f"Line {i+1}: Contains unusual characters")
        
        if result["issues"]:
            result["is_valid"] = False
        
        return result