# 🚀 AI自媒体学习Agent - 快速启动指南

## 📋 准备工作

### 1. 环境要求
- Python 3.11+
- Docker & Docker Compose
- 至少8GB内存

### 2. API密钥
准备以下任一API密钥：
- OpenAI API Key（推荐GPT-4）
- Anthropic API Key（推荐Claude-3）

## ⚡ 一键安装

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd ai-media-agent

# 2. 运行安装脚本
./scripts/setup.sh
```

## 🔧 手动配置

### 1. 编辑环境变量
```bash
cd backend
cp .env.example .env
nano .env  # 填入你的API密钥
```

### 2. 必填配置项
```env
# 选择一个提供商
LLM_PROVIDER=anthropic  # 或 openai
ANTHROPIC_API_KEY=your_key_here
# 或
OPENAI_API_KEY=your_key_here

# 数据库配置（默认即可）
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_media_agent
```

## 🚀 启动服务

### 1. 启动后端
```bash
cd backend
source venv/bin/activate
python main.py
```

### 2. 验证启动
访问：http://localhost:8000/docs

## 🧪 测试功能

### API测试
```bash
# 测试聊天接口
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "什么是AI自媒体？"}'
```

### 系统测试
```bash
cd backend
python scripts/test_system.py
```

## 📊 核心功能

### 1. 智能问答
- **端点**: `/api/v1/chat`
- **功能**: 基于航海手册的AI问答
- **示例**: "如何选择AI自媒体赛道？"

### 2. 学习进度
- **端点**: `/api/v1/progress/{user_id}`
- **功能**: 21天学习路径管理
- **示例**: 查看当前学习进度

### 3. 知识库管理
- **端点**: `/api/v1/knowledge/status`
- **功能**: 查看知识库状态
- **包含**: 航海手册、Q&A、爆款案例

## 🔍 故障排除

### 常见问题

#### 1. 数据库连接失败
```bash
# 检查Docker服务
docker-compose ps

# 重启数据库
docker-compose restart postgres
```

#### 2. API密钥错误
```bash
# 检查环境变量
cd backend
source venv/bin/activate
python -c "from app.core.config import settings; print(settings.LLM_PROVIDER, bool(settings.ANTHROPIC_API_KEY))"
```

#### 3. 依赖安装失败
```bash
# 升级pip和重新安装
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### 日志查看
```bash
# 查看应用日志
tail -f backend/logs/app.log

# 查看数据库日志
docker-compose logs postgres
```

## 📖 使用示例

### 基础问答
```python
import requests

response = requests.post("http://localhost:8000/api/v1/chat", json={
    "message": "AI自媒体有哪些变现方式？",
    "user_id": "user123"
})

print(response.json())
```

### 查看学习进度
```python
response = requests.get("http://localhost:8000/api/v1/progress/user123")
print(response.json())
```

## 🎯 下一步

1. **测试核心功能**: 先通过API测试问答功能
2. **上传知识库**: 将航海手册放到正确位置
3. **自定义配置**: 根据需要调整参数
4. **开发前端**: 创建用户界面
5. **部署上线**: 配置生产环境

## 📞 获取支持

- 查看日志文件：`backend/logs/app.log`
- 运行测试脚本：`python scripts/test_system.py`
- 检查API文档：http://localhost:8000/docs

---

🎉 **恭喜！** 你的AI自媒体学习Agent已经准备就绪！