import argparse
import json
from pathlib import Path
from datetime import datetime

from day14.dataset import load_golden_cases
from day14.evaluator import run_workflow_suite, run_routing_suite

def main() -> None:
    parser = argparse.ArgumentParser(description="System Evaluation Runner")
    parser.add_argument("--suite", choices=["routing", "workflow"], help="Çalıştırılacak test paketi")
    parser.add_argument("--router", choices=["keyword", "llm"], help="Routing testleri için router tipi")
    parser.add_argument("--all", action="store_true", help="Tüm suite'leri çalıştır")
    
    args = parser.parse_args()
    
    if not args.suite and not args.all:
        parser.error("Ya --suite ya da --all belirtilmelidir.")
        
    if (args.suite == "routing" or args.all) and not args.router and not args.all:
        parser.error("--suite routing seçildiğinde --router [keyword|llm] belirtilmelidir.")
        
    dataset_path = Path(__file__).resolve().parent / "data" / "golden_cases.jsonl"
    registered_tools = {"calculate_shipping_cost", "search_notes"}
    all_cases = load_golden_cases(str(dataset_path), registered_tools)
    
    output_dir = Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    if args.all or args.suite == "routing":
        routers = ["keyword", "llm"] if args.all else [args.router]
        routing_report = {"generated_at": datetime.now().isoformat(), "results": {}}
        
        for r_type in routers:
            print(f"\n--- Routing Suite ({r_type}) çalıştırılıyor ---")
            metrics = run_routing_suite(all_cases, r_type)
            routing_report["results"][r_type] = metrics
            
        routing_out = output_dir / "day14-routing-comparison.json"
        with open(routing_out, "w", encoding="utf-8") as f:
            json.dump(routing_report, f, indent=2, ensure_ascii=False)
        print(f"Routing comparison raporu yazıldı: {routing_out}")

    if args.all or args.suite == "workflow":
        print("\n--- Workflow Suite çalıştırılıyor ---")
        workflow_metrics = run_workflow_suite(all_cases)
        
        report = {
            "config": {
                "model": "qwen3:1.7b",
                "temperature": 0,
                "allowed_routes": ["smalltalk", "knowledge", "tool"],
                "available_tools": list(registered_tools)
            },
            "generated_at": datetime.now().isoformat(),
            "workflow_metrics": workflow_metrics
        }
        
        report_out = output_dir / "day14-evaluation-report.json"
        with open(report_out, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"Workflow evaluation raporu yazıldı: {report_out}")

if __name__ == "__main__":
    main()