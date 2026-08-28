import json
import uuid
from pathlib import Path

def write_trace(state: dict):
    output_file = Path("output/day09-workflow-traces.jsonl")
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    retrieved_data = []
    for chunk in state.get("retrieved_chunks", []):
        retrieved_data.append({
            "chunk_id": chunk.get("chunk_id"),
            "score": chunk.get("score")
        })
    
    #sözlük formatı
    trace_record = {
        "run_id": str(uuid.uuid4()),
        "query": state.get("query"),
        "route": state.get("route"),
        "original_query": state.get("original_query"),
        "retrieval_query": state.get("retrieval_query"),
        "rewrite_count": state.get("rewrite_count", 0),
        "node_trace": state.get("node_trace", []),
        "retrieved": retrieved_data,
        "tool_name": state.get("tool_name"),
        "status": state.get("status"),
        "final_answer": state.get("answer"),
        "error_type" : state.get("error_type"),
        "failed_node":state.get("failed_node"),
        "fallback_reason":state.get("fallback_reason"),
        "errors":state.get("errors",[])
    }
    
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(trace_record, ensure_ascii=False) + "\n")