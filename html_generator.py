"""
NewsRadar - HTML Page Generator
Generates a beautiful, responsive news aggregation page
"""

import os
from datetime import datetime
from typing import List, Dict
from collections import defaultdict

# Category icons and colors
CATEGORY_STYLE = {
    "AI": {"icon": "🤖", "color": "#a78bfa", "bg": "#1e1b4b"},
    "網路安全": {"icon": "🔒", "color": "#f87171", "bg": "#4a0519"},
    "經濟": {"icon": "📈", "color": "#34d399", "bg": "#022c22"},
    "科技": {"icon": "💻", "color": "#60a5fa", "bg": "#0c1929"},
    "國際": {"icon": "🌍", "color": "#fbbf24", "bg": "#422006"},
}

DEFAULT_STYLE = {"icon": "📰", "color": "#6b7280", "bg": "#f9fafb"}

CATEGORY_STYLE["金融"] = {"icon": "💹", "color": "#f59e0b", "bg": "#422006"}


def generate_html(articles: List[Dict], output_path: str = "output/index.html",
                  stats: Dict = None, last_update: str = None) -> str:
    """Generate the complete HTML page"""
    
    if last_update is None:
        last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Group articles by category
    categorized = defaultdict(list)
    for article in articles:
        cat = article.get("predicted_category", article["category"])
        categorized[cat].append(article)
    
    # Build HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NewsRadar - 新聞雷達</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #3b82f6;
            --bg: #0f0f23;
            --card-bg: #1a1a3e;
            --text: #e2e8f0;
            --text-muted: #94a3b8;
            --border: #334155;
            --hover: #1e293b;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Noto Sans TC', 'Inter', -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
            color: white;
            padding: 2rem 1rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }}
        
        .header-content {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        
        .header p {{
            opacity: 0.9;
            font-size: 1.1rem;
        }}
        
        .stats-bar {{
            background: white;
            border-bottom: 1px solid var(--border);
            padding: 1rem;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        
        .stats-content {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
        }}
        
        .stats-left {{
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }}
        
        .stat-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.4rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            transition: transform 0.2s;
        }}
        
        .stat-badge:hover {{
            transform: translateY(-2px);
        }}
        
        .last-update {{
            color: var(--text-muted);
            font-size: 0.85rem;
        }}
        
        .main-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }}
        
        .category-section {{
            margin-bottom: 3rem;
        }}
        
        .category-header {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1.5rem;
            padding: 0.75rem 1rem;
            border-bottom: 2px solid;
            border-radius: 8px 8px 0 0;
            background: rgba(251, 191, 36, 0.05);
        }}
        
        .category-icon {{
            font-size: 1.8rem;
        }}
        
        .category-title {{
            font-size: 1.5rem;
            font-weight: 700;
        }}
        
        .category-count {{
            background: var(--text-muted);
            color: white;
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.8rem;
            margin-left: auto;
        }}
        
        .articles-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1.5rem;
        }}
        
        .article-card {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            border: 1px solid var(--border);
            display: flex;
            flex-direction: column;
        }}
        
        .article-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }}
        
        .article-header {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            margin-bottom: 0.75rem;
        }}
        
        .article-source {{
            font-size: 0.75rem;
            color: var(--text-muted);
            font-weight: 500;
        }}
        
        .article-time {{
            font-size: 0.7rem;
            color: var(--text-muted);
        }}
        
        .article-title {{
            font-size: 1rem;
            font-weight: 600;
            line-height: 1.5;
            margin-bottom: 0.75rem;
            flex-grow: 1;
        }}
        
        .article-title a {{
            color: var(--text);
            text-decoration: none;
            transition: color 0.2s;
        }}
        
        .article-title a:hover {{
            color: var(--primary);
        }}
        
        .article-translated {{
            font-size: 0.85rem;
            color: var(--text-muted);
            background: var(--hover);
            padding: 0.5rem 0.75rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
            font-style: italic;
        }}
        
        .article-description {{
            font-size: 0.85rem;
            color: var(--text-muted);
            line-height: 1.5;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .article-summary {{
            margin-top: 0.75rem;
            padding: 0.75rem;
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            border-radius: 8px;
            font-size: 0.8rem;
            color: #0369a1;
        }}
        
        .article-summary-label {{
            font-weight: 600;
            margin-bottom: 0.25rem;
        }}
        
        .footer {{
            text-align: center;
            padding: 2rem;
            color: var(--text-muted);
            font-size: 0.85rem;
            border-top: 1px solid var(--border);
            margin-top: 3rem;
        }}
        
        .refresh-btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: var(--primary);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 500;
            transition: background 0.2s;
        }}
        
        .refresh-btn:hover {{
            background: #1d4ed8;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.8rem; }}
            .articles-grid {{
                grid-template-columns: 1fr;
            }}
            .stats-content {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
        
        /* Animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .category-section {{
            animation: fadeIn 0.5s ease forwards;
        }}
        
        .category-section:nth-child(1) {{ animation-delay: 0.1s; }}
        .category-section:nth-child(2) {{ animation-delay: 0.2s; }}
        .category-section:nth-child(3) {{ animation-delay: 0.3s; }}
        .category-section:nth-child(4) {{ animation-delay: 0.4s; }}
        .category-section:nth-child(5) {{ animation-delay: 0.5s; }}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <h1>📡 NewsRadar 新聞雷達</h1>
            <p>AI 驅動的新聞聚合平台 | 掌握全球最新資訊</p>
        </div>
    </header>
    
    <div class="stats-bar">
        <div class="stats-content">
            <div class="stats-left">
                {''.join(_generate_stat_badges(stats or {}))}
            </div>
            <div class="last-update">
                🔄 更新時間: {last_update}
            </div>
        </div>
    </div>
    
    <main class="main-content">
        {''.join(_generate_category_sections(categorized))}
    </main>
    
    <footer class="footer">
        <p>NewsRadar 新聞雷達 | 自動更新</p>
        <p style="margin-top: 0.5rem;">
            <a href="." class="refresh-btn">🔄 重新整理</a>
        </p>
    </footer>
</body>
</html>"""
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_path


def _generate_stat_badges(stats: Dict) -> List[str]:
    """Generate stat badges HTML"""
    badges = []
    for cat, count in stats.items():
        style = CATEGORY_STYLE.get(cat, DEFAULT_STYLE)
        badges.append(
            f'<span class="stat-badge" style="background: {style["bg"]}; color: {style["color"]};">'
            f'{style["icon"]} {cat}: {count}'
            f'</span>'
        )
    return badges


def _generate_category_sections(categorized: Dict) -> List[str]:
    """Generate category sections HTML"""
    sections = []
    for cat in ["AI", "網路安全", "科技", "經濟", "國際"]:
        articles = categorized.get(cat, [])
        if not articles:
            continue
        
        style = CATEGORY_STYLE.get(cat, DEFAULT_STYLE)
        
        cards_html = ''
        for article in articles[:20]:  # Limit to 20 per category
            cards_html += _generate_article_card(article, style)
        
        section = f"""
        <section class="category-section">
            <div class="category-header" style="border-color: {style['color']};">
                <span class="category-icon">{style['icon']}</span>
                <h2 class="category-title">{cat}</h2>
                <span class="category-count" style="background: {style['color']};">{len(articles)} 篇</span>
            </div>
            <div class="articles-grid">
                {cards_html}
            </div>
        </section>
        """
        sections.append(section)
    
    return sections


def _generate_article_card(article: Dict, style: Dict) -> str:
    """Generate a single article card HTML"""
    title = article.get("title", "")
    link = article.get("link", "#")
    translated = article.get("translated_title", "")
    description = article.get("description", "")
    source = article.get("source", "")
    summary = article.get("summary", "")
    published = article.get("published")
    
    time_str = ""
    if published:
        if isinstance(published, datetime):
            time_str = published.strftime("%m/%d %H:%M")
        else:
            time_str = str(published)[:16]
    
    translated_html = ""
    if translated and translated != title:
        translated_html = f'<div class="article-translated">{translated}</div>'
    
    summary_html = ""
    if summary:
        summary_html = f'''
        <div class="article-summary">
            <div class="article-summary-label">📝 AI 摘要</div>
            {summary}
        </div>
        '''
    
    desc_html = ""
    if description:
        desc_html = f'<div class="article-description">{description}</div>'
    
    return f"""
    <article class="article-card">
        <div class="article-header">
            <span class="article-source">{source}</span>
            <span class="article-time">{time_str}</span>
        </div>
        <h3 class="article-title">
            <a href="{link}" target="_blank" rel="noopener">{title}</a>
        </h3>
        {translated_html}
        {desc_html}
        {summary_html}
    </article>
    """


if __name__ == "__main__":
    # Test with sample data
    test_articles = [
        {
            "title": "OpenAI Releases GPT-5 with Revolutionary Capabilities",
            "link": "https://example.com/1",
            "description": "The new model shows unprecedented performance...",
            "category": "AI",
            "predicted_category": "AI",
            "source": "TechCrunch",
            "source_lang": "en",
            "translated_title": "OpenAI 發布具有革命性能力的 GPT-5",
            "published": datetime.now(),
        }
    ]
    generate_html(test_articles)
    print("HTML generated successfully!")
