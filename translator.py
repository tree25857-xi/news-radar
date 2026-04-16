#!/usr/bin/env python3
"""
NewsRadar - Google Translate Integration
Translates non-Chinese titles to Traditional Chinese for display
Uses Google Translate + OpenCC for S2T conversion
"""

import logging
import asyncio
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
    
    async def _translate_async(self, text: str, src_lang: str = 'en') -> str:
        """Async translate text to Traditional Chinese"""
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
            result = await self.client.translate(text, src=src_lang, dest='zh-cn')
            translated = result.text
            
            # Convert Simplified Chinese to Traditional Chinese
            if OPENCC_AVAILABLE:
                translated = opencc_s2t.convert(translated)
            
            self.cache[cache_key] = translated
            return translated
        except Exception as e:
            logger.warning(f"翻譯失敗: {e}")
            return text
    
    def translate_to_chinese(self, text: str, src_lang: str = 'en') -> str:
        """Sync wrapper for translate"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're already in an async context, create a new task
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(asyncio.run, self._translate_async(text, src_lang))
                    return future.result()
            else:
                return asyncio.run(self._translate_async(text, src_lang))
        except Exception as e:
            logger.warning(f"翻譯執行失敗: {e}")
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
    
    async def translate_all():
        nonlocal translated_count
        tasks = []
        
        for article in articles:
            title = article.get('title', '')
            lang = article.get('lang', 'en')
            
            if lang == 'en' and title:
                tasks.append((article, 'title', translator._translate_async(title, 'en')))
                translated_count += 1
            
            # Also translate summary if exists
            summary = article.get('summary', '')
            if lang == 'en' and summary:
                tasks.append((article, 'summary', translator._translate_async(summary, 'en')))
        
        # Execute all translations concurrently
        if tasks:
            results = await asyncio.gather(*[t[2] for t in tasks], return_exceptions=True)
            
            for i, (article, field, _) in enumerate(tasks):
                if isinstance(results[i], Exception):
                    logger.warning(f"翻譯錯誤: {results[i]}")
                else:
                    article[field] = results[i]
        
        await asyncio.sleep(delay)  # Respect rate limits
    
    try:
        asyncio.run(translate_all())
    except Exception as e:
        logger.warning(f"翻譯執行失敗: {e}")
    
    logger.info(f"翻譯完成：{translated_count} 篇文章")
    return articles