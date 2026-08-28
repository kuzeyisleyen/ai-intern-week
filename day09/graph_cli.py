import sys
from day09.state import create_initial_state
from day09.graph_workflow import run_graph_workflow
from day09.trace_writer import write_trace

def print_workflow_trace(state: dict):
    """İş akışı tamamlandıktan sonra terminale basar."""
    print("\n" + "="*40)
    print(" WORKFLOW ÖZETİ")
    print("="*40)
    print(f"Durum (Status): {state.get('status')}")
    print(f"Rota (Route): {state.get('route', 'Belirlenmedi')}")
    
    trace = state.get("node_trace", [])
    print(f"İz (Trace): {' ➔ '.join(trace) if trace else 'Boş'}")
        
    if state.get("status") in ["error", "stopped"]:
        print("-" * 40)
        print(" HATA DETAYLARI")
        print(f"Hata Türü: {state.get('error_type', 'Bilinmiyor')}")
        print(f"Kopan Düğüm: {state.get('failed_node', 'Bilinmiyor')}")
        if state.get("fallback_reason"):
            print(f"Fallback Nedeni: {state.get('fallback_reason')}")
        if state.get("errors"):
            print("Hata Mesajları :")
            for err in state.get("errors", []):
                print(f"  - {err}")
    else:
        print(f"\nCEVAP: {state.get('answer', 'Cevap üretilemedi.')}")
        
    print("="*40 + "\n")

def run_langgraph_workflow_cli(query: str):
    print(f"\n{'='*50}\nSORU: {query}")
    print("[SİSTEM] LangGraph orkestrasyonu başlatılıyor...")
    
    final_state = run_graph_workflow(query)
    
    write_trace(final_state)
    print("[SİSTEM] Trace (iz) başarıyla output/day09-workflow-traces.jsonl dosyasına kaydedildi.")
    
    print_workflow_trace(final_state)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
        run_langgraph_workflow_cli(user_query)
    else:
        test_queries = [
            "Merhaba",
            "Named volume nedir?",
            "Ankara'ya 2 kg kargo ne kadar?",
            "Eski roma imparatorluğu nasıl yıkıldı?", 
            "selam, bana shipping fiyatı hesapla" 
        ]
        
        for q in test_queries:
            run_langgraph_workflow_cli(q)