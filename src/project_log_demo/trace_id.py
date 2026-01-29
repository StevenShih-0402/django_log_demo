# /src/project_log_demo/trace_id.py
# 負責在日誌中注入與管理唯一追蹤 ID (Trace ID)。

import uuid
import logging
from asgiref.local import Local

# 使用 Local 存儲每個線程/協程的 Trace ID
_storage = Local()

def get_trace_id():
    """
    獲取當前請求的 Trace ID，如果不存在則生成一個。
    """
    return getattr(_storage, 'trace_id', 'no-trace-id')

def set_trace_id(trace_id=None):
    """
    設定當前請求的 Trace ID。
    """
    if trace_id is None:
        trace_id = str(uuid.uuid4())
    _storage.trace_id = trace_id
    return trace_id

def clear_trace_id():
    """
    清除當前請求的 Trace ID。
    """
    if hasattr(_storage, 'trace_id'):
        del _storage.trace_id

class TraceIDFilter(logging.Filter):
    """
    日誌過濾器，將 Trace ID 注入到每筆日誌紀錄中。
    """
    def filter(self, record):
        record.trace_id = get_trace_id()
        return True
