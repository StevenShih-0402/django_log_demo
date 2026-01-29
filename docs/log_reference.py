import os
import sys
from datetime import datetime

from colorlog import ColoredFormatter

from project_log_demo.trace_id import TraceIDFilter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# === 建立 logs 目錄（依日期分資料夾） ===
today_str = datetime.now().strftime("%Y-%m-%d")
LOG_BASE_DIR = BASE_DIR / 'logs' / today_str
LOG_BASE_DIR.mkdir(parents=True, exist_ok=True)

# === 設定 logs 訊息格式（含顏色與時間） ===
LOG_FORMAT = "%(log_color)s%(asctime)s | %(levelname)s | %(name)s | trace_id=%(trace_id)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# === 設定 DEBUG logs 是否輸出到終端機的 Flag 檔案設定 ===
DEBUG_FLAG_PATH = os.path.join(BASE_DIR, 'project_log_demo', '.debug_log_enabled')
DEBUG_LOG_ENABLED = os.path.exists(DEBUG_FLAG_PATH)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'filters': {
        'trace_id': {
            '()': TraceIDFilter,
        },
    },

    # Django (Python) 標準 Log 處理方式無法解析 colorlog 建立的 logger record
    'formatters': {
        'standard': {
            'format': "%(asctime)s | %(levelname)s | %(name)s | trace_id=%(trace_id)s | %(message)s",
            'datefmt': DATE_FORMAT
        },
        'colored': {
            '()': ColoredFormatter,
            'format': LOG_FORMAT,
            'datefmt': DATE_FORMAT,
            'log_colors': {
                'DEBUG':    'cyan',
                'INFO':     'black,bg_green',
                'WARNING':  'black,bg_yellow',
                'ERROR':    'white,bg_red',
                'CRITICAL': 'white,bg_purple',
            },
        },
    },

    'handlers': {
        # Console 彩色輸出
        'console': {
            'level': 'DEBUG' if DEBUG_LOG_ENABLED else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
            'filters': ['trace_id'],
            'stream': sys.stdout,
        },

        # 系統層 logger（每天一檔）
        'system_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOG_BASE_DIR / 'system.log',
            'when': 'midnight',
            'backupCount': 30,
            'encoding': 'utf-8',
            'formatter': 'standard',
            'filters': ['trace_id'],
        },

        # 用戶操作 logger（每天一檔）
        'audit_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOG_BASE_DIR / 'audit.log',
            'when': 'midnight',
            'backupCount': 30,
            'encoding': 'utf-8',
            'formatter': 'standard',
            'filters': ['trace_id'],
        },

        # Debug logger（每天一檔）
        'debug_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOG_BASE_DIR / 'debug.log',
            'when': 'midnight',
            'backupCount': 30,
            'encoding': 'utf-8',
            'formatter': 'standard',
            'filters': ['trace_id'],
            'level': 'DEBUG',
        },
    },

    'loggers': {
        # 系統層 logger
        'django': {
            'handlers': ['console', 'debug_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'app.system': {
            'handlers': ['console', 'system_file', 'debug_file'],
            'level': 'INFO',
            'propagate': False,
        },

        # 用戶操作 logger
        'audit': {
            'handlers': ['console', 'audit_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },

    'root': {
        'handlers': ['console', 'debug_file'],
        'level': 'DEBUG' if DEBUG_LOG_ENABLED else 'INFO',
    },
}
