#!/usr/bin/env python3
"""
AI增强版Demo - 集成Gemini-2.5-pro
使用OpenRouter API
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random
import urllib.request
import urllib.parse
from pathlib import Path

# OpenRouter配置
OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-flash-1.5"  # 使用可用的Gemini模型

# 加载数据
def load_data():
    """加载模拟数据"""
    data = {}
    
    # Q&A数据
    try:
        with open('../data/qa.json', 'r', encoding='utf-8') as f:
            data['qa'] = json.load(f)['qa_pairs']
    except:
        data['qa'] = []
    
    # 学习路径
    try:
        with open('../data/learning_path.json', 'r', encoding='utf-8') as f:
            data['learning_path'] = json.load(f)
    except:
        data['learning_path'] = {"stages": []}
    
    # 爆款案例（简化处理CSV）
    try:
        cases = []
        with open('../data/cases.csv', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            headers = lines[0].strip().split(',')
            for line in lines[1:]:
                values = line.strip().split(',')
                case = dict(zip(headers, values))
                cases.append(case)
        data['cases'] = cases
    except:
        data['cases'] = []
    
    return data

# 全局数据
DATA = load_data()

def call_gemini(prompt):
    """调用Gemini API"""
    try:
        # 构建系统提示词
        system_prompt = """你是一个专业的AI自媒体学习助手，专门帮助用户学习AI自媒体相关知识。
你有以下知识库：
1. AI自媒体基础概念和定义
2. 21天学习计划（分为定位、搭建、运营三个阶段）
3. 爆款案例分析数据
4. 平台运营技巧（小红书、抖音等）
5. 变现方式和商业化策略

请根据用户问题，提供专业、实用、可操作的建议。回答要简洁明了，重点突出。"""

        # 准备请求数据
        request_data = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        # 创建请求
        req = urllib.request.Request(
            OPENROUTER_API_URL,
            data=json.dumps(request_data).encode('utf-8'),
            headers={
                'Authorization': f'Bearer {OPENROUTER_API_KEY}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'http://localhost:8000',
                'X-Title': 'AI Media Agent Demo'
            }
        )
        
        # 发送请求
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode('utf-8'))
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                print(f"API响应格式错误: {result}")
                return None
    
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"API HTTP错误 {e.code}: {error_body}")
        return None
    except Exception as e:
        print(f"API调用错误: {e}")
        return None

class AIHandler(BaseHTTPRequestHandler):
    """AI增强的HTTP处理器"""
    
    def do_OPTIONS(self):
        """处理CORS预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """处理GET请求"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if self.path == '/':
            response = {
                "message": "AI自媒体学习Agent - AI增强版",
                "model": "Gemini-2.0-flash via OpenRouter",
                "endpoints": {
                    "/chat": "POST - AI智能问答",
                    "/progress": "GET - 学习进度",
                    "/cases": "GET - 爆款案例",
                    "/path": "GET - 学习路径",
                    "/analyze": "POST - AI内容分析"
                }
            }
        elif self.path == '/progress':
            # 模拟进度
            day = random.randint(1, 21)
            stage_idx = 0 if day <= 4 else (1 if day <= 11 else 2)
            stage = DATA['learning_path']['stages'][stage_idx]
            
            # 找到今天的任务
            today_task = None
            for task in stage['tasks']:
                if task['day'] == day:
                    today_task = task
                    break
            
            response = {
                "current_day": day,
                "total_days": 21,
                "progress": int(day/21*100),
                "stage": stage['name'],
                "stage_description": stage['description'],
                "today_task": today_task
            }
        elif self.path == '/cases':
            response = {
                "cases": DATA['cases'][:5],
                "total": len(DATA['cases'])
            }
        elif self.path == '/path':
            response = DATA['learning_path']
        else:
            response = {"error": "Not found"}
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_POST(self):
        """处理POST请求"""
        # 读取请求体
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            if self.path == '/chat':
                response = self._process_chat(data.get('message', ''))
            elif self.path == '/analyze':
                response = self._analyze_content(data.get('content', ''), data.get('platform', '小红书'))
            elif self.path == '/generate-path':
                response = self._generate_personalized_path(data.get('profile', {}))
            else:
                self.send_error(404)
                return
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_error(500, str(e))
    
    def _process_chat(self, message):
        """处理聊天消息 - 使用AI"""
        message_lower = message.lower()
        
        # 先尝试从知识库精确匹配
        for qa in DATA['qa']:
            if any(keyword in message_lower for keyword in qa['question'].lower().split()):
                # 使用AI增强回答
                enhanced_prompt = f"""用户问题：{message}
                
参考答案：{qa['answer']}

请基于参考答案，结合你的知识，给出更详细和实用的回答。保持专业性，增加具体的操作建议。"""
                
                ai_answer = call_gemini(enhanced_prompt)
                if ai_answer:
                    return {
                        "answer": ai_answer,
                        "type": "ai_enhanced",
                        "source": f"AI增强 - {qa['category']}",
                        "confidence": 0.95
                    }
        
        # 如果没有精确匹配，直接使用AI回答
        # 构建包含上下文的提示词
        context_prompt = f"""用户问题：{message}

请根据以下信息回答：
1. 我们有21天的AI自媒体学习计划，分为定位（1-4天）、搭建（5-11天）、运营（12-21天）三个阶段
2. 主要平台是小红书和抖音
3. 变现方式包括广告合作、知识付费、专业服务、流量分成
4. 我们有爆款案例数据可以参考

