#!/usr/bin/env python3
"""
NewsRadar - Main Entry Point
Command-line interface for the news aggregation system

Usage:
    python main.py              # Run once
    python main.py --serve     # Run with auto-refresh
    python main.py --cron      # Run as cron job
"""

import argparse
import sys
import os
import time
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_once():
    """Run a single update cycle"""
    from scheduler import run_update
    return run_update()


def run_serve(refresh_interval: int = 1800):
    """Run with periodic updates"""
    logger.info(f"🔄 啟動自動更新模式（每 {refresh_interval} 秒）")
    logger.info("按 Ctrl+C 停止")
    
    while True:
        try:
            run_once()
            time.sleep(refresh_interval)
        except KeyboardInterrupt:
            logger.info("👋 停止自動更新")
            break


def run_cron():
    """Run as cron job (compatible with GitHub Actions)"""
    logger.info("⏰ 執行 Cron 任務...")
    articles = run_once()
    if articles:
        logger.info(f"✅ Cron 任務完成：{len(articles)} 篇文章")
    else:
        logger.error("❌ Cron 任務失敗：無文章")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="NewsRadar - 新聞聚合系統")
    parser.add_argument(
        "--serve",
        action="store_true",
        help="啟動自動更新模式"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=1800,
        help="自動更新間隔（秒），預設 1800（30分鐘）"
    )
    parser.add_argument(
        "--cron",
        action="store_true",
        help="以 Cron 模式執行（用於 GitHub Actions）"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="測試模式：使用少量信源"
    )
    
    args = parser.parse_args()
    
    if args.cron:
        run_cron()
    elif args.serve:
        run_serve(args.interval)
    else:
        run_once()


if __name__ == "__main__":
    main()
