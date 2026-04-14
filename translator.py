"""
NewsRadar - Google Translate Integration
Translates non-Chinese titles to Chinese for display
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


class Translator:
    def __init__(self):
        if TRANSLATOR_AVAILABLE:
            self.client = GoogleTranslator()
        self.cache: Dict[str, str] = {}
    
    def translate_to_chinese(self, text: str, src_lang: str = 'en') -> str:
        """Translate text to Chinese"""
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
            result = self.client.translate(text, src=src_lang, dest='zh-tw')
            translated = result.text
            self.cache[cache_key] = translated
            return translated
        except Exception as e:
            logger.warning(f"翻譯失敗: {e}")
            return text
    
    def translate_batch(self, articles: List[Dict]) -> List[Dict]:
        """Translate all articles in batch"""
        for article in articles:
            if article["source_lang"] != "zh":
                translated = self.translate_to_chinese(article["title"], article["source_lang"])
                article["translated_title"] = translated
            else:
                article["translated_title"] = article["title"]
            time.sleep(0.2)  # Rate limiting
        
        return articles
    
    def _is_chinese(self, text: str) -> bool:
        """Check if text contains Chinese characters"""
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False


def translate_articles(articles: List[Dict]) -> List[Dict]:
    """Main entry point for translating articles"""
    translator = Translator()
    return translator.translate_batch(articles)


if __name__ == "__main__":
    test_articles = [
        {"title": "OpenAI announces GPT-5", "source_lang": "en", "translated_title": None},
        {"title": "This is in Chinese already", "source_lang": "zh", "translated_title": None},
    ]
    result = translate_articles(test_articles)
    for a in result:
        print(f"{a['title']} -> {a['translated_title']}")
