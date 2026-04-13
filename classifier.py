"""
NewsRadar - Keyword-based Article Classifier
Automatically classifies articles into categories based on keywords
"""

import logging
from typing import List, Dict, Tuple
from config import CATEGORY_KEYWORDS

logger = logging.getLogger(__name__)


class ArticleClassifier:
    def __init__(self):
        self.keywords = CATEGORY_KEYWORDS
    
    def classify(self, article: Dict) -> str:
        """Classify a single article into a category"""
        title = article.get("title", "").lower()
        description = article.get("description", "").lower()
        text = f"{title} {description}"
        
        scores = {}
        for category, keywords in self.keywords.items():
            score = self._calculate_score(text, keywords)
            if score > 0:
                scores[category] = score
        
        if not scores:
            return article.get("category", "國際")  # Default
        
        # Return category with highest score
        return max(scores, key=scores.get)
    
    def _calculate_score(self, text: str, keywords: List[str]) -> float:
        """Calculate match score for a category"""
        score = 0.0
        for keyword in keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in text:
                # Exact match counts more
                score += 1.0
                # Bonus for word boundaries
                import re
                if re.search(r'\b' + re.escape(keyword_lower) + r'\b', text):
                    score += 0.5
        
        return score
    
    def classify_batch(self, articles: List[Dict]) -> List[Dict]:
        """Classify all articles"""
        for article in articles:
            predicted = self.classify(article)
            article["predicted_category"] = predicted
            # Keep original category but note prediction
            if article["predicted_category"] != article["category"]:
                logger.debug(f"重新分類: {article['title'][:40]} -> {predicted}")
        
        return articles
    
    def get_category_stats(self, articles: List[Dict]) -> Dict[str, int]:
        """Get statistics of articles per category"""
        stats = {cat: 0 for cat in self.keywords.keys()}
        for article in articles:
            cat = article.get("predicted_category", article["category"])
            if cat in stats:
                stats[cat] += 1
        return stats


def classify_articles(articles: List[Dict]) -> List[Dict]:
    """Main entry point for classifying articles"""
    classifier = ArticleClassifier()
    return classifier.classify_batch(articles)


if __name__ == "__main__":
    test_article = {
        "title": "New AI model breaks records in image recognition",
        "description": "A new deep learning approach achieves state-of-the-art results",
        "category": "AI"
    }
    classifier = ArticleClassifier()
    result = classifier.classify(test_article)
    print(f"分類結果: {result}")
