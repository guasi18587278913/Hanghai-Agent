#!/bin/bash

echo "🔧 Fixing AI Media Agent setup issues..."

cd backend

# 激活虚拟环境
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# 安装修复版本的依赖
echo "📥 Installing fixed dependencies..."
pip install -r requirements-fix.txt

# 检查Docker状态
echo "🐳 Checking Docker status..."
if ! docker info > /dev/null 2>&1; then
    echo "⚠️  Docker is not running. Please start Docker Desktop and run this script again."
    echo "   You can install Docker Desktop from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# 启动数据库服务
echo "🗄️  Starting database services..."
docker-compose up -d

# 等待数据库就绪
echo "⏳ Waiting for database to be ready..."
sleep 15

# 检查数据库连接
echo "🔍 Checking database connection..."
timeout 30 bash -c 'until docker-compose exec -T postgres pg_isready -U postgres; do sleep 1; done'

if [ $? -eq 0 ]; then
    echo "✅ Database is ready!"
else
    echo "❌ Database connection failed. Please check Docker logs:"
    echo "   docker-compose logs postgres"
    exit 1
fi

# 创建数据库表
echo "🔨 Creating database tables..."
python scripts/create_tables.py

# 初始化知识库数据
echo "📚 Initializing knowledge base..."
python scripts/init_data.py

echo "✅ Setup fixed successfully!"
echo ""
echo "🚀 Next steps:"
echo "1. Edit backend/.env with your API keys"
echo "2. Run: python main.py"
echo "3. Visit: http://localhost:8000/docs"