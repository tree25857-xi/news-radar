# 📡 NewsRadar 新聞雷達

AI 驅動的新聞聚合平台，自動蒐集、分類、翻譯全球新聞。

## ✨ 功能

- 🤖 **38 個 RSS 信源** 覆蓋 5 大領域
- 🏷️ **關鍵詞自動分類** (AI、網路安全、經濟、科技、國際)
- 🌐 **Google Translate 翻譯** 英文標題為中文
- 📝 **AI 摘要生成** (需 Groq API Key)
- 📱 **美觀的響應式 HTML 頁面**
- ⏰ **定時自動更新** (GitHub Actions / Cron)

## 📊 信源分佈

| 領域 | 信源數 |
|------|--------|
| AI | 17 |
| 網路安全 | 6 |
| 經濟 | 3 |
| 科技 | 5 |
| 國際 | 7 |

## 🚀 快速開始

### 本地運行

```bash
# 安裝依賴
pip install -r requirements.txt

# 單次運行
python main.py

# 自動更新模式（每 30 分鐘）
python main.py --serve

# Cron 模式
python main.py --cron
```

### GitHub Actions

推送後自動每 4 小時更新一次，输出到 `gh-pages` 分支。

## 📁 目錄結構

```
news-radar/
├── collector.py          # RSS 蒐集
├── translator.py          # 翻譯
├── classifier.py         # 分類
├── html_generator.py     # HTML 生成
├── scheduler.py          # 定時任務
├── config.py             # RSS Feeds 配置
├── main.py               # 入口
├── requirements.txt
├── .github/workflows/
│   └── news.yml          # GitHub Actions
└── output/
    └── index.html        # 輸出頁面
```

## ⚙️ 配置

### RSS 信源

編輯 `config.py` 中的 `FEEDS` 字典添加或修改信源。

### Groq AI 摘要

```bash
export GROQ_API_KEY="your-api-key"
```

## 🌐 輸出示例

生成的 `output/index.html` 包含：
- 每個分類的新聞卡片
- 翻譯後的中文標題
- AI 生成的摘要（如有）
- 響應式設計（支援移動端）
