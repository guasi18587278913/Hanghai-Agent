# AI自媒体学习Agent

## 项目概述
一个基于RAG技术的智能学习助手，专门为AI自媒体航海项目设计，提供7×24小时的个性化学习支持。

## 技术栈
- 后端：Python 3.11 + FastAPI + LangChain
- 数据库：PostgreSQL + pgvector + Redis
- 前端：React + Ant Design
- AI模型：Claude/GPT API

## 快速开始

### 1. 环境要求
- Python 3.11+
- PostgreSQL 15+（需要pgvector扩展）
- Redis 7+
- Node.js 18+

### 2. 后端安装
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 前端安装
```bash
cd frontend
npm install
```

### 4. 配置环境变量
复制 `.env.example` 到 `.env` 并填写相关配置

### 5. 启动服务
```bash
# 启动后端
cd backend
uvicorn main:app --reload

# 启动前端
cd frontend
npm start
```

## 项目结构
```
ai-media-agent/
├── backend/          # 后端代码
├── frontend/         # 前端代码
├── data/            # 知识库数据
├── scripts/         # 工具脚本
└── docs/           # 项目文档
```

## 开发团队
- 李亚东：产品设计 + 全栈开发
- Claude AI：技术方案设计 + 代码实现辅助