请给出专业、具体、可操作的建议。"""

        ai_answer = call_gemini(context_prompt)
        
        if ai_answer:
            return {
                "answer": ai_answer,
                "type": "ai_generated",
                "source": "Gemini AI",
                "suggestions": self._generate_suggestions(message)
            }
        else:
            # 降级到规则匹配
            return self._fallback_response(message)
    
    def _analyze_content(self, content, platform):
        """AI分析内容"""
        prompt = f"""请分析以下{platform}平台的内容标题，并给出优化建议：

标题：{content}

请从以下维度分析：
1. 标题吸引力（1-10分）
2. 关键词布局
3. 情绪价值
4. 目标受众匹配度
5. 爆款潜力预测

给出具体的优化建议和改进方向。"""

        ai_analysis = call_gemini(prompt)
        
        if ai_analysis:
            return {
                "analysis": ai_analysis,
                "platform": platform,
                "original_content": content,
                "type": "ai_analysis"
            }
        else:
            # 降级响应
            return {
                "analysis": "标题还不错，建议加入数字和结果导向的词汇",
                "score": random.randint(60, 85),
                "type": "rule_based"
            }
    
    def _generate_suggestions(self, message):
        """生成相关建议"""
        suggestions = []
        
        if "新手" in message or "开始" in message:
            suggestions = ["了解21天学习计划", "查看爆款案例", "选择适合的平台"]
        elif "变现" in message or "赚钱" in message:
            suggestions = ["了解变现门槛", "查看成功案例", "制定内容策略"]
        elif "内容" in message or "创作" in message:
            suggestions = ["分析爆款标题", "学习内容模板", "了解平台规则"]
        else:
            suggestions = ["查看学习进度", "浏览爆款案例", "获取今日任务"]
        
        return suggestions[:3]
    
    def _fallback_response(self, message):
        """降级响应（当AI不可用时）"""
        return {
            "answer": "我是AI自媒体学习助手。我可以帮您：\n1. 制定21天学习计划\n2. 分析爆款案例\n3. 提供运营建议\n\n请问您想了解哪方面？",
            "type": "fallback",
            "suggestions": ["查看21天计划", "分析爆款案例", "了解变现方式"]
        }
    
    def _generate_personalized_path(self, profile):
        """生成个性化学习路径"""
        # 构建用户画像描述
        profile_desc = f"""
用户画像：
- 时间投入：{profile.get('timeAvailable', '未知')}
- AI水平：{profile.get('aiLevel', '未知')}
- 内容能力：{profile.get('contentSkill', '未知')}
- 目标：{profile.get('goal', '未知')}
- 偏好形式：{profile.get('format', '未知')}
- 方向：{profile.get('direction', [])}
- 经验：{profile.get('experience', [])}
"""
        
        # 使用AI生成个性化建议
        prompt = f"""基于以下用户画像，生成一个21天的AI自媒体学习计划：

{profile_desc}

请按照以下格式生成3个学习阶段，每个阶段包含具体任务：
1. 阶段名称、时长、重点
2. 5个具体的学习任务
3. 给出个性化的学习建议

要求：
- 根据用户的时间、能力和目标定制
- 任务要具体可执行
- 循序渐进，由浅入深"""

        ai_response = call_gemini(prompt)
        
        if ai_response:
            return {
                "type": "ai_generated",
                "personalizedAdvice": ai_response,
                "profile": profile,
                "message": "已为您生成个性化学习路径"
            }
        else:
            # 降级处理：返回基础路径
            return {
                "type": "default",
                "message": "基于您的情况，推荐以下学习路径",
                "path": self._get_default_path_for_profile(profile)
            }
    
    def _get_default_path_for_profile(self, profile):
        """根据用户画像返回默认路径"""
        # 这里可以根据不同的用户类型返回不同的预设路径
        if profile.get('aiLevel', 0) <= 2:
            # 新手路径
            return {
                "name": "AI新手进阶路径",
                "phases": [
                    {
                        "name": "基础认知",
                        "duration": "1-7天",
                        "tasks": ["了解AI工具", "学习基础操作", "确定方向"]
                    },
                    {
                        "name": "实践练习",
                        "duration": "8-14天",
                        "tasks": ["创作首批内容", "优化迭代", "建立节奏"]
                    },
                    {
                        "name": "提升优化",
                        "duration": "15-21天",
                        "tasks": ["数据分析", "爆款研究", "变现探索"]
                    }
                ]
            }
        else:
            # 进阶路径
            return {
                "name": "AI进阶优化路径",
                "phases": [
                    {
                        "name": "快速定位",
                        "duration": "1-4天",
                        "tasks": ["赛道分析", "竞品研究", "差异化定位"]
                    },
                    {
                        "name": "内容爆发",
                        "duration": "5-14天",
                        "tasks": ["批量创作", "多平台分发", "数据优化"]
                    },
                    {
                        "name": "商业变现",
                        "duration": "15-21天",
                        "tasks": ["开通收益", "商务合作", "私域运营"]
                    }
                ]
            }

def run_server(port=8000):
    """启动服务器"""
    print(f"""
╔═══════════════════════════════════════════╗
║   🚀 AI自媒体学习Agent - AI增强版          ║
╚═══════════════════════════════════════════╝

✨ 已集成 Gemini-2.0-flash 模型
🔑 使用 OpenRouter API

✅ 服务启动成功！

📍 访问地址：
   - API测试: http://localhost:{port}/
   - AI聊天: POST http://localhost:{port}/chat
   - 内容分析: POST http://localhost:{port}/analyze
   - 学习进度: GET http://localhost:{port}/progress
   - 爆款案例: GET http://localhost:{port}/cases

🎨 打开 demo.html 查看Web界面

按 Ctrl+C 停止服务
""")
    
    server = HTTPServer(('localhost', port), AIHandler)
    server.serve_forever()

if __name__ == '__main__':
    try:
        run_server()
    except KeyboardInterrupt:
        print("\n\n👋 服务已停止")