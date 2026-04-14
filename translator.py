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
    logger.warning("googletrans not installed. Run: pip install googletrans==4.0.0-rc1")

# Check if OpenCC is available for S2T conversion
try:
    from opencc import OpenCC
    opencc_s2t = OpenCC('s2t')  # Simplified to Traditional
    OPENCC_AVAILABLE = True
except ImportError:
    OPENCC_AVAILABLE = False
    logger.warning("opencc-python-reinstalled not installed. Run: pip install opencc-python-reimplemented")

class Translator:
    def __init__(self):
        if TRANSLATOR_AVAILABLE:
            self.client = GoogleTranslator()
        self.cache: Dict[str, str] = {}
    
    def translate_to_chinese(self, text: str, src_lang: str = 'en') -> str:
        """Translate text to Traditional Chinese"""
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
    translator = Translator()
    translated_count = 0
    
    for article in articles:
        title = article.get('title', '')
        lang = article.get('lang', 'en')
        
        if lang == 'en' and title:
            translated_title = translator.translate_to_chinese(title, 'en')
            article['title'] = translated_title
            translated_count += 1
            time.sleep(delay)  # Respect rate limits
        
        # Also translate summary if exists
        summary = article.get('summary', '')
        if lang == 'en' and summary:
            article['summary'] = translator.translate_to_chinese(summary, 'en')
    
    logger.info(f"翻譯完成：{translated_count} 篇文章")
    return articles