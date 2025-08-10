#!/bin/bash

echo "🚀 开始部署到Netlify..."

# 检查是否安装了netlify-cli
if ! command -v netlify &> /dev/null
then
    echo "❌ 未安装Netlify CLI，正在安装..."
    npm install -g netlify-cli
fi

# 构建项目
echo "📦 构建项目..."
npm run build

# 检查构建是否成功
if [ ! -d "out" ]; then
    echo "❌ 构建失败，请检查错误信息"
    exit 1
fi

echo "✅ 构建成功！"

# 部署到Netlify
echo "🌐 正在部署到Netlify..."
netlify deploy --dir=out --prod

echo "🎉 部署完成！"
echo "📝 提示：如果是首次部署，请访问 https://app.netlify.com 查看你的站点地址"