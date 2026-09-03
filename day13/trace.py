import json
import os
import time

TRACE_FILE = "output/day13-hitl-traces.jsonl"

def log_trace(
    thread_id: str,
    action_id: str = None,
    action_type: str = None,
    node: str = None,
    approval_required: bool = None,
    approval_decision: str = None,
    interrupt_reason: str = None,
    resumed: bool = False,
    status: str = None,
    terminal_status: str = None,
    error_type: str = None,
    duration_ms: int = None,
    run_id: str = None
) -> None:
    """
    Workflow event'lerini JSONL formatında kaydeder.
    Hassas payload verilerini (örn. mail body, finansal detaylar) içermez.
    """
    os.makedirs(os.path.dirname(TRACE_FILE), exist_ok=True)
    
    trace_event = {
        "timestamp": time.time(),
        "run_id": run_id,
        "thread_id": thread_id,
        "action_id": action_id,
        "action_type": action_type,
        "node": node,
        "approval_required": approval_required,
        "approval_decision": approval_decision,
        "interrupt_reason": interrupt_reason,
        "resumed": resumed,
        "status": status,
        "terminal_status": terminal_status,
        "error_type": error_type,
        "duration_ms": duration_ms
    }
    
    # None olmayan değerleri filtreleyerek temiz bir log oluştur
    clean_event = {k: v for k, v in trace_event.items() if v is not None}
    
    with open(TRACE_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(clean_event) + "\n")