#!/bin/bash
cd /home/tree/.openclaw/workspace/news-radar
source .venv/bin/activate 2>/dev/null || true
SKIP_TRANSLATION=true python3 main.py --cron >> /tmp/update_news.log 2>&1

# 自動推送到 GitHub
cd /home/tree/.openclaw/workspace/news-radar
git add index.html
git commit -m "Auto update: $(date +%Y-%m-%d\ %H:%M)" 2>/dev/null
git push 2>/dev/null
