#!/usr/bin/env python3
"""
Gemini AI 摘要生成器 v2
"""

import os
import requests
import json
import re

# 從環境變數讀取 API Key，預設值為直接設定（過渡期）
API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyANsR1k6UEC6Sl1VvxDwJNufbPF9uZjXUA')
MODEL = "gemini-2.5-flash"

def generate_summary(news_items, category="一般"):
    """用 Gemini 生成新聞摘要"""
    
    if not news_items:
        return None
    
    # 組合新聞標題
    headlines = "\n".join([f"- {n['title']}" for n in news_items[:8]])
    
    prompt = f"""你是一個新聞分析師。請為以下{category}領域的新聞生成一個簡短的摘要（50字內）和三個標籤。

新聞標題：
{headlines}

重要：請只回傳一個JSON物件，格式如下（不要陣列，不要其他文字）：
{{"summary": "摘要文字", "tags": ["標籤1", "標籤2", "標籤3"]}}
"""
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3, 
            "maxOutputTokens": 150,
            "thinkingConfig": {"thinkingBudget": 0}  # 禁用思考模式
        }
    }
    
    try:
        r = requests.post(url, json=payload, timeout=30)
        if r.status_code == 200:
            data = r.json()
            
            # 安全的取值
            candidates = data.get('candidates', [])
            if not candidates:
                print(f"❌ 無候選回覆")
                return None
            
            first_candidate = candidates[0]
            content = first_candidate.get('content', {})
            parts = content.get('parts', [])
            if not parts:
                print(f"❌ 無回覆內容")
                return None
            
            text = parts[0].get('text', '')
            if not text:
                print(f"❌ 回覆文字為空")
                return None
            
            # 解析 JSON
            text = text.strip()
            # 移除 markdown code block
            text = re.sub(r'^```json\s*', '', text)
            text = re.sub(r'^```\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
            
            result = json.loads(text)
            
            # 如果是陣列，取第一個元素
            if isinstance(result, list):
                result = result[0] if result else None
            
            # 如果成功且是 dict，返回結果
            if isinstance(result, dict) and 'summary' in result:
                return result
            else:
                print(f"❌ 無效的回覆格式: {type(result)}")
                return None
        else:
            print(f"❌ API 錯誤: {r.status_code}")
            return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析錯誤: {e}")
        print(f"   原始回覆: {text[:200]}...")
        return None
    except Exception as e:
        print(f"❌ 例外: {e}")
        return None

def summarize_all(news_by_category):
    """為每個類別生成摘要"""
    results = {}
    
    for category, news in news_by_category.items():
        print(f"  📝 {category}...")
        result = generate_summary(news, category)
        if result:
            results[category] = result
            print(f"    ✓ {result.get('summary', '')[:40]}...")
        else:
            results[category] = {"summary": "無可用摘要", "tags": []}
        
        # 加入延遲避免 rate limit
        import time
        time.sleep(3)
    
    return results

if __name__ == '__main__':
    # 測試
    test_news = [
        {"title": "台積電公佈財報營收創新高"},
        {"title": "AI 需求帶動半導體股上漲"},
        {"title": "美股三大指數創新高"},
    ]
    
    result = generate_summary(test_news, "科技")
    print("✅ 測試成功！")
    if result:
        print("摘要:", result.get('summary'))
        print("標籤:", result.get('tags'))