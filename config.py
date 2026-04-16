"""
RSS Feed Sources Configuration
8 categories with forex and commodities added
"""

FEEDS = {
    "AI": [
        # 英文 AI 信源
        {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/", "lang": "en"},
        {"name": "MIT Technology Review AI", "url": "https://www.technologyreview.com/feed/", "lang": "en"},
        {"name": "The Verge AI", "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "lang": "en"},
        {"name": "ArXiv CS.AI", "url": "https://arxiv.org/rss/cs.AI", "lang": "en"},
        {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/", "lang": "en"},
        {"name": "Wired AI", "url": "https://www.wired.com/feed/tag/ai/latest/rss", "lang": "en"},
        {"name": "VentureBeat", "url": "https://venturebeat.com/feed/", "lang": "en"},
        # 中文 AI 信源
        {"name": "機器之心", "url": "https://jiqizhixin.com/rss", "lang": "zh"},
        {"name": "36kr AI", "url": "https://36kr.com/feed/tag/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD", "lang": "zh"},
        {"name": "品玩 AI", "url": "https://www.pingwest.com/feed", "lang": "zh"},
        # AI 播客/新聞
        {"name": "Hugging Face Blog", "url": "https://huggingface.co/blog/feed.xml", "lang": "en"},
        {"name": "OpenAI Blog", "url": "https://openai.com/blog/rss/", "lang": "en"},
        {"name": "DeepMind Blog", "url": "https://deepmind.com/blog/feed/basic/", "lang": "en"},
        {"name": "Anthropic Blog", "url": "https://www.anthropic.com/blog/rss.xml", "lang": "en"},
        {"name": "AI News", "url": "https://www.artificialintelligence-news.com/feed/", "lang": "en"},
        {"name": "Last Week in AI", "url": "https://lastweekin.ai/feed", "lang": "en"},
        {"name": "The AI News", "url": "https://theAINews.beehiiv.com/feed", "lang": "en"},
    ],
    "網路安全": [
        {"name": "The Hacker News", "url": "https://feeds.feedburner.com/TheHackersNews", "lang": "en"},
        {"name": "Krebs on Security", "url": "https://krebsonsecurity.com/feed/", "lang": "en"},
        {"name": "Dark Reading", "url": "https://www.darkreading.com/rss.xml", "lang": "en"},
        {"name": "BleepingComputer", "url": "https://www.bleepingcomputer.com/feed/", "lang": "en"},
        {"name": "SecurityWeek", "url": "https://www.securityweek.com/feed/", "lang": "en"},
        {"name": "CyberScoop", "url": "https://www.cyberscoop.com/feed/", "lang": "en"},
    ],
    "經濟": [
        {"name": "Bloomberg Markets", "url": "https://www.bloomberg.com/feed/podcast/etp-rss.xml", "lang": "en"},
        {"name": "Financial Times", "url": "https://www.ft.com/?format=rss", "lang": "en"},
        {"name": "經濟日报", "url": "https://feed.udn.com.cn/rss/realtime.xml", "lang": "zh"},
    ],
    "科技": [
        {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "lang": "en"},
        {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index", "lang": "en"},
        {"name": "Wired", "url": "https://www.wired.com/feed/rss", "lang": "en"},
        {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "lang": "en"},
        {"name": "Engadget", "url": "https://www.engadget.com/rss.xml", "lang": "en"},
    ],
    "國際": [
        {"name": "BBC World", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "lang": "en"},
        {"name": "Reuters World", "url": "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best", "lang": "en"},
        {"name": "AP News", "url": "https://apnews.com/rss", "lang": "en"},
        {"name": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml", "lang": "en"},
        {"name": "DW World", "url": "https://rss.dw.com/rdf/rss-en-world", "lang": "en"},
        {"name": "NHK World", "url": "https://www3.nhk.or.jp/rss/news/c0.xml", "lang": "en"},
        {"name": "France24", "url": "https://www.france24.com/en/rss", "lang": "en"},
    ],
    "金融": [
        {"name": "Yahoo 台股", "url": "https://tw.stock.yahoo.com/news", "lang": "zh"},
        {"name": "Seeking Alpha", "url": "https://seekingalpha.com/feed.xml", "lang": "en"},
        {"name": "CoinDesk", "url": "https://www.coindesk.com/arc/outboundfeeds/rss/", "lang": "en"},
        {"name": "CoinTelegraph", "url": "https://cointelegraph.com/rss", "lang": "en"},
        {"name": "FX Street", "url": "https://www.fxstreet.com/rss/news.aspx", "lang": "en"},
        {"name": "Investing.com", "url": "https://www.investing.com/rss/news.rss", "lang": "en"},
        {"name": "MarketWatch", "url": "http://feeds.marketwatch.com/marketwatch/topstories/", "lang": "en"},
    ],
    "外匯市場": [
        {"name": "FX Street Forex", "url": "https://www.fxstreet.com/rss/news.aspx", "lang": "en"},
        {"name": "Investing.com Forex", "url": "https://www.investing.com/rss/forex.rss", "lang": "en"},
        {"name": "DailyFX", "url": "https://www.dailyfx.com/feeds/jforex", "lang": "en"},
        {"name": "Forex Crunch", "url": "https://www.forexcrunch.com/feed/", "lang": "en"},
        {"name": "BabyPips", "url": "https://www.babypips.com/feed", "lang": "en"},
    ],
    "商品期貨": [
        {"name": "Investing.com Commodities", "url": "https://www.investing.com/rss/commodities.rss", "lang": "en"},
        {"name": "Oil Price", "url": "https://oilprice.com/feed/", "lang": "en"},
        {"name": "Kitco News", "url": "https://www.kitco.com/rss/", "lang": "en"},
        {"name": "SGX Commodities", "url": "https://www.sgx.com/rss/feed-products-forex", "lang": "en"},
        {"name": "CME Group", "url": "https://www.cmegroup.com/rss/marketdata/latest20.rss", "lang": "en"},
    ],
}

# 每個分類的最大文章數量
MAX_ARTICLES_PER_CATEGORY = 100

# 關鍵詞分類系統
CATEGORY_KEYWORDS = {
    "AI": [
        "ai", "artificial intelligence", "machine learning", "deep learning",
        "neural network", "gpt", "llm", "chatgpt", "openai", "anthropic",
        "claude", "gemini", "copilot", "stable diffusion", "midjourney",
        "transformer", "nlp", "nlu", "computer vision", "大模型", "人工智能",
        "機器學習", "深度學習", "生成式 AI", "langchain", "hugging face",
        "diffusion", "multimodal", "foundation model", "agi",
        "自動駕駛", "機器人", "人形機器人", "智慧", "智能", "算力",
    ],
    "網路安全": [
        "security", "cybersecurity", "hack", "breach", "vulnerability",
        "malware", "ransomware", "phishing", "cyber attack", "data leak",
        "cve", "zero-day", "exploit", "firewall", "encryption", "privacy",
        "dark web", "cybercrime", "threat", "infosec", "資安", "網路安全",
        "駭客", "漏洞", "攻擊", "洩漏", "加密", "後門", "木馬", "病毒",
        "APT", "DDoS", "botnet", "spyware", "adware", "rootkit",
    ],
    "經濟": [
        "economy", "economic", "gdp", "inflation", "recession", "market",
        "stock", "bond", "fed", "interest rate", "交易", "經濟", "央行",
        "升息", "降息", "通膨", "GDP", "貿易", "進出口", "半導體", "景氣",
    ],
    "科技": [
        "tech", "technology", "software", "hardware", "startup", "app",
        "smartphone", "laptop", "computer", "device", "科技", "軟體", "硬體",
        "新品", "發表", "蘋果", "Google", "Meta", "Microsoft", "Amazon",
    ],
    "國際": [
        "world", "global", "international", "war", "conflict", "diplomacy",
        "un", "politics", "election", "國際", "世界", "戰爭", "政治", "外交",
        "總統", "政府", "協議", "談判", "歐洲", "亞洲", "中東", "烏克蘭",
    ],
    "金融": [
        "stock", "market", "trading", "invest", "finance", "bitcoin", "crypto",
        "forex", "currency", "bond", "fund", "etf", "Nasdaq", "Dow", "S&P",
        "股價", "交易所", "上市", "財報", "營收", "加密貨幣", "比特幣", "以太幣",
        "外匯", "USD", "EUR", "JPY", "台股", "美股", "期貨", "選擇權",
    ],
    "外匯市場": [
        "forex", "fx", "currency", "usd", "eur", "jpy", "gbp", "chf", "aud", "cad", "nzд",
        "外匯", "匯率", "美元", "歐元", "日圓", "英鎊", "瑞士法郎",
        "trading", "pip", "spread", "leverage", "margin", "lot",
        "外匯交易", "外幣", "換匯", "貶值", "升值", "央行干預",
    ],
    "商品期貨": [
        "commodity", "futures", "oil", "gold", "silver", "copper", "natural gas",
        "cme", "nymex", "comex", "ice", "大宗商品", "期貨", "原油", "黃金",
        "白銀", "銅", "天然氣", "農產品", "大豆", "小麥", "玉米",
        "商品價格", "供需", "庫存", "OPEC", "庫存報告",
        "wti", "brent", "crude", "precious metals", "base metals",
    ],
}

TRANSLATE_DELAY = 0.5
