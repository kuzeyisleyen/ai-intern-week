import json
import time
import uuid
from pathlib import Path
from typing import Dict, Any

def log_tool_trace(adapter_response: Dict[str, Any], tool_name: str) -> None:
    """
    MCP Adaptöründen dönen standart yanıtı alır ve 
    kılavuzun observability kontratına uygun olarak ayrı bir JSON dosyasına yazar.
    """
    # Her kayıt için benzersiz bir dosya adı 
    timestamp = int(time.time())
    short_id = str(uuid.uuid4())[:8]
    output_file = Path(f"output/traces/trace_{timestamp}_{short_id}.json")
    
    # Klasör yoksa oluştur
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    trace_data = adapter_response.get("trace", {})
    
    trace_record = {
        "capability_name": tool_name,
        "status": adapter_response.get("status"),
        "provider": trace_data.get("provider"),
        "server_name": trace_data.get("server_name"),
        "capability_type": trace_data.get("capability_type", "tool"),
        "transport": trace_data.get("transport"),
        "duration_ms": trace_data.get("duration_ms"),
        "error_type": trace_data.get("error_type")
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(trace_record, ensure_ascii=False, indent=2))