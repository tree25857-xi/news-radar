"""
NewsRadar - RSS Feed Collector
Reads RSS feeds and collects articles with metadata
"""

import feedparser
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib

from config import FEEDS, CATEGORY_KEYWORDS, TRANSLATE_DELAY

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class NewsCollector:
    def __init__(self, max_workers: int = 10, timeout: int = 15):
        self.max_workers = max_workers
        self.timeout = timeout
        self.articles: List[Dict] = []
        
    def collect_all(self) -> List[Dict]:
        """Collect all articles from all feeds"""
        all_feeds = []
        for category, feeds in FEEDS.items():
            for feed in feeds:
                all_feeds.append((category, feed))
        
        logger.info(f"開始蒐集 {len(all_feeds)} 個 RSS 信源...")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._fetch_feed, cat, feed): (cat, feed)
                for cat, feed in all_feeds
            }
            
            for future in as_completed(futures):
                cat, feed = futures[future]
                try:
                    articles = future.result()
                    logger.info(f"✓ {feed['name']}: 取得 {len(articles)} 篇文章")
                except Exception as e:
                    logger.error(f"✗ {feed['name']}: {str(e)}")
        
        # Remove duplicates
        unique_articles = self._deduplicate(self.articles)
        logger.info(f"總計取得 {len(unique_articles)} 篇不重複文章")
        return unique_articles
    
    def _fetch_feed(self, category: str, feed_info: Dict) -> List[Dict]:
        """Fetch a single RSS feed"""
        articles = []
        try:
            # Use requests to fetch with timeout, then parse with feedparser
            resp = requests.get(feed_info["url"], timeout=self.timeout, headers={
                'User-Agent': 'NewsRadar/1.0'
            })
            resp.raise_for_status()
            parsed = feedparser.parse(resp.content)
            
            for entry in parsed.entries[:30]:  # Limit to 30 per feed
                article = self._parse_entry(entry, category, feed_info)
                if article:
                    articles.append(article)
                    self.articles.append(article)
            
            time.sleep(TRANSLATE_DELAY)
        except Exception as e:
            logger.warning(f"抓取失敗 {feed_info['name']}: {e}")
        
        return articles
    
    def _parse_entry(self, entry, category: str, feed_info: Dict) -> Optional[Dict]:
        """Parse a single RSS entry"""
        try:
            # Get title
            title = getattr(entry, 'title', '') or ''
            title = title.strip()
            if not title:
                return None
            
            # Get link
            link = getattr(entry, 'link', '') or ''
            
            # Get description/summary
            description = ''
            if hasattr(entry, 'summary'):
                description = self._clean_html(entry.summary)
            elif hasattr(entry, 'description'):
                description = self._clean_html(entry.description)
            
            # Get published date
            published = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                try:
                    from time import mktime
                    published = datetime.fromtimestamp(mktime(entry.published_parsed))
                except:
                    published = datetime.now()
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                try:
                    from time import mktime
                    published = datetime.fromtimestamp(mktime(entry.updated_parsed))
                except:
                    published = datetime.now()
            else:
                published = datetime.now()
            
            # Generate unique ID
            article_id = hashlib.md5(f"{link}{title}".encode()).hexdigest()[:16]
            
            return {
                "id": article_id,
                "title": title,
                "link": link,
                "description": description[:500] if description else '',
                "category": category,
                "source": feed_info["name"],
                "source_lang": feed_info["lang"],
                "published": published,
                "translated_title": None,
                "summary": None,
            }
        except Exception as e:
            logger.warning(f"解析文章失敗: {e}")
            return None
    
    def _clean_html(self, text: str) -> str:
        """Remove HTML tags from text"""
        import re
        if not text:
            return ''
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _deduplicate(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on title similarity"""
        seen_titles = set()
        unique = []
        
        for article in articles:
            title_lower = article["title"].lower()
            # Simple deduplication: check if similar title exists
            is_duplicate = False
            for seen in seen_titles:
                if self._title_similarity(title_lower, seen) > 0.8:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                seen_titles.add(title_lower)
                unique.append(article)
        
        # Sort by published date (newest first)
        unique.sort(key=lambda x: x["published"], reverse=True)
        return unique
    
    def _title_similarity(self, s1: str, s2: str) -> float:
        """Calculate simple title similarity"""
        words1 = set(s1.split())
        words2 = set(s2.split())
        if not words1 or not words2:
            return 0.0
        intersection = words1 & words2
        union = words1 | words2
        return len(intersection) / len(union) if union else 0.0


def collect_news() -> List[Dict]:
    """Main entry point for collecting news"""
    collector = NewsCollector()
    return collector.collect_all()


if __name__ == "__main__":
    articles = collect_news()
    print(f"取得 {len(articles)} 篇文章")
    for a in articles[:5]:
        print(f"  [{a['category']}] {a['title'][:60]}...")
