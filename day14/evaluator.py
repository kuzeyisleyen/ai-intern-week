import time
from typing import Any, Dict, List

from day09.native_workflow import run_native_workflow
from day14.router_experiment import run_experiment

def evaluate_trajectory(expected: List[str], actual: List[str]) -> bool:
    """Kılavuza göre 'ordered subsequence' (sıralı alt dizi) kontrolü yapar."""
    if not expected:
        return True
    if not actual:
        return False
    
    expected_idx = 0
    for node in actual:
        if expected_idx < len(expected) and node == expected[expected_idx]:
            expected_idx += 1
            
    return expected_idx == len(expected)

def run_workflow_suite(cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Workflow (Uçtan uca sistem) evaluation metriklerini hesaplar."""
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
            state = run_native_workflow(case["query"])
        except Exception as exc:
            state = {"status": "error", "error_type": type(exc).__name__}
            
        duration_ms = (time.perf_counter() - start_time) * 1000
        
        actual = {
            "route": state.get("route"),
            "tool": state.get("tool_name"),
            "provider": state.get("tool_provider"), 
            "trajectory": state.get("node_trace", []),
            "terminal_status": state.get("status")
        }
        
        scores = {}
        
        # Her metrik için farklı payda (denominator) hesaplaması ve null kontrolü
        if "expected_route" in case:
            metrics["route"]["total"] += 1
            scores["route_correct"] = (actual["route"] == case["expected_route"])
            if scores["route_correct"]: metrics["route"]["correct"] += 1
        else:
            scores["route_correct"] = None
            
        if "expected_tool" in case:
            metrics["tool"]["total"] += 1
            scores["tool_correct"] = (actual["tool"] == case["expected_tool"])
            if scores["tool_correct"]: metrics["tool"]["correct"] += 1
        else:
            scores["tool_correct"] = None
            
        if "expected_tool_provider" in case:
            metrics["provider"]["total"] += 1
            scores["provider_correct"] = (actual["provider"] == case["expected_tool_provider"])
            if scores["provider_correct"]: metrics["provider"]["correct"] += 1
        else:
            scores["provider_correct"] = None
            
        if "approval_required" in case:
            metrics["approval"]["total"] += 1
            scores["approval_correct"] = (state.get("approval_required", False) == case["approval_required"])
            if scores["approval_correct"]: metrics["approval"]["correct"] += 1
        else:
            scores["approval_correct"] = None
            
        if "expected_terminal_status" in case:
            metrics["terminal"]["total"] += 1
            scores["terminal_correct"] = (actual["terminal_status"] == case["expected_terminal_status"])
            if scores["terminal_correct"]: metrics["terminal"]["correct"] += 1
        else:
            scores["terminal_correct"] = None
            
        if "allowed_trajectory" in case:
            metrics["trajectory"]["total"] += 1
            scores["trajectory_correct"] = evaluate_trajectory(case["allowed_trajectory"], actual["trajectory"])
            if scores["trajectory_correct"]: metrics["trajectory"]["correct"] += 1
        else:
            scores["trajectory_correct"] = None
            
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
    """Routing experiment'ini evaluator yapısına bağlar."""
    routing_cases = [c for c in cases if c.get("suite") == "routing" or "expected_route" in c]
    return run_experiment(router_type, routing_cases)