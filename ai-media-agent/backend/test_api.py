#!/usr/bin/env python3
"""
测试OpenRouter API连接
"""
import json
import urllib.request

OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def test_api():
    """测试API连接"""
    print("测试OpenRouter API连接...")
    
    # 尝试不同的模型
    models_to_try = [
        "google/gemini-pro",
        "google/gemini-flash-1.5",
        "openai/gpt-3.5-turbo",
        "meta-llama/llama-3.2-3b-instruct:free"
    ]
    
    for model in models_to_try:
        print(f"\n尝试模型: {model}")
        request_data = {
            "model": model,
            "messages": [
                {"role": "user", "content": "什么是AI自媒体？用一句话回答"}
            ],
            "max_tokens": 100
        }
        
        try:
            req = urllib.request.Request(
                OPENROUTER_API_URL,
                data=json.dumps(request_data).encode('utf-8'),
                headers={
                    'Authorization': f'Bearer {OPENROUTER_API_KEY}',
                    'Content-Type': 'application/json',
                    'HTTP-Referer': 'http://localhost:8000',
                    'X-Title': 'Test'
                }
            )
            
            with urllib.request.urlopen(req, timeout=20) as response:
                result = json.loads(response.read().decode('utf-8'))
                print(f"✅ 模型 {model} 连接成功！")
                if 'choices' in result:
                    print(f"回答: {result['choices'][0]['message']['content']}")
                    return  # 找到可用模型，退出
        
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            error_json = json.loads(error_body)
            print(f"❌ {model}: {error_json.get('error', {}).get('message', 'Unknown error')}")
        except Exception as e:
            print(f"❌ {model}: {e}")

if __name__ == "__main__":
    test_api()