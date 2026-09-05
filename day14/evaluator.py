import time
from typing import Any, Dict, List

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

from day09.native_workflow import run_native_workflow
from day13.durable_graph import get_durable_graph_builder
from day14.router_experiment import run_experiment
from day14.metrics import score_case

def normalize_workflow_result(state: dict) -> dict:
    """Ders 2 ve 4: State nesnesini evaluator'ın beklediği formata dönüştürür."""
    trace = state.get("trace") or {}
    
    raw_trajectory = state.get("node_trace", [])
    mapping = {
        "generate_with_context": "generate",
        "check_quality": "retrieval_quality",
        "execute_tool": "tool",
        "tool_node": "tool"
    }
    mapped_trajectory = [mapping.get(node, node) for node in raw_trajectory]

    return {
        "route": state.get("route"),
        "tool": state.get("tool_name"),
        "provider": state.get("tool_provider") or trace.get("provider"),
        "trajectory": mapped_trajectory,
        "terminal_status": state.get("status"),
        "approval_required": state.get("approval_required", False)
    }

def run_durable_workflow(case: dict) -> dict:
    """Day 13'ün gerçek altyapısını kullanarak durable vakalarını test eder."""
    builder = get_durable_graph_builder()
    
    with SqliteSaver.from_conn_string(":memory:") as checkpointer:
        graph = builder.compile(checkpointer=checkpointer)
        config = {"configurable": {"thread_id": case["id"]}}
        
        # Vaka dosyasından eylemi çek, yoksa varsayılanı kullan
        action_type = case.get("expected_action", "publish_report")
        
        graph.invoke({"action_type": action_type}, config)
        
        snapshot = graph.get_state(config)
        is_interrupted = len(snapshot.next) > 0
        
        # 3. Eğer vaka dosyasında bir "devam kararı" (resume_payload) varsa ve sistem durmuşsa, kararı uygula
        resume_payload = case.get("resume_payload")
        if is_interrupted and resume_payload:
            graph.invoke(Command(resume=resume_payload), config)
            snapshot = graph.get_state(config)
            is_interrupted = len(snapshot.next) > 0
            
        final_state = snapshot.values or {}
        
        # 4. Final state durumunu normalize_workflow_result fonksiyonunun anlayacağı basitliğe indirge
        status = "interrupted" if is_interrupted else final_state.get("status")
        
        return {
            "status": status,
            "approval_required": final_state.get("approval_required", False),
            "node_trace": final_state.get("node_trace", []),
        }

def execute_case(case: dict) -> dict:
    """Ders 1: Suite'e göre doğru runner'ı çalıştırır."""
    suite = case.get("suite")
    
    if suite == "durable":
        return run_durable_workflow(case)
        
    # Workflow ve diğer durumlar için native çalıştırıcı
    return run_native_workflow(case["query"])

def run_workflow_suite(cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    workflow_cases = [c for c in cases if c.get("suite") in ("workflow", "durable")]
    
    results = []
    metrics = {
        "route": {"correct": 0, "total": 0},
        "tool": {"correct": 0, "total": 0},
        "provider": {"correct": 0, "total": 0},
        "approval": {"correct": 0, "total": 0},
        "terminal": {"correct": 0, "total": 0},
        "trajectory": {"correct": 0, "total": 0},
    }
    
    for case in workflow_cases:
        start_time = time.perf_counter()
        
        try:
            state = execute_case(case)
        except Exception as exc:
            state = {"status": "error", "error_type": type(exc).__name__}
            
        duration_ms = (time.perf_counter() - start_time) * 1000
        
        actual = normalize_workflow_result(state)
        #logic tekrarı kalktı metrics.py kullanılıyor
        scores = score_case(case, actual)
        
        for key in ["route", "tool", "provider", "approval", "terminal", "trajectory"]:
            score_val = scores.get(f"{key}_correct")
            if score_val is not None:
                metrics[key]["total"] += 1
                if score_val is True:
                    metrics[key]["correct"] += 1
            
        results.append({
            "id": case["id"],
            "actual": actual,
            "scores": scores,
            "duration_ms": int(duration_ms)
        })
        
    def calc_acc(metric_key: str) -> float:
        tot = metrics[metric_key]["total"]
        return (metrics[metric_key]["correct"] / tot) if tot > 0 else 0.0
        
    aggregate = {
        "case_count": len(workflow_cases),
        "route_accuracy": calc_acc("route"),
        "tool_accuracy": calc_acc("tool"),
        "provider_accuracy": calc_acc("provider"),
        "approval_accuracy": calc_acc("approval"),
        "terminal_accuracy": calc_acc("terminal"),
        "trajectory_accuracy": calc_acc("trajectory")
    }
    
    return {"per_case_results": results, "aggregate_result": aggregate}

def run_routing_suite(cases: List[Dict[str, Any]], router_type: str) -> Dict[str, Any]:
    routing_cases = [c for c in cases if c.get("suite") == "routing" or "expected_route" in c]
    return run_experiment(router_type, routing_cases)