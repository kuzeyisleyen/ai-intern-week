import time
from typing import Any, Dict

from day09.nodes import classify_keyword 

def run_keyword_router(query: str) -> Dict[str, Any]:
    """
    Sınıflandırma sonucunu, çalışma süresini ve hataları paketler.
    """
    start_time = time.perf_counter()
    
    route = classify_keyword(query)
    
    end_time = time.perf_counter()
    latency_ms = (end_time - start_time) * 1000 
    
    return {
        "route": route,
        "router": "keyword",
        "latency_ms": latency_ms,
        "fallback_used": False,
        "error_type": None,
    }