#!/bin/bash
# ============================================================
# NewsRadar 自動更新（伺服器版）
# 2026-11-26 重寫：原本寫死 /home/tree/...（樹的電腦），改成伺服器路徑
#
# 執行環境：伺服器無 pip/ensurepip → 依賴裝在 /home/node/.openclaw/venvs/news-radar-libs
# 認證：GitHub credential store（repo 外，remote URL 不含 token）
# ============================================================
set -uo pipefail

RADAR_DIR="/home/node/.openclaw/workspace/projects/news-radar"
PYLIBS="/home/node/.openclaw/venvs/news-radar-libs"
LOGFILE="/home/node/.openclaw/workspace/log/news-radar.log"
STATUSFILE="/home/node/.openclaw/workspace/log/news-radar.status"

mkdir -p "$(dirname "$LOGFILE")"
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOGFILE"; }

cd "$RADAR_DIR" || { log "❌ 目錄不存在：$RADAR_DIR"; exit 1; }

export PYTHONPATH="$PYLIBS:${PYTHONPATH:-}"
export SKIP_TRANSLATION="${SKIP_TRANSLATION:-true}"

log "📡 開始抓取 RSS…"
OUT=$(python3 main.py --cron 2>&1)
echo "$OUT" >> "$LOGFILE"

COUNT=$(echo "$OUT" | grep -oE "取得 [0-9]+ 篇" | grep -oE "[0-9]+" | tail -1)
if [ -z "$COUNT" ] || [ "$COUNT" -lt 1 ]; then
  log "❌ 未取得文章，更新失敗"
  echo "error no-articles $(date -u +%FT%TZ)" > "$STATUSFILE"
  exit 1
fi
log "✅ 取得 $COUNT 篇文章"

# ── 只有 index.html 與 output/ 會變動 ──
git add index.html output/ 2>/dev/null

if git diff --cached --quiet; then
  log "ℹ️ 內容無變更，不產生 commit"
  echo "ok $COUNT nochange $(date -u +%FT%TZ)" > "$STATUSFILE"
  exit 0
fi

git commit -q -m "Auto update: $(date '+%Y-%m-%d %H:%M')" || { log "❌ commit 失敗"; exit 1; }

# ── 推送（credential store 自動供應憑證）──
if git push origin main 2>&1 | tee -a "$LOGFILE"; then
  SHA=$(git rev-parse --short HEAD)
  log "✅ 已推送：$SHA"
  echo "ok $COUNT $SHA $(date -u +%FT%TZ)" > "$STATUSFILE"
else
  log "❌ push 失敗"
  echo "error push-failed $(date -u +%FT%TZ)" > "$STATUSFILE"
  exit 1
fi
