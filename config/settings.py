"""
配置文件
包含所有的設置和配置項
"""

import os
from pathlib import Path

# 基礎路徑設置
BASE_DIR = Path(__file__).resolve().parent.parent
CHROME_DATA_DIR = BASE_DIR / "chrome-data"
CHROME_LOGIN_DATA_DIR = BASE_DIR / "chrome-login-data"
LOGS_DIR = BASE_DIR / "logs"

# Chrome 設置
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROME_PORT = 9222
MAX_RETRIES = 3
PAGE_LOAD_TIMEOUT = 15

# API 設置
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# User Agent 池
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.92 Mobile Safari/537.36",
]

# 日誌設置
LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': str(LOGS_DIR / 'scraper.log')
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        }
    }
} 