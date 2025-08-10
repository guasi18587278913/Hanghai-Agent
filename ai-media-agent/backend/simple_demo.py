#!/usr/bin/env python3
"""
超简化Demo - 无需任何依赖
30分钟快速版本
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random
from pathlib import Path

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

class DemoHandler(BaseHTTPRequestHandler):
    """简单的HTTP处理器"""
    
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
                "message": "AI自媒体学习Agent - 简化Demo",
                "endpoints": {
                    "/chat": "POST - 智能问答",
                    "/progress": "GET - 学习进度",
                    "/cases": "GET - 爆款案例",
                    "/path": "GET - 学习路径"
                }
            }
        elif self.path == '/progress':
            # 模拟进度
            day = random.randint(1, 21)
            response = {
                "current_day": day,
                "total_days": 21,
                "progress": int(day/21*100),
                "stage": "定位阶段" if day <= 4 else ("搭建阶段" if day <= 11 else "运营阶段")
            }
        elif self.path == '/cases':
            response = {
                "cases": DATA['cases'][:3],
                "total": len(DATA['cases'])
            }
        elif self.path == '/path':
            response = DATA['learning_path']
        else:
            response = {"error": "Not found"}
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_POST(self):
        """处理POST请求"""
        if self.path != '/chat':
            self.send_error(404)
            return
        
        # 读取请求体
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            message = data.get('message', '')
            
            # 简单的关键词匹配
            response = self._process_chat(message)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_error(500, str(e))
    
    def _process_chat(self, message):
        """处理聊天消息"""
        message_lower = message.lower()
        
        # 查找匹配的Q&A
        for qa in DATA['qa']:
            # 更宽松的匹配：检查关键词是否在问题中
            qa_keywords = ['ai自媒体', '赛道', '平台', '涨粉', '变现']
            for keyword in qa_keywords:
                if keyword in message_lower and keyword in qa['question'].lower():
                    return {
                        "answer": qa['answer'],
                        "type": "qa",
                        "source": qa['category']
                    }
        
        # 学习相关
        if any(word in message_lower for word in ['学习', '计划', '进度', '21天']):
            day = random.randint(1, 21)
            stage = DATA['learning_path']['stages'][0 if day <= 4 else (1 if day <= 11 else 2)]
            return {
                "answer": f"您当前在{stage['name']}（第{day}天），{stage['description']}",
                "type": "learning"
            }
        
        # 爆款相关
        if any(word in message_lower for word in ['爆款', '案例', '成功']):
            if DATA['cases']:
                case = random.choice(DATA['cases'])
                return {
                    "answer": f"推荐案例：{case['title']}，{case['platform']}平台，{case['views']}播放",
                    "type": "case"
                }
        
        # 默认回复
        return {
            "answer": "我是AI自媒体学习助手，可以回答关于AI自媒体的问题，提供学习计划和爆款案例分析。",
            "type": "default",
            "suggestions": ["什么是AI自媒体？", "查看学习计划", "分析爆款案例"]
        }

def run_server(port=8000):
    """启动服务器"""
    print(f"""
╔═══════════════════════════════════════════╗
║   🚀 AI自媒体学习Agent - 超简化Demo        ║
╚═══════════════════════════════════════════╝

✅ 服务启动成功！

📍 访问地址：
   - API测试: http://localhost:{port}/
   - 聊天接口: POST http://localhost:{port}/chat
   - 学习进度: GET http://localhost:{port}/progress
   - 爆款案例: GET http://localhost:{port}/cases
   - 学习路径: GET http://localhost:{port}/path

🎨 打开 demo.html 查看Web界面

按 Ctrl+C 停止服务
""")
    
    server = HTTPServer(('localhost', port), DemoHandler)
    server.serve_forever()

if __name__ == '__main__':
    try:
        run_server()
    except KeyboardInterrupt:
        print("\n\n👋 服务已停止")