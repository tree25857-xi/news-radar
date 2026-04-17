"""
NewsRadar - Scheduler
Handles periodic news updates via cron or GitHub Actions
"""

import sys
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_update():
    """Run a complete news update cycle"""
    from collector import collect_news
    from translator import translate_articles
    from classifier import classify_articles
    from ai_summarizer import summarize_all
    from html_generator import generate_html
    
    logger.info("🚀 開始 NewsRadar 更新...")
    start = datetime.now()
    
    # Step 1: Collect
    logger.info("📡 步驟 1/5: 蒐集 RSS 信源...")
    articles = collect_news()
    
    if not articles:
        logger.warning("未取得任何文章")
        return
    
    # Step 2: Classify
    logger.info("🏷️ 步驟 2/5: 分類文章...")
    articles = classify_articles(articles)
    
    # Step 3: Translate
    skip_translate = os.environ.get("SKIP_TRANSLATION", "false").lower() in ("1", "true", "yes")
    
    if skip_translate:
        logger.info("⏭️ 翻譯已跳過（SKIP_TRANSLATION=true）")
    else:
        logger.info("🌐 步驟 3/5: 翻譯標題...")
        try:
            articles = translate_articles(articles)
        except Exception as e:
            logger.warning(f"翻譯失敗: {e}")
    
    # Step 4: AI Summary (可選功能)
    logger.info("🤖 步驟 4/5: AI 生成摘要...")
    skip_ai = os.environ.get("SKIP_AI_SUMMARY", "true").lower() in ("1", "true", "yes")
    
    if skip_ai:
        logger.info("⏭️ AI 摘要功能已停用（SKIP_AI_SUMMARY=true）")
    else:
        try:
            from collections import defaultdict
            news_by_cat = defaultdict(list)
            for a in articles:
                cat = a.get('predicted_category', a.get('category', '其他'))
                news_by_cat[cat].append(a)
            
            ai_results = summarize_all(dict(news_by_cat))
            
            # 附加 AI 摘要到文章
            for a in articles:
                cat = a.get('predicted_category', a.get('category', '其他'))
                if cat in ai_results:
                    a['ai_summary'] = ai_results[cat].get('summary', '')
                    a['ai_tags'] = ai_results[cat].get('tags', [])
        except Exception as e:
            logger.warning(f"AI 摘要失敗: {e}")
    
    # Step 5: Generate HTML
    logger.info("📄 步驟 5/5: 生成 HTML 頁面...")
    
    # Stats
    from collections import Counter
    stats = Counter(a.get("predicted_category", a["category"]) for a in articles)
    stats = dict(stats)
    
    output_path = os.path.join(os.path.dirname(__file__), "output", "index.html")
    generate_html(articles, output_path, stats)
    
    elapsed = (datetime.now() - start).total_seconds()
    logger.info(f"✅ 更新完成！取得 {len(articles)} 篇文章，耗時 {elapsed:.1f} 秒")
    
    return articles


if __name__ == "__main__":
    run_update()
