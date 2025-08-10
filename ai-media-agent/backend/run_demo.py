#!/usr/bin/env python3
"""
快速启动Demo脚本
30分钟快速版本 - 无需复杂配置
"""
import os
import sys
import webbrowser
import time
import uvicorn
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

def check_environment():
    """检查环境"""
    print("🔍 检查环境配置...")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ Python版本需要3.8+")
        return False
    
    # 检查数据文件
    data_files = [
        "../data/qa.json",
        "../data/learning_path.json", 
        "../data/cases.csv"
    ]
    
    for file in data_files:
        if not os.path.exists(file):
            print(f"⚠️ 缺少数据文件: {file}")
    
    print("✅ 环境检查完成")
    return True

def start_demo():
    """启动Demo"""
    print("""
╔═══════════════════════════════════════════╗
║     🚀 AI自媒体学习Agent - Demo启动器      ║
╚═══════════════════════════════════════════╝
    """)
    
    if not check_environment():
        return
    
    print("\n📦 准备启动服务...")
    print("=" * 50)
    print("访问地址:")
    print("  📊 API文档: http://localhost:8000/docs")
    print("  🎨 Demo界面: 打开 demo.html 文件")
    print("  🔥 快速测试: http://localhost:8000/api/v1/demo/quick-demo")
    print("=" * 50)
    
    # 3秒后自动打开浏览器
    print("\n⏰ 3秒后自动打开浏览器...")
    time.sleep(3)
    
    # 打开API文档
    webbrowser.open("http://localhost:8000/docs")
    
    # 启动服务
    print("\n✨ 服务启动中...\n")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    try:
        start_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Demo已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        print("\n请确保:")
        print("1. 已安装依赖: pip install fastapi uvicorn pandas")
        print("2. 在backend目录下运行")
        print("3. 端口8000未被占用")