import argparse
import statistics
from pathlib import Path
from typing import Any

from day14.dataset import load_golden_cases, select_scored_routing_cases
from day14.metrics import (
    calculate_route_accuracy, 
    calculate_per_class_route_accuracy, 
    build_confusion_matrix
)
from day14.keyword_router import run_keyword_router
from day14.llm_router import run_llm_router  


ALLOWED_ROUTES = {"smalltalk", "knowledge", "tool"}


def run_experiment(router_type: str, cases: list[dict]) -> dict[str, Any]:
    """Belirtilen router tipine göre evaluation vakalarını çalıştırır."""
    
    if router_type not in ("keyword", "llm"):
        raise ValueError(f"Bilinmeyen router tipi: {router_type}")

    case_results = []
    latencies = []
    failures = 0
    invalid_outputs = 0
    
    for case in cases:
        query = case["query"]
        
        try:
            if router_type == "keyword":
                result = run_keyword_router(query)
            elif router_type == "llm":
                result = run_llm_router(query)
                
        except Exception as exc:
            result = {
                "route": None,
                "router": router_type,
                "latency_ms": 0.0,
                "fallback_used": False,
                "error_type": type(exc).__name__,
            }
            
        actual_route = result.get("route")
        latency = result.get("latency_ms", 0.0)
        error_type = result.get("error_type")

        if isinstance(latency, bool) or not isinstance(latency, (int, float)):
            latency = 0.0
            error_type = error_type or "InvalidLatencyError"
        
        latencies.append(latency)
        
        if error_type is not None:
            failures += 1
            
        if actual_route not in ALLOWED_ROUTES:
            invalid_outputs += 1
            
        expected_route = case.get("expected_route")
        route_correct = None
        if expected_route is not None:
            route_correct = (expected_route == actual_route)
            
        case_results.append({
            "id": case["id"],
            "query": query,
            "expected": {
                "route": expected_route,
            },
            "actual": {
                "route": actual_route,
                "router": result.get("router", router_type),
                "latency_ms": latency,
                "fallback_used": result.get("fallback_used", False),
                "error_type": error_type,
            },
            "scores": {
                "route_correct": route_correct
            }
        })
        
    route_acc = calculate_route_accuracy(case_results)
    per_class_acc = calculate_per_class_route_accuracy(cases, case_results)

    valid_case_results = [
        result
        for result in case_results
        if result.get("actual", {}).get("route") in ALLOWED_ROUTES
    ]
    valid_result_ids = {result["id"] for result in valid_case_results}
    valid_cases = [case for case in cases if case["id"] in valid_result_ids]
    conf_matrix = build_confusion_matrix(valid_cases, valid_case_results)
    
    avg_latency = statistics.mean(latencies) if latencies else 0.0
    median_latency = statistics.median(latencies) if latencies else 0.0
    
    return {
        "case_results": case_results,
        "accuracy": route_acc,
        "per_class": per_class_acc,
        "confusion_matrix": conf_matrix,
        "failures": failures,
        "invalid_outputs": invalid_outputs,
        "avg_latency": avg_latency,
        "median_latency": median_latency,
    }


def print_comparison_table(keyword_metrics: dict, llm_metrics: dict) -> None:
    """Kılavuzdaki Keyword vs LLM karşılaştırma tablosunu konsola basar."""
    
    def fmt_acc(acc_dict: dict) -> str:
        if acc_dict.get("accuracy") is None:
            return "N/A"
        return f"{acc_dict['accuracy'] * 100:.1f}% ({acc_dict['correct']}/{acc_dict['denominator']})"

    print("\n| Metric | Keyword | LLM |")
    print("|---|---:|---:|")
    
    # Global Accuracy
    kw_acc = fmt_acc(keyword_metrics["accuracy"])
    llm_acc = fmt_acc(llm_metrics["accuracy"])
    print(f"| Accuracy | {kw_acc} | {llm_acc} |")
    
    # Per-Class Accuracy
    for route in ["smalltalk", "knowledge", "tool"]:
        kw_class = fmt_acc(keyword_metrics["per_class"].get(route, {}))
        llm_class = fmt_acc(llm_metrics["per_class"].get(route, {}))
        print(f"| {route.capitalize()} accuracy | {kw_class} | {llm_class} |")
        
    # Errors & Latency
    print(f"| Invalid outputs | {keyword_metrics['invalid_outputs']} | {llm_metrics['invalid_outputs']} |")
    print(f"| Failures/timeouts | {keyword_metrics['failures']} | {llm_metrics['failures']} |")
    print(f"| Avg latency ms | {keyword_metrics['avg_latency']:.2f} | {llm_metrics['avg_latency']:.2f} |")
    print(f"| Median latency ms | {keyword_metrics['median_latency']:.2f} | {llm_metrics['median_latency']:.2f} |\n")


def print_single_result(router_type: str, metrics: dict) -> None:
    """Sadece tek bir router çalıştırıldığında özet sonuç basar."""
    print(f"\n=== {router_type.upper()} ROUTER SONUÇLARI ===")
    
    acc = metrics["accuracy"]
    acc_val = acc.get("accuracy")
    acc_str = f"{acc_val * 100:.1f}%" if acc_val is not None else "N/A"
    print(f"Global Accuracy: {acc_str} ({acc.get('correct')}/{acc.get('denominator')})")
    print(f"Avg Latency: {metrics['avg_latency']:.2f} ms")
    print(f"Median Latency: {metrics['median_latency']:.2f} ms")

    print("\nPer-Class Accuracy:")
    for route, route_metrics in metrics["per_class"].items():
        route_accuracy = route_metrics.get("accuracy")
        route_accuracy_text = (
            f"{route_accuracy * 100:.1f}%"
            if route_accuracy is not None
            else "N/A"
        )
        print(
            f"  {route}: {route_accuracy_text} "
            f"({route_metrics.get('correct')}/{route_metrics.get('denominator')})"
        )
    
    print("\nConfusion Matrix (Beklenen x Tahmin Edilen):")
    matrix = metrics["confusion_matrix"]
    for expected, predictions in matrix.items():
        print(f"  {expected}: {predictions}")
    print("=" * 40 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Router Benchmark Deneyi")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--router", choices=["keyword", "llm"], help="Çalıştırılacak router tipi.")
    mode.add_argument("--compare", action="store_true", help="Keyword ve LLM router'ı karşılaştır.")
    args = parser.parse_args()

    # Veri setini yükle
    try:
        registered_tools = {"calculate_shipping_cost", "search_notes"}
        dataset_path = Path(__file__).resolve().parent / "data" / "golden_cases.jsonl"
        all_cases = load_golden_cases(dataset_path, registered_tools)
        
        # Yalnızca skorlanacak routing vakalarını al
        routing_cases = select_scored_routing_cases(all_cases)
    except Exception as e:
        print(f"Veri seti yüklenirken hata oluştu: {e}")
        return

    print(f"Toplam skorlanacak routing vakası: {len(routing_cases)}")

    try:
        if args.compare:
            print("\nKarşılaştırmalı evaluation başlatılıyor...")
            kw_metrics = run_experiment("keyword", routing_cases)
            llm_metrics = run_experiment("llm", routing_cases)
            print_comparison_table(kw_metrics, llm_metrics)
        else:
            print(f"\n'{args.router}' evaluation başlatılıyor...")
            metrics = run_experiment(args.router, routing_cases)
            print_single_result(args.router, metrics)
    except NotImplementedError as exc:
        print(f"Evaluation başlatılamadı: {exc}")


if __name__ == "__main__":
    main()
