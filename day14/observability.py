import json
import time
from datetime import datetime
from typing import Any, Dict, Optional

TRACE_FILE = "output/day14-spans.jsonl"

def record_span(
    run_id: str,
    thread_id: str,
    operation: str,
    component: str,
    start_time: float,
    status: str = "ok",
    error_type: Optional[str] = None,
    attributes: Optional[Dict[str, Any]] = None
) -> None:
    """
    Span mental modeline uygun, privacy-safe (gizlilik odaklı) log kaydı atar.
    """
    duration_ms = int((time.perf_counter() - start_time) * 1000)
    
    safe_attributes = attributes or {}
    
    span_data = {
        "timestamp": datetime.now().isoformat(),
        "run_id": run_id,
        "thread_id": thread_id,
        "operation": operation,
        "component": component,
        "duration_ms": duration_ms,
        "status": status,
        "error_type": error_type,
        "attributes": safe_attributes
    }
    
    with open(TRACE_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(span_data, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    t0 = time.perf_counter()
    time.sleep(0.1) 
    
    record_span(
        run_id="run-123",
        thread_id="thread-456",
        operation="router.classify",
        component="llm_router",
        start_time=t0,
        status="ok",
        attributes={
            "query_length": 15,
            "route": "tool",
            "router_type": "llm"
        }
    )
    print(f"Örnek span '{TRACE_FILE}' dosyasına yazıldı.")