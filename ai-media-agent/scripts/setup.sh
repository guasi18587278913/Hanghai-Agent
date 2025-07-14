#!/bin/bash

echo "🚀 Setting up AI Media Agent development environment..."

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $python_version"

# 创建虚拟环境
echo "📦 Creating Python virtual environment..."
cd backend
python3 -m venv venv

# 激活虚拟环境
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# 安装依赖
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 复制环境变量文件
echo "📄 Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Please edit backend/.env file with your API keys"
fi

# 启动数据库服务
echo "🗄️  Starting database services..."
docker-compose up -d

# 等待数据库就绪
echo "⏳ Waiting for database to be ready..."
sleep 15

# 创建数据库表
echo "🔨 Creating database tables..."
python scripts/create_tables.py

# 初始化知识库数据
echo "📚 Initializing knowledge base..."
python scripts/init_data.py

# 运行系统测试
echo "🧪 Running system tests..."
python scripts/test_system.py

echo "✅ Backend setup complete!"

# 设置前端
cd ../frontend
if [ -d "." ]; then
    echo "📦 Installing frontend dependencies..."
    # npm install
    echo "✅ Frontend setup complete!"
fi

echo "🎉 Setup complete! Next steps:"
echo "1. Edit backend/.env with your API keys"
echo "2. Run 'cd backend && source venv/bin/activate && python main.py' to start the backend"
echo "3. Visit http://localhost:8000/docs to see the API documentation"
echo "4. Test the chat API at http://localhost:8000/api/v1/chat"