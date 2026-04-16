#!/usr/bin/env python3
"""
NewsRadar - Google Translate Integration
Translates non-Chinese titles to Traditional Chinese for display
Uses Google Translate + OpenCC for S2T conversion
"""

import logging
from typing import List, Dict
import time

logger = logging.getLogger(__name__)

# Check if googletrans is available
try:
    from googletrans import Translator as GoogleTranslator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False
    logger.warning("googletrans not installed. Run: pip install googletrans==4.0.2")

# Check if OpenCC is available for S2T conversion
try:
    import opencc
    OPENCC_AVAILABLE = True
    try:
        opencc_s2t = opencc.OpenCC('s2t')
    except:
        OPENCC_AVAILABLE = False
except ImportError:
    OPENCC_AVAILABLE = False
    logger.warning("OpenCC not installed. Chinese conversion disabled.")


class GoogleTranslatorClient:
    def __init__(self):
        if TRANSLATOR_AVAILABLE:
            self.client = GoogleTranslator()
        self.cache: Dict[str, str] = {}
    
    def translate_to_chinese(self, text: str, src_lang: str = 'en') -> str:
        """Translate text to Traditional Chinese (sync)"""
        if not text:
            return ''
        
        # Don't translate if already Chinese
        if self._is_chinese(text):
            return text
        
        # Check cache
        cache_key = f"{src_lang}:{text}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        if not TRANSLATOR_AVAILABLE:
            return text  # Return original if no translator
        
        try:
            # googletrans 4.x is sync
            result = self.client.translate(text, src=src_lang, dest='zh-cn')
            translated = result.text
            
            # Convert Simplified Chinese to Traditional Chinese
            if OPENCC_AVAILABLE:
                translated = opencc_s2t.convert(translated)
            
            self.cache[cache_key] = translated
            return translated
        except Exception as e:
            logger.warning(f"翻譯失敗: {e}")
            return text
    
    def _is_chinese(self, text: str) -> bool:
        """Check if text contains Chinese characters"""
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False


def translate_articles(articles: List[Dict], delay: float = 0.5) -> List[Dict]:
    """Translate all article titles to Traditional Chinese"""
    translator = GoogleTranslatorClient()
    translated_count = 0
    
    for article in articles:
        title = article.get('title', '')
        lang = article.get('source_lang', 'en')
        
        if lang == 'en' and title:
            article['title'] = translator.translate_to_chinese(title, 'en')
            translated_count += 1
        
        # Also translate summary if exists
        summary = article.get('summary', '')
        if lang == 'en' and summary:
            article['summary'] = translator.translate_to_chinese(summary, 'en')
        
        # Small delay to respect rate limits
        if translated_count % 10 == 0:
            time.sleep(delay)
    
    logger.info(f"翻譯完成：{translated_count} 篇文章")
    return articles


if __name__ == '__main__':
    # Test
    test_articles = [
        {"title": "Breaking: AI achieves new milestone", "lang": "en"},
        {"title": "Climate change affects global markets", "lang": "en"},
    ]
    
    result = translate_articles(test_articles)
    for a in result:
        print(f"  [{a['lang']}] {a['title']}")
