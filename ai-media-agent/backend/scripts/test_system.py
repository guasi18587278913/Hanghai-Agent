#!/usr/bin/env python3
"""
系统功能测试脚本
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.chat_service import ChatService
from app.services.rag_service import RAGService
from app.services.llm_service import LLMService
from app.core.logging import setup_logging


async def test_rag_service():
    """测试RAG服务"""
    print("\n🔍 Testing RAG Service...")
    
    try:
        rag_service = RAGService()
        
        # 测试添加文档
        test_content = """
        AI自媒体是指利用人工智能技术来创作、优化和运营自媒体内容的新兴方式。
        主要包括以下几个方面：
        1. AI写作：使用ChatGPT、Claude等工具辅助文案创作
        2. AI绘画：使用Midjourney、DALL-E等工具创作视觉内容
        3. AI视频：使用Runway、Pika等工具制作视频内容
        """
        
        result = await rag_service.add_document(
            content=test_content,
            source="测试文档",
            metadata={"type": "test"}
        )
        
        if result:
            print("✅ Document added successfully")
        else:
            print("❌ Failed to add document")
            return False
        
        # 测试搜索
        search_results = await rag_service.search("什么是AI自媒体", k=3)
        
        if search_results:
            print(f"✅ Search returned {len(search_results)} results")
            for i, result in enumerate(search_results):
                print(f"   Result {i+1}: {result['content'][:100]}...")
        else:
            print("❌ Search returned no results")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ RAG service test failed: {e}")
        return False


async def test_llm_service():
    """测试LLM服务"""
    print("\n🤖 Testing LLM Service...")
    
    try:
        llm_service = LLMService()
        
        # 测试简单生成
        prompt = "请简单解释什么是AI自媒体，用一句话回答。"
        response = await llm_service.generate(prompt)
        
        if response and len(response) > 0:
            print(f"✅ LLM generated response: {response[:100]}...")
        else:
            print("❌ LLM failed to generate response")
            return False
        
        # 测试意图分类
        intent_result = await llm_service.classify_intent("我想学习AI自媒体")
        print(f"✅ Intent classification: {intent_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM service test failed: {e}")
        return False


async def test_chat_service():
    """测试聊天服务"""
    print("\n💬 Testing Chat Service...")
    
    try:
        chat_service = ChatService()
        
        # 测试问答
        response = await chat_service.process_question(
            message="AI自媒体有哪些常见的变现方式？",
            user_id="test_user"
        )
        
        if response.get('answer'):
            print(f"✅ Chat service response: {response['answer'][:100]}...")
            print(f"   Sources: {len(response.get('sources', []))}")
            print(f"   Suggestions: {len(response.get('suggestions', []))}")
        else:
            print("❌ Chat service failed to process question")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Chat service test failed: {e}")
        return False


async def main():
    """主函数"""
    setup_logging()
    
    print("🚀 Starting system functionality tests...")
    
    # 检查环境变量
    from app.core.config import settings
    
    if not settings.ANTHROPIC_API_KEY and not settings.OPENAI_API_KEY:
        print("⚠️  Warning: No API keys found. Some tests may fail.")
        print("Please set ANTHROPIC_API_KEY or OPENAI_API_KEY in your .env file")
    
    # 运行测试
    tests = [
        ("RAG Service", test_rag_service),
        ("LLM Service", test_llm_service),
        ("Chat Service", test_chat_service),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = await test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # 显示测试结果
    print("\n📊 Test Results:")
    print("=" * 50)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if success:
            passed += 1
    
    print("=" * 50)
    print(f"Total: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! System is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the configuration.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())