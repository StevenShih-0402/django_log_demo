# /src/project_log_demo/middleware.py
# 負責處理每個請求的 Trace ID 生命週期。

from .trace_id import set_trace_id, clear_trace_id

class TraceIDMiddleware:
    """
    中介軟體，用於在請求開始時生成 Trace ID 並在結束時清除。
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 從請求標頭中嘗試獲取傳入的 trace_id，否則生成新的
        trace_id = request.headers.get('X-Trace-ID')
        trace_id = set_trace_id(trace_id)
        
        response = self.get_response(request)
        
        # 在回應標頭中附帶 Trace ID 以便追蹤
        response['X-Trace-ID'] = trace_id
        
        # 請求結束，清除存儲
        clear_trace_id()
        
        return response
