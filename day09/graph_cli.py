import sys
from day09.state import create_initial_state
from day09.graph_workflow import graph
from day09.trace_writer import write_trace

def run_langgraph_workflow(query: str):
    print(f"\n{'='*50}\nSORU: {query}")
    
    # 1. Başlangıç durumunu oluştur
    initial_state = create_initial_state(query)
    
    # 2. Graph'ı çalıştır (invoke)
    print("[SİSTEM] LangGraph orkestrasyonu başlatılıyor...")
    final_state = graph.invoke(initial_state)
    
    # 3. TRACE'İ KAYDET (İşte burayı ekliyoruz!)
    write_trace(final_state)
    print("[SİSTEM] Trace (iz) başarıyla output/day09-workflow-traces.jsonl dosyasına kaydedildi.")
    
    # 4. Sonuçları ekrana yazdır
    print(f"[ROTA]: {final_state.get('route')}")
    print(f"[TRACE]: {final_state.get('node_trace')}")
    print(f"[CEVAP]: {final_state.get('answer')}")
    print(f"[ADIM SAYISI]: {final_state.get('step_count')}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
        run_langgraph_workflow(user_query)
    else:
        test_queries = [
            "Merhaba",
            "Named volume nedir?",
            "Ankara'ya 2 kg kargo ne kadar?",
            "Eski roma imparatorluğu nasıl yıkıldı?", 
            "selam, bana shipping fiyatı hesapla" 
        ]
        
        for q in test_queries:
            run_langgraph_workflow(q)